from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

import models


class CreateDealForm(forms.ModelForm):
    class Meta:
        model = models.Deal
        fields = ('ad', 'amount', 'bid', 'owner', 'creator')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(CreateDealForm, self).__init__(*args, **kwargs)

        self.fields['owner'].required = False
        self.fields['creator'].required = False

    def clean(self):
        cleaned_data = super(CreateDealForm, self).clean()
        cleaned_data.update({
            'owner': self.user.get_business_profile(),
            'creator': self.user.get_userprofile()
        })

        return cleaned_data

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        ad = self.cleaned_data.get('ad')

        MaxValueValidator(ad.amount)(amount)
        MinValueValidator(1)(amount)

        return amount

    def save(self, commit=True):
        deal = super(CreateDealForm, self).save(commit)

        if commit:
            LogEntry.objects.log_action(
                user_id         = self.user.pk,
                content_type_id = ContentType.objects.get_for_model(deal).pk,
                object_id       = deal.pk,
                object_repr     = '(Frontend)' + force_unicode(deal),
                action_flag     = ADDITION
            )

        deal.send_mail('interested', deal.ad.creator.user.email, deal.ad.creator.lang_code)
        return deal


class DealForm(forms.Form):
    ACTION_CHOICES = (
        (models.Deal.ACTIVATE, _('Activate')),
        (models.Deal.EXTEND, _('Extend')),
        (models.Deal.CANCEL, _('Cancel')),
        (models.Deal.COMPLETE, _('Complete')),
    )
    action = forms.ChoiceField(choices=ACTION_CHOICES, required=True)
    cancel_reason = forms.CharField(max_length=2000, required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    amount = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.instance = kwargs.pop('instance')
        super(DealForm, self).__init__(*args, **kwargs)

        if self.data.get('action', None) == models.Deal.CANCEL:
            self.fields['cancel_reason'].required = True
        elif self.data.get('action', None) == models.Deal.COMPLETE:
            self.fields['price'].required = True
            self.fields['amount'].required = True

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        if amount is not None:
            MaxValueValidator(self.instance.ad.amount)(amount)
            MinValueValidator(1)(amount)

        return amount

    def clean_action(self):
        action = self.cleaned_data.get('action', None)

        if self.instance.state == 'interested':
            valid_actions = [models.Deal.ACTIVATE]
        elif self.instance.state == 'active':
            valid_actions = [models.Deal.COMPLETE, models.Deal.EXTEND, models.Deal.CANCEL]
        else:
            valid_actions = []

        if action not in valid_actions:
            raise ValidationError('%s is not one of the valid actions: %s' % (action, ', '.join(valid_actions)))

        return action

    def save(self):
        cancel_reason = None
        price = None
        amount = None

        action = self.cleaned_data.get('action', None)

        if action == models.Deal.CANCEL:
            cancel_reason = self.cleaned_data.get('cancel_reason')
        elif action == models.Deal.COMPLETE:
            price = self.cleaned_data.get('price')
            amount = self.cleaned_data.get('amount')

        self.instance.do_action(action, cancel_reason, amount, price)

        LogEntry.objects.log_action(
            user_id         = self.user.pk,
            content_type_id = ContentType.objects.get_for_model(self.instance).pk,
            object_id       = self.instance.pk,
            object_repr     = '(Frontend)' + force_unicode(self.instance),
            action_flag     = CHANGE
        )

        return self.instance
