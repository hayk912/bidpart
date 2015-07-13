from django.db import models
from picklefield.fields import PickledObjectField
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from sendsms.api import send_sms


class NotificationManager(models.Manager):
    def create(self, profile, message, uri, params):
        users = User.objects.filter(userprofile__business_profiles=profile)
        notifs = []
        for user in users:
            notif = Notification(user=user, message=message, uri=uri,
                params=params)
            notif.save()
            notifs.append(notif)

        return notifs


class NotificationSettingsManager(models.Manager):
    def setting_for_notification(self, notification):
        return NotificationSetting.objects.get(for_uri=notification.uri,
            user=notification.user)


class Notification(models.Model):
    objects = NotificationManager()

    ALLOWED_URI_CHOICES = (
        ('ads:ad', 'Ad'),
        ('notifications:detail', 'Notification')
    )

    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='notifications')
    uri = models.CharField(max_length=255, choices=ALLOWED_URI_CHOICES)
    params = PickledObjectField()
    created = models.DateTimeField(auto_now_add=True)
    read_timestamp = models.DateTimeField(null=True)
    is_read = models.BooleanField(default=False, db_column='is_read')
    did_email = models.BooleanField(default=False)
    did_sms = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return ('notifications:goto', (), {'notification_id': self.pk})


class NotificationSetting(models.Model):
    objects = NotificationSettingsManager()

    user = models.ForeignKey(User, related_name='notification_settings')
    for_uri = models.CharField(max_length=255,
        choices=Notification.ALLOWED_URI_CHOICES)
    email = models.BooleanField(default=True)
    sms = models.BooleanField(default=False)


@receiver(pre_save, sender=Notification)
def _notification_read(sender, instance, **kwargs):
    if instance.is_read and not instance.read_timestamp:
        instance.read_timestamp = timezone.now()


@receiver(pre_save, sender=Notification)
def _notification_emails_sms(sender, instance, **kwargs):
    if not instance.pk:
        settings = NotificationSetting.objects.setting_for_notification(instance)

        if settings.email:
            send_mail(subject='New notification on Bidpart!',
                message=instance.message, from_email='notification@bidpart.se',
                recipient_list=[settings.user.email])
            instance.did_email = True
        if settings.sms:
            cellphone = instance.user.userprofile.cellphone
            if cellphone:
                send_sms(body=instance.message, from_phone='Bidpart AB',
                    to=[cellphone])
                instance.did_sms = True


@receiver(post_save, sender=User)
def _create_notification_settings(sender, instance, created, **kwargs):
    if created:
        for uri in Notification.ALLOWED_URI_CHOICES:
            setting = NotificationSetting(user=instance, for_uri=uri[0])
            setting.save()
