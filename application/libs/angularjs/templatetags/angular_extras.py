from datetime import datetime
from django import template
from django.db.models import Model
from django.forms import BaseForm, Field
from django.forms.forms import BoundField
import simplejson

register = template.Library()


@register.filter
def ng_init(value):
    def serialize(obj):
        data = dict()

        if isinstance(obj, BaseForm):
            data['fields'] = dict()
            for field in obj:
                data['fields'][field.html_name] = serialize(field)

        elif isinstance(obj, (Field, BoundField)):
            value = obj.value()

            if value is None:
                value = ''
            elif isinstance(value, bool):
                value = int(value)
            elif isinstance(value, Model):
                value = value.pk

            data['value'] = value

            if hasattr(obj.field, 'choices'):
                data['choices'] = list()
                for key, value in obj.field.choices:
                    choice = {
                        'key': unicode(key),
                        'value': unicode(value)
                    }
                    data['choices'].append(choice)

        elif isinstance(obj, (dict, list)):
            data = obj

        return data

    out = ''
    data = serialize(value)
    for key in data:
        out += '%s=%s; ' % (key, simplejson.JSONEncoderForHTML().encode(data[key]))

    return out
