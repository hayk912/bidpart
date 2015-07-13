#from django.core.exceptions import ValidationError
from decimal import Decimal
from django.core.cache import cache
from django.db import models
from django.db.models import Manager
from functions import string_with_title

from django.utils.translation import ugettext_lazy as _

SETTING_KEYS = (
    ('test', 'test'),
    ('test2', 'test2')
)

SETTING_TYPES = (
    ('str', _('String')),
    ('int', _('Integer')),
    ('decimal', _('Decimal')),
    ('bool', _('Boolean')),
)
settings_cache = {}


class AdminSettingManager(Manager):
    def active_settings(self):
        return self.filter(active=True)

    def get_active_key(self, key):
        queryset = cache.get('active_settings', None)
        if not queryset:
            cache.set('active_settings', AdminSetting.objects.active_settings())
        return queryset.get(key=key)


class AdminSetting(models.Model):
    settings_group = models.ManyToManyField('AdminSettingsGroup', related_name='admin_settings', null=True, blank=True  )
    key = models.CharField(max_length=64, choices=SETTING_KEYS)
    value = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=16, choices=SETTING_TYPES, default=SETTING_KEYS[0][0])
    active = models.BooleanField()

    objects = AdminSettingManager()

    def __unicode__(self):
        return '%s: %s (%s)' % (self.key, self.value, self.active)

    def get_value(self):
        value = self.value
        try:
            if self.type == 'int':
                return int(value)
            elif self.type == 'bool':
                if value == 'False':
                    return False
                else:
                    return True
            elif self.type == 'DecimalField':
                return Decimal(value)
            else:
                return value
        except (TypeError, ValueError):
            return ''

    def save(self, *args, **kwargs):
        print self.active
        if self.active:
            existing = AdminSetting.objects.filter(key=self.key, active=True)
            if existing.exists():
                print '%s existing' % existing.count()
                existing.update(active=False)
        super(AdminSetting, self).save(*args, **kwargs)
        cache.set('active_settings', AdminSetting.objects.active_settings())

    class Meta:
        unique_together = ('key', 'value')
        app_label = string_with_title('adminsettings', _('Admin settings'))
        verbose_name = _('Admin setting')
        verbose_name_plural = _('Admin settings')


class AdminSettingsGroup(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = string_with_title('adminsettings', _('Admin settings'))
        verbose_name = _('Admin settings group')
        verbose_name_plural = _('Admin settings groups')
