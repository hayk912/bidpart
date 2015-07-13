# coding=utf-8
from decimal import Decimal
import hashlib
from babel.support import Format
from currencies.models import Currency
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest
from django.utils import simplejson
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from application import settings
from application.apps.accounts.functions import has_active_business_profile
from application.apps.ads.paginator import AdsPaginator
from application.apps.deals.func import commission
from application.apps.deals.models import Deal
from http import TextareaJsonResponse
import forms
import models
from application.apps.deals.forms import CreateDealForm, DealForm


def show_buy_sell(request, show=None):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'

    if show in [b[0] for b in settings.SHOW_BUY_SELL]:
        request.session['show_buy_sell'] = show
    else:
        request.session['show_buy_sell'] = settings.SHOW_BUY_SELL_DEFAULT

    response = HttpResponseRedirect(next)

    return response


def get_product_type_fields(request, product_type, is_request=False):
    form = forms.AdForm(user=request.user, language_code=request.LANGUAGE_CODE,
                        initial={'product_type': product_type, 'is_request': is_request})
    return render(request, 'ads/ad_form_product_type_fields.html', {'form': form})


def get_product_types(request, product_category):
    product_category = int(product_category)
    if product_category > 0:
        form = forms.AdForm(user=request.user, language_code=request.LANGUAGE_CODE,
                            initial={'product_category': product_category})
    else:
        form = forms.AdForm(user=request.user, language_code=request.LANGUAGE_CODE)

    data = list()
    for key, value in form.fields['product_type'].choices:
        data.append({
            'key': key,
            'value': value
        })

    data = simplejson.dumps(data)
    return HttpResponse(data, mimetype='application/json')


class BaseIframeUploadView(CreateView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseIframeUploadView, self).dispatch(request, *args, **kwargs)

    def get_valid_json(self, form, instance):
        raise NotImplementedError()

    def get_invalid_json(self, form):
        raise NotImplementedError()

    def form_valid(self, form):
        if self.request.REQUEST['X-Requested-With'] == 'IFrame':
            instance = form.save()
            return TextareaJsonResponse(self.get_valid_json(form, instance), status=201)
        else:
            return HttpResponseBadRequest()

    def form_invalid(self, form):
        if self.request.REQUEST['X-Requested-With'] == 'IFrame':
            return TextareaJsonResponse(self.get_invalid_json(form), status=400)
        else:
            return HttpResponseBadRequest()


