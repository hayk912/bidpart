from application.apps.accounts.models import OldPassword
from application.apps.accounts.functions import old_pw_crypt
from django.contrib.auth.models import User
from django.core.validators import email_re


class OldPasswordBackend:
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
        else:
            try:
                old_password = OldPassword.objects.get(user=user)
            except:
                return None
            else:
                # Found old password, save and delete old record
                if old_password.old_password == old_pw_crypt(password, old_password.old_nonce):
                    user.set_password(password)
                    user.save()
                    old_password.delete()
                    return user
                else:
                    return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
