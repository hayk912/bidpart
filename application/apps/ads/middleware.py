# -*- coding: utf-8 -*-
from application import settings

class BuySellMiddleware(object):

    def process_request(self, request):
        if not request.session.get('show_buy_sell'):
            request.session['show_buy_sell'] = settings.SHOW_BUY_SELL_DEFAULT
