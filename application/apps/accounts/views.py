from urlparse import urlparse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.db.models import Q, Count, Sum
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils import translation
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, FormView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import ProcessFormView, FormMixin
from application import settings
from application.apps.ads.models import Ad
from application.apps.deals.func import deal_agent_price_sum
from application.apps.deals.models import Deal
from forms import LoginForm, SignupForm, AccountForm, AgentDealSearchForm, AgentInviteForm, AgentInvoiceForm
from models import BusinessProfile, UserProfile
from functions import has_active_business_profile


class AccountFormView(FormView):
    template_name = 'accounts/account_form.html'
    form_class = AccountForm

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(AccountFormView, self).get_context_data(**kwargs)
        kwargs['group'] = 'settings'
        kwargs['type'] = 'account_form'

        return kwargs

    def get_initial(self):
        initial = super(AccountFormView, self).get_initial()
        user = self.request.user
        business_profile = user.get_business_profile()

        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.userprofile.phone,
            'email': user.email,
            'email_confirm': user.email,
            'business_name': business_profile.business_name,
            'country': business_profile.country,
            'address': business_profile.address,
            'address_zipcode': business_profile.address_zipcode,
            'address_city': business_profile.address_city,
            'business_description': business_profile.business_description,
            'newsletter': user.userprofile.newsletter,
        })

        return initial

    def get_success_url(self):
        return reverse('accounts:account_form')

    def form_valid(self, form):
        form.save(user=self.request.user)
        messages.add_message(self.request, messages.SUCCESS, _('Your details was saved successfully.'))
        return HttpResponseRedirect(self.get_success_url())


class SignupView(FormView):
    template_name = 'accounts/signup_form.html'
    form_class = SignupForm
    success_url = '/'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts:account_form'))
        else:
            return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SignupView, self).get_form_kwargs()
        kwargs['initial']['next'] = self.get_success_url()
        kwargs['initial']['agent_id'] = self.request.GET.get('a')
        return kwargs

    def get_success_url(self):
        next = self.request.REQUEST.get('next', None)
        if not next:
            next = self.request.META.get('HTTP_REFERER', None)
        if not next:
            next = self.success_url
        return urlparse(next).path

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class LoginView(FormView):
    template_name = 'accounts/login_form.html'
    form_class = LoginForm
    success_url = '/'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url(request))
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['initial']['next'] = self.get_success_url()
        return kwargs

    def get_success_url(self, request=None):
        if not request:
            request = self.request

        next_url = request.REQUEST.get('next', None) \
            or request.META.get('HTTP_REFERER', None) \
            or reverse('accounts:index')

        next_url = urlparse(next_url)

        if next_url.path and next_url.fragment:
            return u'{0}#{1}'.format(next_url.path, next_url.fragment)
        elif next_url.path:
            return next_url.path

    def form_valid(self, form):
        login(self.request, form.user)

        if form.cleaned_data.get('remember_me', False):
            self.request.session.set_expiry(2419200) # expire after 4 weeks
        else:
            self.request.session.set_expiry(0) # expire on browser close

        return super(LoginView, self).form_valid(form)


