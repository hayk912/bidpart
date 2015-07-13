from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, TemplateView
from application.apps.interest.forms import InterestForm
from application.apps.interest.models import Interest


class InterestCreateView(CreateView):
    model = Interest
    form_class = InterestForm
    success_url = reverse_lazy('interest:success')

    def form_valid(self, form):

        return super(InterestCreateView, self).form_valid(form)


class InterestSuccess(TemplateView):
    template_name = 'interest/interest_success.html'