class AdImageCreateView(BaseIframeUploadView):
    form_class = forms.AdImageForm
    model = models.AdImage

    def get_form_kwargs(self):
        kwargs = super(AdImageCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_valid_json(self, form, instance):
        return {
            'pk': instance.pk,
            'list_thumb': instance.get_thumb('list_thumb')
        }

    def get_invalid_json(self, form):
        return {
            'errors': form.errors
        }


class AdFileCreateView(BaseIframeUploadView):
    form_class = forms.AdFileForm
    model = models.AdFile

    def get_form_kwargs(self):
        kwargs = super(AdFileCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_valid_json(self, form, instance):
        return {
            'pk': instance.pk,
            'filename': instance.get_url()
        }

    def get_invalid_json(self, form):
        return {
            'errors': form.errors
        }


class AdCreateView(CreateView):
    form_class = forms.AdForm
    model = models.Ad

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(AdCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AdCreateView, self).get_form_kwargs()
        kwargs['initial']['currency'] = self.request.session['currency'].pk
        kwargs['user'] = self.request.user
        kwargs['language_code'] = self.request.LANGUAGE_CODE
        return kwargs


class GetBidpartProvisionView(View):
    def get(self, request):
        commission_sum = 0
        price = request.GET.get('price') or 0
        currency_id = request.GET.get('currency')

        if currency_id:
            commission_sum = commission(
                request.user.get_business_profile(),
                Decimal(price),
                Currency.objects.get(pk=currency_id)
            )

        return HttpResponse(simplejson.dumps({
            'commission': Format(request.LANGUAGE_CODE).currency(commission_sum, 'EUR')
        }), content_type='application/json')


class AdUpdateView(UpdateView):
    form_class = forms.AdForm
    model = models.Ad

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(AdUpdateView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(AdUpdateView, self).get_queryset().filter(active=True)

    def get_object(self, queryset=None):
        object = super(AdUpdateView, self).get_object(queryset)
        if self.request.user.has_perm('change_ad', object):
            return object
        else:
            raise PermissionDenied(_('Permission denied'))

    def get_form_kwargs(self):
        kwargs = super(AdUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['language_code'] = self.request.LANGUAGE_CODE
        return kwargs


class AdDeleteView(DeleteView):
    success_url = reverse_lazy('ads:ad_success_delete')
    model = models.Ad

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(AdDeleteView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def get_object(self, queryset=None):
        ad = super(AdDeleteView, self).get_object(queryset)
        if ad.owner.pk != self.request.user.get_business_profile().pk:
            raise Http404
        return ad

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AdView(DetailView):
    object = None
    template_name = 'ads/ad_detail.html'
    url_keys = ('business_domain', 'product_category', 'product_type')

    def dispatch(self, request, *args, **kwargs):
        if not set(kwargs.keys()).intersection((self.pk_url_kwarg, self.slug_url_kwarg)):
            kwargs[self.pk_url_kwarg] = args[-1]

        return super(AdView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not self.object:
            self.object = super(AdView, self).get_object(queryset)
            self.object.num_views += 1
            self.object.save()

        return self.object

    def get_queryset(self):
        queryset = models.Ad.objects.filter(active=True)
        queryset = queryset.select_related('owner')

        queryset = queryset.prefetch_related('value_set__field')
        queryset = queryset.prefetch_related('value_set__choice_value')
        queryset = queryset.prefetch_related('deals__creator__user')
        queryset = queryset.prefetch_related('files')
        queryset = queryset.prefetch_related('images')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AdView, self).get_context_data(**kwargs)
        context['filter_form'] = forms.AdsFilter(language_code=self.request.LANGUAGE_CODE, data=self.get_form_kwargs())
        try:
            is_owner = self.request.user.get_business_profile().pk == self.object.owner.pk
        except AttributeError:
            is_owner = False

        context['more_ads'] = self.more_ads()

        if self.request.user.has_perm('change_ad', self.object):
            context['can_update_ad'] = True

        if not self.request.user.is_authenticated():
            context['create_deal_login_first'] = True # Logga in och vidarebefodra tillbaka hit.
        elif not is_owner:
            if self.object.deals.filter(
                    owner=self.request.user.get_business_profile()).exists(): # Finns det en deal mellan ägare och user redan?
                context['has_deal_already'] = True # Visa att man redan har skapat en deal.
            else:
                context['create_deal_form'] = CreateDealForm(user=self.request)

        if is_owner:
            context['deals'] = Deal.objects.filter(ad=self.object)

        if self.request.user.is_authenticated() and is_owner:
            if self.object.deals.count():
                context['update_deal_forms'] = []
                for deal in self.object.deals.all():
                    if deal.state == 'interested':
                        context['update_deal_forms'].append((
                            'deals/deal_activate_deal_modal.html', DealForm(user=self.request.user, instance=deal),
                            deal)) # Activate deal
                    elif deal.state == 'active':
                        context['update_deal_forms'].append((
                            'deals/deal_extend_deal_modal.html', DealForm(user=self.request.user, instance=deal),
                            deal)) # Extend time
                        context['update_deal_forms'].append((
                            'deals/deal_cancel_deal_modal.html', DealForm(user=self.request.user, instance=deal),
                            deal)) # Cancel deal
                        context['update_deal_forms'].append((
                            'deals/deal_complete_deal_modal.html', DealForm(user=self.request.user, instance=deal),
                            deal)) # Complete deal

        return context

    def more_ads(self):
        queryset = forms.AdsFilter(language_code=self.request.LANGUAGE_CODE).all()
        queryset = queryset.exclude(pk=self.object.pk)
        queryset = queryset.filter(owner=self.object.owner)
        queryset = queryset.order_by('-created')

        cache_key = 'more_ads_%s' % self.object.pk
        cache_ = cache.get(cache_key)
        if cache_:
            more_ads = cache_
        else:
            cache.set(cache_key, queryset[0:10], 30 * 60)
            more_ads = queryset[0:10]

        return more_ads

    def get_form_kwargs(self):
        form_data = dict()
        ad_values = {
            'business_domain': [bd.slug for bd in self.object.business_domains.all()],
            'product_category': [cat.slug for cat in self.object.product_type.product_categories.all()],
            'product_type': self.object.product_type.slug
        }

        form_data['to_currency'] = self.request.session['currency']

        # reset session if ad does not match what's in the session
        for key in self.url_keys:
            try:
                if not self.request.session[key] in ad_values[key]:
                    del self.request.session[key]
            except KeyError:
                pass

        # set the form data with the session so we keep the navigation
        for key in self.url_keys:
            try:
                form_data[key] = self.request.session[key]
            except KeyError:
                pass

        return form_data or None


class AdsListView(ListView):
    template_name = 'ads/ad_list.html'
    url_keys = ('business_domain', 'product_category', 'product_type')
    paginate_by = 20
    #paginator_class = Paginator

    def get_form_kwargs(self):
        kwargs = dict()
        kwargs['data'] = self.request.GET.dict()
        kwargs['data']['to_currency'] = self.request.session['currency']
        kwargs['data']['show_buy_sell'] = self.request.session['show_buy_sell']

        kwargs['language_code'] = self.request.LANGUAGE_CODE

        # clean out the session-based navigation so we always start from a clean state on each page-view
        for key in self.url_keys:
            try:
                del self.request.session[key]
            except KeyError:
                pass

        for i, val in enumerate(self.args):
            self.request.session[self.url_keys[i]] = val  # keep sidebar-navigation on a single ad-view
            kwargs['data'][self.url_keys[i]] = val

        return kwargs or None

    def get_queryset(self):
        self.form = forms.AdsFilter(**self.get_form_kwargs())

        if self.form.is_valid():
            return self.form.filter()
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(AdsListView, self).get_context_data(**kwargs)
        context['filter_form'] = self.form

        # only show featured and the carousel on the first page.
        if len(self.args) == 0:
            featured = models.Ad.objects.featured()

            if self.request.session['show_buy_sell'] == 'sell':
                featured = featured.filter(is_request=False)
            elif self.request.session['show_buy_sell'] == 'buy':
                featured = featured.filter(is_request=True)

            context['featured_ads'] = featured[0:5]
            context['show_slider'] = True

        return context
