# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import title
from django.utils.functional import Promise
from application import settings

DEFAULT_FIELD = ('CharField', {
    'max_length': 64,
    'default': '',
    'blank': True
})


def locale_model(fields):
    if not isinstance(fields, (list, tuple, dict)):
        fields = [fields]

    class Meta:
        abstract = True

    def get_localized(obj, field, lang_code):
        field_name = '%s_%s' % (field, lang_code)
        value = getattr(obj, field_name, '')
        if not value:
            for lang_code, lang_name in settings.LANGUAGES:
                field_name = '%s_%s' % (field, lang_code)
                value = getattr(obj, field_name)
                if value:
                    return value
        else:
            return value

    attributes = {
        '__module__': 'application.apps.locale.models',
        'Meta': Meta,
        'get_localized': get_localized
    }

    # normalize to a dict.
    fields_dict = {}
    if not isinstance(fields, dict):
        for attr_name in fields:
            fields_dict[attr_name] = DEFAULT_FIELD
    else:
        fields_dict = fields

    for attr_name, field in fields_dict.iteritems():
        # A field for every language.
        for lang in settings.LANGUAGES:
            if isinstance(field[1].get('verbose_name'), Promise):
                verbose_name = field[1].get('verbose_name')
            elif field[1].get('verbose_name') is not None:
                verbose_name = '%s (%s)' % (field[1]['verbose_name'], lang[0])
            else:
                verbose_name = '%s (%s)' % (title(attr_name), lang[0])
                verbose_name = verbose_name.replace('_', ' ')

            attrs = field[1].copy()
            attrs['verbose_name'] = verbose_name

            attributes['%s_%s' % (attr_name, lang[0])] = getattr(models, field[0])(**attrs)

    return type('LocaleModel', (models.Model,), attributes)
