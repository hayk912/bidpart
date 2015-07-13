# -*- coding: utf-8 -*-
from application import settings


def show_buy_cell(request):
    if not request.session.get('show_buy_sell'):
        request.session['show_buy_sell'] = settings.SHOW_BUY_SELL_DEFAULT

    to_show = None
    for show in settings.SHOW_BUY_SELL:
        if show[0] == request.session['show_buy_sell']:
            to_show = show

    return {
        'SHOW_BUY_SELL_CHOICES': settings.SHOW_BUY_SELL,
        'SHOW_BUY_SELL_ACTIVE': to_show
    }

