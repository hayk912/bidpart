from django.views.generic import DetailView
from models import Page


class PageView(DetailView):
    slug_field = 'title_slug'
    template_name = 'cms/page_detail.html'
    model = Page
