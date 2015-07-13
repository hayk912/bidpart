from urlparse import urljoin
from django import template
from django.templatetags.static import PrefixNode
from application import settings
from application.apps.files.models import SiteFile

register = template.Library()

@register.simple_tag
def get_thumb(image, thumb_format):
    try:
        thumb = image.get_thumb(thumb_format=thumb_format)
    except AttributeError:
        thumb =  ''

    if thumb:
        return thumb
    else:
        for default_thumb in settings.IMAGE_THUMB_DEFAULTS:
            if default_thumb[0] == thumb_format:
                return urljoin(PrefixNode.handle_simple("STATIC_URL"), default_thumb[1])

    return ''

@register.simple_tag
def sitefile(key, locale_code=None):
    if locale_code is not None:
        key += '_' + locale_code
    try:
        file = SiteFile.objects.get(file_key=key)
    except (SiteFile.MultipleObjectsReturned, SiteFile.DoesNotExist):
        return ''

    return file.get_absolute_url()

