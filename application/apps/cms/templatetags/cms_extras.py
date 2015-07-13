from django import template
from django.core.cache import cache
from django.core.urlresolvers import reverse
from application.apps.cms.models import Page, SliderPage

register = template.Library()


_pages_links_cache = []

@register.simple_tag(takes_context=True)
def pages_links(context):

    links = list()
    pages = _cached_pages()
    lang_code = context['LANGUAGE_CODE']

    for page in pages:
        if page.show_in_menu and page.active:
            anchor = '<li>%s</li>' % _page_link(page, lang_code)
            links.append(anchor)

    return ''.join(links)


@register.simple_tag(takes_context=True)
def page_link(context, page_slug):

    pages = _cached_pages()
    lang_code = context['LANGUAGE_CODE']
    for page in pages:
        if page.title_slug == page_slug:
            if page.active:
                return _page_link(page, lang_code)
            else:
                return ''
    return ''


@register.inclusion_tag('cms/slider.html', takes_context=True)
def frontpage_slider(context):
    return {
        'pages': SliderPage.objects.filter(active=True).select_related('image').order_by('order'),
        'LANGUAGE_CODE': context['LANGUAGE_CODE']
    }


def _cached_pages():
    pages = cache.get('pages_links')
    if not pages:
        pages = Page.objects.all()
        cache.set('pages_links', pages)
    return pages


def _page_link(page, lang_code):
    anchor_template = '<a href="%s">%s</a>'
    title = page.get_localized('title', lang_code)
    url = reverse('cms:page_view', kwargs={'slug': page.title_slug})
    return anchor_template % (url, title)



