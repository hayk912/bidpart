# -*- coding: utf-8 -*-
from application.apps.ads.templatetags.ads_extras import register

@register.simple_tag(takes_context=True)
def get_localized(context, obj, field=None):
    val = obj.get_localized(field, context['LANGUAGE_CODE'])
    if val is None:
        val = ''
    return val

@register.assignment_tag
def get_localized_formfield(form, fieldname, locale):
    return form['{0}_{1}'.format(fieldname, locale)]
