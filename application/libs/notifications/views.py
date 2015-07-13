from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from models import Notification


def goto(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    notification.is_read = True
    notification.save()

    return HttpResponseRedirect(reverse(notification.uri, kwargs=notification.params))


def detail(request, notification_id):
    return HttpResponse('A notification object')