def logout_view(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'

    logout(request)
    return HttpResponseRedirect(urlparse(next).path)


@login_required
def index(request):
    return render(request, 'accounts/index.html')


class AgentDashboard(ListView):
    template_name = 'accounts/agent_index.html'
    paginate_by = 15
    model = Deal
    invite_form = None

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    @method_decorator(user_passes_test(lambda u: u.get_business_profile().is_agent))
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(AgentDashboard, self).dispatch(request, *args, **kwargs)

    def do_invite(self):
        self.invite_form = AgentInviteForm(request=self.request, data=self.request.POST)
        if self.invite_form.is_valid():
            self.invite_form.send_invite()
            return HttpResponseRedirect(reverse('accounts:agent_index'))

        return self.get(self.request)

    def do_invoice(self):
        form = AgentInvoiceForm(
            data=self.request.POST,
            user=self.request.user
        )
        if form.is_valid():
            invoice = form.make_invoice()
            return HttpResponseRedirect(invoice.get_absolute_url())
        else:
            return HttpResponseBadRequest()

    def get(self, request, *args, **kwargs):
        return super(AgentDashboard, self).get(request, *args, **kwargs)

    def post(self, request):
        self.request = request
        if request.POST.get('deals'):
            return self.do_invoice()
        elif request.POST.get('do_invite'):
            return self.do_invite()

        return HttpResponseRedirect(reverse('accounts:agent_index'))

    def get_queryset(self):
        self.form = AgentDealSearchForm(data=self.request.GET or None,
                                        businessprofile=self.request.user.get_business_profile())
        if self.form.is_valid():
            return self.form.search()
        else:
            return self.form.all()

    def get_context_data(self, **kwargs):
        data = super(AgentDashboard, self).get_context_data(**kwargs)
        data['search_form'] = self.form

        data['deal_agent_price_sum'] = deal_agent_price_sum(self.request.user.get_business_profile())
        data['invite_form'] = self.invite_form or AgentInviteForm(request=self.request)
        data['invoice_form'] = AgentInvoiceForm(user=self.request.user)
        return data


class MyAccountListView(ListView):
    template_name = 'accounts/index.html'
    paginate_by = 15
    model = Ad

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(MyAccountListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        bp = self.request.user.get_business_profile()
        queryset = Ad.objects.filter(active=True)
        group = self.kwargs.get('group', 'ads')
        type = self.kwargs.get('type', 'active')

        queryset = queryset.prefetch_related('deals')
        queryset = queryset.prefetch_related('images')
        queryset = queryset.select_related('currency')

        if group not in ('ads', 'deals'):
            raise Http404
        if type not in ('active', 'unpublished', 'completed', 'canceled'):
            raise Http404

        if group == 'ads':
            queryset = queryset.filter(owner=bp)
            queryset = queryset.annotate_deal_state_count('interested')
            queryset = queryset.annotate_deal_state_count('active')
            queryset = queryset.annotate_deal_state_count('completed')
            queryset = queryset.annotate_deal_state_count('canceled')

            if type == 'active':
                queryset = queryset.filter(published=True)
            elif type == 'unpublished':
                queryset = queryset.filter(published=False)
            elif type == 'completed':
                queryset = queryset.filter(deals__state='completed').distinct()
            elif type == 'canceled':
                raise Http404

        elif group == 'deals':
            queryset = queryset.filter(deals__owner=bp).distinct()
            if type == 'active':
                queryset = queryset.filter(deals__state__in=['interested', 'active'])
            elif type == 'cancelled':
                queryset = queryset.filter(deals__state='canceled')
            elif type == 'completed':
                queryset = queryset.filter(deals__state='completed')

        queryset = queryset.order_by('-last_deal_updated')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyAccountListView, self).get_context_data(**kwargs)
        context.update({
            'group': self.kwargs.get('group', 'ads'),
            'type': self.kwargs.get('type', 'active')
        })
        return context


@login_required
def switch_business_profile(request, business_profile_id):
    business_profile = get_object_or_404(BusinessProfile, id=business_profile_id,
                                         business_profiles__user_id=request.user.id)

    userprofile = request.user.get_userprofile()
    userprofile.active_profile_id = business_profile.id
    userprofile.save()

    return HttpResponseRedirect(reverse('accounts:index'))


@user_passes_test(has_active_business_profile)
def test_view(request):
    return HttpResponse("Success!")


def change_language(request, lang_code='en'):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'

    response = HttpResponseRedirect(next)
    if lang_code and translation.check_for_language(lang_code):
        if hasattr(request, 'session'):
            request.session['django_language'] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        if request.user.is_authenticated():
            up = request.user.get_userprofile()
            up.lang_code = lang_code
            up.save()

    return response
