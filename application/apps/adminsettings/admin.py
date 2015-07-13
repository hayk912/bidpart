import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class AdminSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'type', 'active', 'get_settings_group',)
    list_filter = ('active', 'key', 'settings_group',)
    search_fields = ('key',)
    actions = ['activate', 'deactivate']

    def get_settings_group(self, instance):
        return ', '.join([v.name for v in instance.settings_group.all()])

    def activate(self, request, queryset):
        queryset = queryset.get()
        queryset.active = True
        queryset.save()
        self.message_user(request, _('Activated setting!'))
    activate.short_description = _('Activate setting')

    def deactivate(self, request, queryset):
        queryset = queryset.get()
        queryset.active = False
        queryset.save()
        self.message_user(request, _('Deactivated setting!'))
    deactivate.short_description = _('Deactivate setting')


class AdminSettingAdminInline(admin.TabularInline):
    verbose_name = _('Product type')
    verbose_name_plural = _('Product types')
    model = models.AdminSetting.settings_group.through
    extra = 0


class AdminSettingsGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [AdminSettingAdminInline]
    actions = ['activate_settings_group', 'deactivate_settings_group']

    def _change_settings_group(self, request, queryset, bool=None):
        settings = queryset.get().admin_settings.all()
        num = 0
        for item in settings:
            item.active = bool
            item.save()
            num += 1
        return num

    def activate_settings_group(self, request, queryset):
        num = self._change_settings_group(request, queryset, bool=True)
        self.message_user(request, '%s settings activated.' % (num,))
    activate_settings_group.short_description = 'Activate settings in settings group'

    def deactivate_settings_group(self, request, queryset):
        num = self._change_settings_group(request, queryset, bool=False)
        self.message_user(request, '%s settings deactivated.' % (num,))
    deactivate_settings_group.short_description = 'Deactivate settings in settings group'



admin.site.register(models.AdminSetting, AdminSettingAdmin)
admin.site.register(models.AdminSettingsGroup, AdminSettingsGroupAdmin)
