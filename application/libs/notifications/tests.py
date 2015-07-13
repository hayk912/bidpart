from django.test import TestCase
from application.apps.accounts.models import BusinessProfile
from models import Notification, NotificationSetting
from django.contrib.auth.models import User
from django.test import Client
from django.core.urlresolvers import NoReverseMatch
from django.core import mail
from application.backends import BallouSMSBackend
import sendsms


class SimpleTest(TestCase):

    profile = None
    user = None

    def setUp(self):
        self.user = User.objects.create_user('testname', 'test@tester.se')
        userprofile = self.user.get_profile()

        self.profile = BusinessProfile.objects.create(
            creator = userprofile,
            address = 'Testroad 123',
            address_zipcode = '123 45',
            address_city = 'City of Tests'
        )

        userprofile.business_profiles.add(self.profile)
        userprofile.save()

    def test_add_notification(self):
        notifs = Notification.objects.create(
            profile=self.profile,
            message='The message goes here',
            uri='ads:ad',
            params={'ad_id': 1}
        )

        self.failUnless(len(notifs) > 0)

        for notif in notifs:
            db_notif = Notification.objects.get(pk=notif.pk)

            self.failUnless(db_notif.pk == notif.pk)
            self.failUnless(db_notif.message == notif.message)
            self.failUnless(db_notif.user == notif.user)
            self.failUnless(db_notif.uri == notif.uri)
            self.failUnless(db_notif.params == notif.params)

    def test_unread_notifications(self):
        notifications = []
        for x in range(5):
            notifs = Notification.objects.create(
                profile=self.profile,
                message='The message goes here',
                uri='ads:ad',
                params={'ad_id': x + 1}
            )
            notifications.extend(notifs)

        client = Client()

        for notification in notifications[:3]:
            try:
                client.get(notification.get_absolute_url())
            except NoReverseMatch:
                pass

        self.failUnless(Notification.objects.filter(is_read=True).count() == 3)
        self.failUnless(Notification.objects.filter(is_read=False).count() == 2)

    def test_notification_settings(self):
        self.user.userprofile.cellphone = '0701234567'
        self.user.userprofile.save()

        self.failUnless(self.user.notification_settings.count() > 0)

        for setting in self.user.notification_settings.all():
            setting.email = True
            setting.sms = True
            setting.save()

        Notification.objects.create(
            profile=self.profile,
            message='The message goes here',
            uri='ads:ad',
            params={'ad_id': 1}
        )

        self.failUnless(Notification.objects.count() > 0)

        for notif in Notification.objects.all():
            settings = NotificationSetting \
                .objects.setting_for_notification(notif)

            self.assertEqual(notif.did_email, settings.email)
            self.assertEqual(notif.did_sms, settings.sms)

        self.failUnless(len(mail.outbox) > 0)
        self.failUnless(len(sendsms.outbox) > 0)

    def test_parse_ballou(self):
        expected_result = """<?xml version="1.0" encoding="ISO-8859-1"?>
            <!DOCTYPE ballou_sms_response PUBLIC "-//ballou//SMS Response DTD//EN" "http://sms2.ballou.se/dtd/ballou_sms_response.dtd">
            <ballou_sms_response>
                <response type="status"><message id="248217214242" to_msisdn="0701234567" status="-1" error="0"/></response>
            </ballou_sms_response>"""

        backend = BallouSMSBackend()
        status = backend.parse_response(expected_result)

        self.failUnless(status['to'] == '0701234567')
        self.failUnless(status['status'] == '-1')
        self.failUnless(status['error'] == '0')
        self.failUnless(status['id'] == '248217214242')
