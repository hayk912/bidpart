from urlparse import urljoin
from django import template
from django.templatetags.static import PrefixNode
from application.apps.accounts.models import AgentDataCache, ProfileDataCache
from application.apps.deals.models import Deal
from application.apps.ads.models import Ad
from django.db.models import Count
from django.conf import settings
from application.apps.deals.func import commission_level, deal_price_sum, calc_commission as func_calc_commission, deal_agent_price_sum

register = template.Library()


@register.inclusion_tag('accounts/sidebar.html', takes_context=True)
def accounts_sidebar(context, *args, **kwargs):
    request = context['request']
    bp = request.user.get_business_profile()

    ads_active_count = Ad.objects.filter(owner=bp, published=True).count()
    ads_unpublished_count = Ad.objects.filter(owner=bp, published=False).count()
    ads_completed_count = Ad.objects.filter(owner=bp, deals__state='completed').distinct().count()

    deals_state = Deal.objects.filter(owner=bp).values('state').annotate(dcount=Count('state'))

    deals_state = dict([(s['state'], s['dcount']) for s in deals_state])

    deals_active_count = int(deals_state.get('active', 0)) + int(deals_state.get('interested', 0))
    deals_cancelled_count = deals_state.get('canceled', 0)
    deals_completed_count = deals_state.get('completed', 0)

    group = kwargs.get('group', context.get('group'))
    type = kwargs.get('type', context.get('type'))

    return {
        'request': request,
        'group': group,
        'type': type,

        'ads_active_count': ads_active_count,
        'ads_unpublished_count': ads_unpublished_count,
        'ads_completed_count': ads_completed_count,

        'deals_active_count': deals_active_count,
        'deals_cancelled_count': deals_cancelled_count,
        'deals_completed_count': deals_completed_count,
    }


def level_progress(commission_levels, current_level_i, total_price):

    current_level_sum = commission_levels[current_level_i][0]
    current_level_perc = commission_levels[current_level_i][1]

    # make sure we are not at the max level
    if current_level_i < len(commission_levels) - 1:
        # how many percent to next level.
        next_level_sum = commission_levels[current_level_i + 1][0]
        next_level_perc = commission_levels[current_level_i + 1][1]

        total_range = next_level_sum - current_level_sum
        progress_amount = total_price - current_level_sum

        current_commission_level = {
            'amount': current_level_sum,
            'perc': '%.2g' % (current_level_perc * 100),
            'progress': (progress_amount / total_range) * 100,
            'amount_left': total_range - progress_amount
        }
        next_commission_level = {
            'amount': next_level_sum,
            'perc': '%.2g' % (next_level_perc * 100),
        }

    else: # we are at max level, fill the bar to the max.
        current_commission_level = {
            'amount': current_level_sum,
            'perc': '%.2g' % (current_level_perc * 100),
            'progress': 100,
            'amount_left': '~'
        }
        next_commission_level = {
            'amount': '~',
            'perc': '%.2g' % (current_level_perc * 100),
        }

    return current_commission_level, next_commission_level


@register.simple_tag
def calc_agent_commission(bidpart_commission, total_agent_commission):
    return func_calc_commission(bidpart_commission, total_agent_commission, settings.AGENT_COMMISSION_LEVELS)

@register.inclusion_tag('accounts/agent_dashboard.html', takes_context=True)
def agent_accounts_dashboard(context):
    request = context['request']
    bp = request.user.get_business_profile()
    data, created = AgentDataCache.objects.get_or_create(businessprofile__pk=bp.pk)

    commission_levels = settings.AGENT_COMMISSION_LEVELS
    deal_price_eur__sum = deal_agent_price_sum(bp)
    current_level_i, perc = commission_level(deal_price_eur__sum=deal_price_eur__sum, levels=commission_levels)

    current_commission_level, next_commission_level = level_progress(commission_levels, current_level_i,
                                                                     deal_price_eur__sum)

    return {
        'request': request,
        'num_recruited': data.num_recruited,
        'num_sold_products': data.num_sold_products,
        'num_interested': data.num_interested,
        'num_active': data.num_active,
        'num_completed': data.num_completed,
        'num_canceled': data.num_canceled,
        'next_commission_level': next_commission_level,
        'current_commission_level': current_commission_level
    }


@register.inclusion_tag('accounts/dashboard.html', takes_context=True)
def accounts_dashboard(context):
    request = context['request']
    bp = request.user.get_business_profile()
    data, created = ProfileDataCache.objects.get_or_create(businessprofile__pk=bp.pk)

    commission_levels = settings.COMMISSION_LEVELS
    current_level_i, perc = commission_level(bp)
    deal_price_eur__sum = deal_price_sum(bp)

    current_commission_level, next_commission_level = level_progress(commission_levels, current_level_i,
                                                                     deal_price_eur__sum)

    if bp.commission_override:
        current_commission_level['perc'] = '%.2g' % (bp.commission_override * 100)

    return {
        'request': request,
        'total_views': data.num_ads_views,
        'total_active_ads': data.num_ads,
        'total_sold_products': data.num_sold_products,
        'next_commission_level': next_commission_level,
        'current_commission_level': current_commission_level
    }


@register.inclusion_tag('accounts/sidebar_commission_levels.html', takes_context=True)
def commission_levels(context, levels=None):
    request = context['request']
    bp = request.user.get_business_profile()
    current_level, perc = commission_level(bp)

    if levels is None:
        levels = settings.COMMISSION_LEVELS

    commission_levels = list()
    for i, level in enumerate(levels):
        min, perc = level
        if i < len(levels) - 1:
            max, next_perc = levels[i + 1]
        else:
            max = '~'

        commission_levels.append({
            'percent': '%.2g' % (perc * 100),
            'min': min,
            'max': max,
            'level': i,
        })

    return {
        'current_level': current_level,
        'commission_levels': commission_levels
    }

@register.simple_tag
def flag(country_code):
    filename = ''
    for flag in getattr(settings, 'FLAGS'):
        if flag[0] == country_code:
            filename = flag[1]

    path = getattr(settings, 'FLAGS_ROOT') + filename
    return urljoin(PrefixNode.handle_simple("STATIC_URL"), path)
