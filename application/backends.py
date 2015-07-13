from django.contrib.auth.models import User
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
from django.core.validators import email_re
from sendsms.backends.base import BaseSmsBackend
from django.conf import settings
from xml.dom import minidom
import requests
import os
import binascii


class RedirectEmailBackend(SMTPEmailBackend):
    def send_messages(self, email_messages_):
        email_messages = []
        for email_message in email_messages_:
            email_message.cc = []
            email_message.bcc = []
            email_message.to = [admin[1] for admin in settings.ADMINS]
            email_messages.append(email_message)

        return super(RedirectEmailBackend, self).send_messages(email_messages)


class ObjectPermsBackend(object):

    def authenticate(self, username=None, password=None):
        # This backend does not authenticate a user so let another backend do that.
        return None

    def has_perm(self, user_obj, perm, obj=None):
        # let django's AuthBackend deal with superusers.
        if user_obj.is_superuser:
            return False

        if obj and hasattr(obj, 'user_has_perm'):
            return obj.user_has_perm(user_obj, perm)

        return False


class EmailBackend:
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class BallouSMSBackend(BaseSmsBackend):
    url = 'http://sms.ballou.se/http/get/SendSms.php'

    def get_username(self):
        return settings.BALLOU_SMS_USERNAME

    def get_password(self):
        return settings.BALLOU_SMS_PASSWORD

    def parse_response(self, response):
        xml = minidom.parseString(response)

        node = xml.getElementsByTagName('message')[0]
        message = {
            'id': node.getAttribute('id'),
            'to': node.getAttribute('to_msisdn'),
            'status': node.getAttribute('status'),
            'error': node.getAttribute('error')
        }
        return message

    def send_messages(self, messages):

        for message in messages:
            for to in message.to:
                request_id = binascii.hexlify(os.urandom(16))

                params = {
                    'UN': self.get_username(),
                    'PW': self.get_password(),
                    'CR': '%s_%s' % (message.to, request_id),
                    'RI': request_id,
                    'O': message.from_phone,
                    'D': message.to,
                    'LONGSMS': 'false',
                    'M': message.body
                }

                requests.get(self.url, params=params)
                #status = self.parse_response(requests.get(self.url, params=params))
                #TODO implement logging
