from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, TemplateView
from application.apps.edr.forms import OptOutForm
from application.apps.edr.models import OptOut


class EdrOptoutView(CreateView):
    model = OptOut
    form_class = OptOutForm
    success_url = reverse_lazy('edr:success')


class EdrOptOutSuccess(TemplateView):
    template_name = 'edr/optout_success.html'
