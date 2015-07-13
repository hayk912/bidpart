from django import template

register = template.Library()


@register.filter
def get_allowed_questions(obj, authed):
    if authed:
        return obj.all()
    else:
        return obj.filter(only_logged_in=0)
