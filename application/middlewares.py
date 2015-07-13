from currencies.models import Currency


class CurrencyMiddleware(object):

    def process_request(self, request):
        if not request.session.get('currency'):
            request.session['currency'] = Currency.objects.get(is_default__exact=True)


class UpdateLocaleMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            if request.LANGUAGE_CODE != request.user.get_userprofile().lang_code:
                request.user.get_userprofile().lang_code = request.LANGUAGE_CODE
                request.user.get_userprofile().save()
