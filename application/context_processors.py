def settings(request):
    from django.conf import settings
    context = {
        'settings': settings
    }

    return context
