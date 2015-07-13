from django.conf import settings
from django.contrib import admin
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import models


class DealAdmin(admin.ModelAdmin):
    list_display = ('state', 'ad_link', 'owner_link', 'seller_link', 'bid', 'currency', 'price', 'commission', 'agent_commission', 'created', 'updated', 'renewed', )
    date_hierarchy = 'created'
    list_filter = ('payed_to_agent', 'manual_processing', 'state', 'owner', 'creator')
    search_fields = ['owner__business_name', 'creator__user__first_name', 'creator__user__last_name']
    readonly_fields = ('seller_link', 'owner_link', 'invoice_link', )
    exclude = ('invoice', )

    def __init__(self, model, admin_site):
        for lang_code, lang_name in settings.LANGUAGES:
            self.search_fields.append('ad__title_{0}'.format(lang_code))

        super(DealAdmin, self).__init__(model, admin_site)

    def invoice_link(self, obj):
        change_url = urlresolvers.reverse('admin:invoice_invoice_change', args=(obj.invoice.pk,))
        return mark_safe('<a href="%s">%s</a>' % (change_url, obj.invoice))
    invoice_link.short_description = 'If this deal auto-created a invoice, it will be referenced here'

    def ad_link(self, instance):
        return u'<a href="{link}">{title}</a>'.format(
            link=reverse('admin:ads_ad_change', args=(instance.ad.pk,)),
            title=unicode(instance.ad)
        )
    ad_link.allow_tags = True
    ad_link.short_description = _('Ad')

    def owner_link(self, instance):
        buyer = instance.ad.owner if instance.ad.is_request else instance.owner

        return u'<a href="{link}">{title}</a>'.format(
            link=reverse('admin:accounts_businessprofile_change', args=(buyer.pk,)),
            title=unicode(buyer)
        )
    owner_link.allow_tags = True
    owner_link.short_description = _('Buyer')

    def seller_link(self, instance):
        seller = instance.owner if instance.ad.is_request else instance.ad.owner
        return u'<a href="{link}">{title}</a>'.format(
            link=reverse('admin:accounts_businessprofile_change', args=(seller.pk,)),
            title=unicode(seller)
        )
    seller_link.allow_tags = True
    seller_link.short_description = _('Seller')

admin.site.register(models.Deal, DealAdmin)
