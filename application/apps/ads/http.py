from django.core import serializers
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson

class TextareaJsonResponse(HttpResponse):


    def __init__(self, content='', mimetype=None, status=None, content_type=None):
        super(TextareaJsonResponse, self).__init__(content, mimetype, status, content_type)

        if isinstance(content, QuerySet):
            json = serializers.serialize('json', content)
        else:
            json = simplejson.dumps(content)
        self.content = '<textarea data-status="%i">%s</textarea>' % (self.status_code, json)

