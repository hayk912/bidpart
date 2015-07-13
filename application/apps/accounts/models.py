# coding=utf-8
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from functions import string_with_title
from application.apps.files.models import Image
import hashlib
import uuid


class BusinessProfile(models.Model):
    """ Business profile, UserProfile extension """

    def get_media_upload_path(instance, filename):
        md5hash = hashlib.md5(str(uuid.uuid1())).hexdigest()
        return "business_image/%s_%s" % (md5hash, filename)

    active = models.BooleanField(default=True, verbose_name=_('Active'))
    creator = models.ForeignKey('UserProfile', related_name="+", verbose_name=_('Creator'), null=True)
    business_name = models.CharField(max_length=128, blank=False, null=True, verbose_name=_('Business name'))

    business_description = models.TextField(verbose_name=_('Business description'), blank=True)
    agent = models.ForeignKey('BusinessProfile', verbose_name=_('Business agent'), blank=True, null=True)
    is_agent = models.BooleanField(default=False, verbose_name=_('Is Agent'))

    logo = models.ForeignKey(Image, related_name="business_logo", null=True, blank=True)

    country = models.CharField(max_length=128, verbose_name=_('Country'), blank=True)
    address = models.CharField(max_length=64, verbose_name=_('Address'), blank=True)
    address_zipcode = models.CharField(max_length=5, verbose_name=_('Zip code'), blank=True)
    address_city = models.CharField(max_length=64, verbose_name=_('City'), blank=True)

    profile_data_cache = models.OneToOneField('ProfileDataCache', blank=True, null=True)
    agent_data_cache = models.OneToOneField('AgentDataCache', blank=True, null=True, related_name='businessprofile')

    commission_override = models.DecimalField(_('Commission Override'), max_digits=2, decimal_places=2,
                                              null=True, blank=True)

    def __unicode__(self):
        return self.business_name

    def get_logo_url(self):
        return str(self.logo.get_url())

    class Meta:
        app_label = string_with_title('accounts', _('Accounts'))
        verbose_name = _('Business profile')
        verbose_name_plural = _('Business profiles')
        ordering = ['business_name']


class AgentProfile(BusinessProfile):
    class Meta:
        proxy = True


class ProfileDataCache(models.Model):
    current_commission_perc = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_('Provision level'),
                                                  default=Decimal('0.1'))  # ex. 0.1
    num_sold_products = models.IntegerField(default=0, verbose_name=_('Number of sold ads'))
    num_bought_products = models.IntegerField(default=0, verbose_name=_('Number of bought ads'))
    num_ads = models.IntegerField(default=0, verbose_name=_('Number of ads'))
    num_ads_views = models.IntegerField(default=0, verbose_name=_('Total views of all ads'))


class AgentDataCache(models.Model):
    num_recruited = models.IntegerField(default=0, verbose_name=_('Number of recruited businesses'))
    num_sold_products = models.IntegerField(default=0, verbose_name=_('Number of sold ads'))
    num_interested = models.IntegerField(default=0, verbose_name=_('Deals (interested)'))
    num_active = models.IntegerField(default=0, verbose_name=_('Deals (active)'))
    num_completed = models.IntegerField(default=0, verbose_name=_('Deals (done)'))
    num_canceled = models.IntegerField(default=0, verbose_name=_('Deals (canceled)'))


class UserProfile(models.Model):
    """ User profile, User extension """

    user = models.OneToOneField(User, related_name='userprofile', verbose_name=_('User'))
    active_profile = models.ForeignKey('BusinessProfile', related_name="+", verbose_name=_('Active profile'))
    business_profiles = models.ManyToManyField(BusinessProfile, related_name="business_profiles")

    phone = models.CharField(max_length=32, verbose_name=_('Phone'), blank=True)
    cellphone = models.CharField(max_length=32, verbose_name=_('Cellphone'), blank=True)

    avatar = models.ForeignKey(Image, null=True, blank=True)

    lang_code = models.CharField(max_length=5, verbose_name=_('Language code'), blank=True)

    newsletter = models.BooleanField()

    def get_business_profiles(self):
        return self.business_profiles.all()

    def get_num_business_profiles(self):
        return self.business_profiles.count()

    def has_business_profile(self):
        return bool(self.business_profiles.count())

    def has_active_business_profile(self):
        return bool(self.active_profile)

    def get_avatar_url(self):
        return str(self.avatar.get_url())

    def __unicode__(self):
        return u'{first_name} {last_name}'.format(
            first_name=self.user.first_name,
            last_name=self.user.last_name
        )

    class Meta:
        app_label = string_with_title('accounts', _('Accounts'))
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')


class OldPassword(models.Model):
    """ Old passwords, to be converted """
    user = models.ForeignKey(User)
    old_password = models.CharField(max_length=128)
    old_nonce = models.CharField(max_length=32)

    def __unicode__(self):
        return unicode(self.old_password + " | " + self.old_nounce)

# END models


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile, created = UserProfile.objects.get_or_create(user=instance)
        user_profile.save()


def get_business_profile(self):
    if not hasattr(self, '_profile_cache'):
        self._profile_cache = UserProfile.objects.get(user__id__exact=self.id)
        self._profile_cache.user = self

    if not hasattr(self, '_multiprofile_cache'):
        if self._profile_cache.active_profile_id:
            self._multiprofile_cache = BusinessProfile.objects.get(pk=self._profile_cache.active_profile_id)
            self._multiprofile_cache.userprofile = self._profile_cache
        else:
            raise ObjectDoesNotExist()

    return self._multiprofile_cache

User.add_to_class('get_business_profile', get_business_profile)
post_save.connect(create_user_profile, sender=User, dispatch_uid="CreateUserProfileOnce")


# Original get_profile method
class SiteProfileNotAvailable(Exception):
    pass


def get_userprofile(self):
    """
    Returns site-specific profile for this user. Raises
    SiteProfileNotAvailable if this site does not allow profiles.
    """
    if not hasattr(self, '_profile_cache'):
        from django.conf import settings
        if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
            raise SiteProfileNotAvailable(
                'You need to set AUTH_PROFILE_MODULE in your project '
                'settings')
        try:
            app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        except ValueError:
            raise SiteProfileNotAvailable(
                'app_label and model_name should be separated by a dot in '
                'the AUTH_PROFILE_MODULE setting')
        try:
            model = models.get_model(app_label, model_name)
            if model is None:
                raise SiteProfileNotAvailable(
                    'Unable to load the profile model, check '
                    'AUTH_PROFILE_MODULE in your project settings')
            self._profile_cache = model._default_manager.using(
                               self._state.db).get(user__id__exact=self.id)
            self._profile_cache.user = self
        except (ImportError, ImproperlyConfigured):
            raise SiteProfileNotAvailable
    return self._profile_cache


User.add_to_class('get_userprofile', get_userprofile)
