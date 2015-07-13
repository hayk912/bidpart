# coding=utf-8
from operator import __or__
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import resolve, reverse
from django.db.models import Q
from django.template import Context, Template
from django.utils import http
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from application.apps.accounts.functions import has_active_business_profile
from application.apps.cms.models import EmailTemplate
from application.apps.deals.func import deal_agent_price_sum, commission_level
from application.apps.deals.models import Deal
from application.apps.invoice.models import Invoice
from models import UserProfile, BusinessProfile
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE


class AccountForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length=30, required=True)
    last_name = forms.CharField(label=_('Last name'), max_length=30, required=True)
    phone = forms.CharField(max_length=32, required=False)
    email = forms.EmailField(label=_('Email'), max_length=75, required=True)
    email_confirm = forms.EmailField(label=_('Confirm email'), max_length=75, required=True)

    business_name = forms.CharField(label=_('Business name'), max_length=128, required=True)
    country = forms.CharField(label=_('Country'), max_length=128, required=True)
    address = forms.CharField(label=_('Address'), max_length=64, required=False)
    address_zipcode = forms.CharField(label=_('Zipcode'), max_length=5, required=False)
    address_city = forms.CharField(label=_('City'), max_length=64, required=False)
    business_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 8}))
    newsletter = forms.BooleanField(label=_('Sign me up for Bidpart newsletter'), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        if kwargs.get('data', False):
            kwargs['data'] = kwargs['data'].copy()
        super(AccountForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        users_queryset =  User.objects.filter(email=email)
        if self.initial.get('email', False):
            users_queryset = users_queryset.exclude(email=self.initial['email'])

        if users_queryset.exists():
            raise forms.ValidationError(_('The entered email already exists'))

        return email

    def clean_email_confirm(self):
        email = self.data.get('email', None)
        email_confirm = self.cleaned_data.get('email_confirm', None)

        if email != email_confirm:
            self.data['email_confirm'] = ''
            raise forms.ValidationError(_('Both email fields must match.'))

        return email_confirm

    def save_businessprofile(self, businessprofile):
        businessprofile.business_name = self.cleaned_data.get('business_name', None)
        businessprofile.company = self.cleaned_data.get('company', None)
        businessprofile.address = self.cleaned_data.get('address', None)
        businessprofile.address_zipcode = self.cleaned_data.get('address_zipcode', None)
        businessprofile.address_city = self.cleaned_data.get('address_city', None)
        businessprofile.country = self.cleaned_data.get('country', None)
        businessprofile.agent_id = self.cleaned_data.get('agent_id', None)
        businessprofile.business_description = self.cleaned_data.get('business_description', None)
        businessprofile.save()
        return businessprofile

    def save_userprofile(self, userprofile):
        userprofile.phone = self.cleaned_data.get('phone', None)
        userprofile.newsletter = self.cleaned_data.get('newsletter', False)
        userprofile.save()
        return userprofile

    def save_user(self, user):
        user.username = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        return user

    def save(self, user=None):
        if not user:
            user = User()

        if not user.pk:
            action_flag = ADDITION
        else:
            action_flag = CHANGE

        user = self.save_user(user)

        if has_active_business_profile(user):
            businessprofile = user.get_business_profile()
        else:
            businessprofile = BusinessProfile()
            businessprofile.creator = user.userprofile

        LogEntry.objects.log_action(
            user_id         = user.pk,
            content_type_id = ContentType.objects.get_for_model(user.userprofile).pk,
            object_id       = user.userprofile.pk,
            object_repr     = '(Frontend)' + force_unicode(user.userprofile),
            action_flag     = action_flag
        )

        businessprofile = self.save_businessprofile(businessprofile)

        if not has_active_business_profile(user):
            user.userprofile.active_profile = businessprofile
            user.userprofile.business_profiles.add(businessprofile)

        user.userprofile = self.save_userprofile(user.userprofile)

        return user


class SignupForm(AccountForm):
    password = forms.CharField(label=_('Password (min 6)'), min_length=6, required=True, widget=forms.PasswordInput)
    terms = forms.BooleanField(label=_('Yes, I approve of the'), required=True)
    next = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput)
    agent_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def clean_agent_id(self):
        agent_id = self.cleaned_data.get('agent_id')
        if agent_id:
            if not BusinessProfile.objects.filter(pk=agent_id, is_agent=True).exists():
                agent_id = None

        return agent_id

    def save_user(self, user):
        user.set_password(self.cleaned_data.get('password'))
        return super(SignupForm, self).save_user(user)

    def save_businessprofile(self, businessprofile):
        businessprofile.agent_id = self.cleaned_data.get('agent_id')
        return super(SignupForm, self).save_businessprofile(businessprofile)


class LoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)
    next = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError(_('Invalid email or password'))
        if not user.is_active:
            raise ValidationError(_('Invalid email or password'))

        self.user = user
        return cleaned_data


class AgentDealSearchForm(forms.Form):
    q = forms.CharField(required=False)
    state = forms.ChoiceField(choices=Deal.STATES, required=False)

    def __init__(self, *args, **kwargs):
        self.businessprofile = kwargs.pop('businessprofile', None)
        super(AgentDealSearchForm, self).__init__(*args, **kwargs)

        self.fields['q'].widget.attrs['placeholder'] = _('Search')
        self.fields['q'].widget.attrs['class'] = 'input-large'

        state_choices = list(Deal.STATES)
        state_choices.insert(0, ('', _('All states')),)
        self.fields['state'].choices = state_choices

    def all(self):
        return Deal.objects.filter(ad__owner__agent=self.businessprofile)

    def search(self):
        q = self.cleaned_data.get('q')
        state = self.cleaned_data.get('state')
        deals = self.all()

        if q:
            q_objects = []
            for lang_code, lang_name in settings.LANGUAGES:
                q_objects.append(Q(**{
                    'ad__title_{0}__icontains'.format(lang_code): q
                }))
            deals = deals.filter(reduce(__or__, q_objects))

        if state:
            deals = deals.filter(state=state)

        return deals


class AgentInviteForm(forms.Form):
    email = forms.EmailField(required=True, label=_('Recruit somone?'))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AgentInviteForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'span2'
        self.fields['email'].widget.attrs['placeholder'] = _('Email')

    def send_invite(self):
        template = EmailTemplate.objects.get(name='agent_invite')
        context = Context({
            'invite_url': 'http://{0}{1}?a={2}'.format(
                settings.BASE_URL,
                reverse('accounts:signup'),
                self.request.user.get_business_profile().pk
            )
        })
        lang_code = self.request.LANGUAGE_CODE
        subject = template.get_localized('subject', lang_code)
        email_html = Template(template.get_localized('html', lang_code)).render(context)
        email_txt = Template(template.get_localized('txt', lang_code)).render(context)

        message = EmailMultiAlternatives(subject=subject, to=[self.cleaned_data['email']])
        message.attach_alternative(email_html, 'text/html')
        message.attach_alternative(email_txt, 'text/plain')

        message.send()


class AgentInvoiceForm(forms.Form):
    deals = forms.ModelMultipleChoiceField(queryset=None, error_messages={'required': _('You need to select one or more choices.')})

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.agent = self.user.get_business_profile()
        super(AgentInvoiceForm, self).__init__(*args, **kwargs)

        self.fields['deals'].queryset = Deal.objects.filter(
            ad__owner__agent=self.agent,
            state='completed',
            payed_to_agent=False
        )

    def make_invoice(self):
        deals = self.cleaned_data.get('deals')
        invoice = Invoice.create_from_deals(deals, sender=self.user, from_agent=True)
        invoice.write_pdf()
        return invoice


