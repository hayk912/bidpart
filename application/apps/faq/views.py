from django.shortcuts import render_to_response
from django.template import RequestContext
from models import FAQGroup, FAQQuestion


def index(request):
    logged_in = request.user.is_authenticated()
    if not logged_in:
        questions = FAQQuestion.objects.filter(only_logged_in=0)
    else:
        questions = FAQQuestion.objects.all()
    groups = FAQGroup.objects.all()
    return render_to_response('faq/index.html',
                          {'groups': groups,
                          'questions': questions,
                          },
                          context_instance=RequestContext(request))
