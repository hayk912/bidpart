# coding=utf-8
from datetime import timedelta
from decimal import Decimal, Context
from currencies.utils import convert as convert_price
from django.utils import timezone
from application import settings
from application.apps.accounts.models import BusinessProfile
from application.apps.deals.models import Deal
from django.db.models import Sum


def deal_price_sum(businessprofile):
    deal_price_eur__sum = Deal.objects.filter(
        state='completed',
        ad__owner=businessprofile
    ).aggregate(Sum('price_eur'))['price_eur__sum']

    if deal_price_eur__sum is None:
        deal_price_eur__sum = 0
    return deal_price_eur__sum


def deal_agent_price_sum(businessprofile):
    return Deal.objects.filter(
        state='completed',
        payed_to_agent=True,
        ad__owner__agent=businessprofile
    ).aggregate(Sum('agent_commission'))['agent_commission__sum'] or 0


def commission_level(businessprofile=None, deal_price_eur__sum=None, levels=None):
    if deal_price_eur__sum is None and businessprofile:
        if businessprofile.is_agent:
            deal_price_eur__sum = deal_agent_price_sum(businessprofile)
        else:
            deal_price_eur__sum = deal_price_sum(businessprofile)

    level = 0
    if levels is None:
        if businessprofile and businessprofile.is_agent:
            levels = list(settings.AGENT_COMMISSION_LEVELS)
        else:
            levels = list(settings.COMMISSION_LEVELS)
    percent = 1

    for i, price_perc in enumerate(levels):
        price, perc = price_perc
        if deal_price_eur__sum >= price:
            level = i
            percent = perc
        else:
            break

    return level, Decimal('%.2f' % percent)


# calculates the commission, you put in a price for the item, a total sum
# of what's sold before and the commission ladder/levels
def calc_commission(price, total_sum, levels):
    level, perc = commission_level(deal_price_eur__sum=total_sum, levels=levels)
    commission_sum = 0
    price_left = price

    # slices prices to be able to calculate the ranges of commisssion later on.
    limits = []
    # fill the limits.
    for i, l in enumerate(levels):
        # the last level is infinitly high so there we place whats left.
        if i + 1 >= len(levels):
            limits.append(price_left)
            break

        # interval start/stop ex. 0 - 10 000
        price_start = Decimal(levels[i][0])
        price_limit = Decimal(levels[i + 1][0])

        if price_left > 0:
            if i < level:
                # don't pay any commission below the current level
                limits.append(0)
            else:
                # slice the price at correct places to be calclulated seperatly later on.
                cut = min(price_limit - price_start, price_left, price_limit - total_sum)
                price_left -= cut
                limits.append(cut)
        else:
            break

    # calculate the different commissions for different levels.
    for i, limit in enumerate(limits):
        commission_sum += limit * Decimal('%.2f' % levels[i][1])

    if commission_sum < settings.MINIMUM_COMMISSION:
        commission_sum = settings.MINIMUM_COMMISSION
    return Decimal('%.2f' % commission_sum)


def commission(businessprofile, price, currency):
    price = convert_price(price, currency.code, 'EUR')

    if businessprofile.commission_override:
        return businessprofile.commission_override * price

    deal_price_eur__sum = deal_price_sum(businessprofile)
    levels = list(settings.COMMISSION_LEVELS)

    return calc_commission(price, deal_price_eur__sum, levels)


def agent_commission(agent, bidpart_commission, currency):
    bidpart_commission = convert_price(bidpart_commission, currency.code, 'EUR')

    reqruits = BusinessProfile.objects.filter(
        agent_id=agent.pk,
        creator__user__date_joined__gte=timezone.now() - timedelta(days=365)
    )

    if reqruits.exists():
        agent_commission_sum = deal_agent_price_sum(agent)
    else:
        agent_commission_sum = 0

    levels = list(settings.AGENT_COMMISSION_LEVELS)

    return calc_commission(bidpart_commission, agent_commission_sum, levels)
