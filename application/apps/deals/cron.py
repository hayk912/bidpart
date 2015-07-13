# coding=utf-8
from django.utils import timezone
import math
import datetime
from django.conf import settings
import subprocess
import threading
from sendsms.api import send_sms

from application.apps.deals.models import Deal


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()


def remind():
    timestamp = timezone.now() - datetime.timedelta(days=7)

    deals = Deal.objects.filter(
        state='active',
        last_reminder__lte=timestamp,
        renewed__lte=timestamp
    )

    for deal in deals:
        renewed_delta_weeks = math.floor((timezone.now() - deal.renewed).total_seconds() / (86400 * 7))

        if renewed_delta_weeks >= 7:
            deal.do_action(deal.COMPLETE)
        else:
            if renewed_delta_weeks >= 6:
                mobile = deal.ad.creator.phone
                lang_code = deal.ad.creator.lang_code or settings.LANGUAGE_CODE
                ad_title = deal.ad.get_localized('title', lang_code)
                if mobile:
                    message = u'www.bidpart.se saknar svar på påminnelse gällande %s till %s. Om inte svar inkommer inom 7 dagar skickas en provitionsfaktura enligt avtal.' % (ad_title, deal.creator.user.get_full_name())
                    message = message.encode('iso-8859-1')
                    send_sms(body=message, from_phone='Bidpart AB', to=[mobile])

                deal.send_mail('reminder')
            elif renewed_delta_weeks >= 3:
                deal.send_mail('reminder')

        deal.last_reminder = timezone.now()
        deal.save()
