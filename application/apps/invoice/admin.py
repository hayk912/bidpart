from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import models


class RowsInline(admin.TabularInline):
    model = models.Row
    extra = 0
    ordering = ('-created', )


class RowAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'deal', 'updated', 'created', )
    date_hierarchy = 'created'


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'our_reference', 'your_reference', 'sent', 'sent_timestamp', 'state', 'expiration', 'updated', 'created', )
    list_filter = ('state', 'sent', )
    search_fields = ('receiver', 'our_reference', 'your_reference', )
    readonly_fields = ('pdf_link',)
    date_hierarchy = 'created'
    inlines = [RowsInline]

    def pdf_link(self, obj):
        if obj.is_written_to_disk:
            return mark_safe('<a href="%s">%s</a>' % (obj.get_absolute_url(), _('PDF-file')))
        else:
            return _('Invoice is not generated to disk.')
    pdf_link.short_description = ''


admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.Row, RowAdmin)
admin.site.register(models.InvoiceLogEntry)
