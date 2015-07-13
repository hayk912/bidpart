from decimal import Decimal, ROUND_UP
from babel.support import Format
from django import template
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.utils.translation import ugettext
from currencies.models import Currency
from django.utils.formats import localize
from application.apps.ads.forms import AdsFilter

register = template.Library()


@register.inclusion_tag('ads/ad_header_search.html', takes_context=True)
def header_search(context, form_data=None):
    return {
        'form': AdsFilter(form_data, language_code=context['LANGUAGE_CODE'])
    }


@register.inclusion_tag('ads/ad_list_sidebar.html')
def ad_filter_sidebar(form):

    fields = ['business_domain', 'product_category', 'product_type']
    all_strings = [ugettext('All business domains'), ugettext('All product categories'),
        ugettext('All product types')]
    all_string = None
    back_args = []
    url_args = []
    field = None

    for i, field in enumerate(fields):
        all_string = all_strings[i]
        url_args = [form[f].value() for f in fields[0:i]]
        if url_args:
            back_args = url_args[0:-1]
        if not form[field].value():
            break

    choices = []
    for choice in form.fields[field].choices:
        choices.append({
            'value': choice[0],
            'label': choice[1],
            'url': reverse('ads:ad_filter', args=url_args + [choice[0]]),
        })

    return {
        'form': form,
        'field': field,
        'choices': choices,
        'active_value': form[field].value,
        'back_url': reverse('ads:ad_filter', args=back_args),
        'all_url': reverse('ads:ad_filter', args=url_args),
        'all_string': all_string
    }

@register.simple_tag
def order_by_link(title, column, form):
    order_by = form['order_by'].value() or form.order_by_default_field
    title = ugettext(title)

    if not column in order_by:
        order_by = column
        tag_class = ''
    elif order_by[0] == '-':
        order_by = order_by[1:]
        tag_class = 'desc'
    else:
        order_by = '-' + order_by
        tag_class = 'asc'

    url = form.get_absolute_url(kwargs={'order_by': order_by})
    return '<a href="%s" class="%s">%s</a>' % (url, tag_class, title)

@register.simple_tag(takes_context=True)
def price(context, amount, from_currency, classes='', convert=True):
    if amount > 0:
        if not isinstance(from_currency, Currency):
            from_currency = Currency.objects.get(code__exact=from_currency)
        to_currency = context['CURRENCY']

        if convert:
            price = convert_price(amount, from_currency, context['CURRENCY'])
        else:
            to_currency = from_currency
            price = amount

        price = Format(context['LANGUAGE_CODE']).currency(price, to_currency.code)
        title = ugettext('Actual price: %(amount)s %(currency)s') % {
            'amount': localize(amount),
            'currency': from_currency
        }
        if convert:
            show_tooltip = from_currency.code != to_currency.code
        else:
            show_tooltip = False
    else:
        price = ugettext('Offer desired')
        title = ugettext('No price is set, please leve an offer.')
        show_tooltip = True

    if show_tooltip:
        return '<a href="#" class="%s" rel="tooltip" data-title="%s">%s</a>' % (classes, title, price)
    else:
        return '<span class="%s">%s</span>' % (classes, price)


def convert_price(amount, from_currency, to_currency):
    if from_currency.code == to_currency.code:
        return amount
    amount = Decimal(amount)
    amount = amount * (to_currency.factor / from_currency.factor)
    return amount.quantize(Decimal("0.01"), rounding=ROUND_UP)


@register.simple_tag
def filter_href(field_key, value, form):
    if value == form.data.get(field_key, None):
        value = None

    href = form.get_absolute_url({
        field_key: value
    })
    return href


@register.simple_tag(takes_context=True)
def append_to_get(context, key, value):
    params = context['request'].GET.copy()
    params[key] = value
    return params.urlencode()


@register.simple_tag
def selected_class(field_key, choice, form):
    if choice == form.data.get(field_key, None):
         return 'selected'
    else:
        return ''


@register.inclusion_tag('ads/pagination.html', takes_context=True)
def pagination(context, tot_pages=10):
    current_page = context['page_obj'].number
    page_range = context['paginator'].page_range

    before_current = page_range[0:current_page]
    after_current = page_range[current_page:len(page_range)]

    if len(before_current) < len(after_current):
        before_current = before_current[-(tot_pages / 2):-1]
        after_current = after_current[0:tot_pages - len(before_current)]
    else:
        after_current = after_current[0:(tot_pages / 2) +1]
        before_current = before_current[-(tot_pages - len(after_current)):-1]

    context['pages'] = before_current + [current_page] + after_current

    return context
