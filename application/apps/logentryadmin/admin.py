from django.contrib.admin.models import LogEntry, DELETION, ADDITION, CHANGE
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'object_link',
        'content_type',
        'user_link',
        'action_time',
        'get_action_flag',
        'change_message',
        ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return super(LogEntryAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_action_flag(self, instance):
        if instance.action_flag == ADDITION:
            return _('Added')
        elif instance.action_flag == CHANGE:
            return _('Changed')
        elif instance.action_flag == DELETION:
            return _('Deleted')

    get_action_flag.short_description = _('Action')

    def user_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.user)
        else:
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % ('auth', 'user'), args=[obj.user_id]),
                escape(obj.user),
                )
        return link
    user_link.allow_tags = True
    user_link.admin_order_field = 'user'
    user_link.short_description = _('User')

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
                )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'


admin.site.register(LogEntry, LogEntryAdmin)
