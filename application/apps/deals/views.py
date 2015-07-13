from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
import models
from django.http import HttpResponse, HttpResponseBadRequest
import forms
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from application.apps.accounts.functions import has_active_business_profile


class DealsCreateView(CreateView):
    model = models.Deal
    form_class = forms.CreateDealForm

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    def dispatch(self, *args, **kwargs):
        return super(DealsCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = super(DealsCreateView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })

        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax():
            response_data = {
                'success': True
            }

            return HttpResponse(json.dumps(response_data), mimetype='application/json')

        return super(DealsCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            response_data = {
                'success': False,
                'errors': form.errors
            }

            return HttpResponseBadRequest(json.dumps(response_data), mimetype='application/json')

        return super(DealsCreateView, self).form_invalid(form)


class DealsUpdateView(UpdateView):
    model = models.Deal
    http_method_names = ['post']
    form_class = forms.DealForm

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: has_active_business_profile(u)))
    def dispatch(self, *args, **kwargs):
        return super(DealsUpdateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(DealsUpdateView, self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user,
            'instance': self.object
        })
        return kwargs

    def get_object(self, queryset=None):
        object = super(DealsUpdateView, self).get_object(queryset)
        if self.request.user.has_perm('change_deal', object):
            return object
        else:
            raise PermissionDenied

    def form_valid(self, form):
        form.save()
        if self.request.is_ajax():
            response_data = {
                'success': True
            }

            return HttpResponse(json.dumps(response_data), mimetype='application/json')

        return super(DealsUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():

            response_data = {
                'success': False,
                'errors': form.errors
            }

            return HttpResponseBadRequest(json.dumps(response_data), mimetype='application/json')

        return super(DealsUpdateView, self).form_invalid(form)


class DashboardListView(ListView):
    template_name = 'dashboard/dashboard_index.html'

    def get_queryset(self):
        queryset = models.Deal.objects
        queryset = queryset.select_related('ad')

        if self.kwargs:
            return queryset.filter(state=self.kwargs['state'])
        else:
            return queryset.all()
