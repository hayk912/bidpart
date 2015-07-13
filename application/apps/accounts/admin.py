from django.core.urlresolvers import reverse
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from application.apps.accounts.models import UserProfile, BusinessProfile, AgentProfile


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'phone', 'newsletter', 'business_link')
    list_display = ('user', 'active_profile', 'cellphone', 'newsletter')
    readonly_fields = ('avatar_image', 'business_link')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    list_filter = ('newsletter', )

    def avatar_image(self, instance):
        return '<img src="%s"/>' % instance.get_avatar_url()
    avatar_image.allow_tags = True
    avatar_image.short_description = _("Avatar")

    def business_link(self, instance):
        return u'<a href="{link}">{business_name}</a>'.format(
            link=reverse('admin:accounts_businessprofile_change', args=(instance.active_profile.pk,)),
            business_name=instance.active_profile.business_name,
        )
    business_link.allow_tags = True
    business_link.short_description = _('Business profile')

    def queryset(self, request):
        queryset = super(UserProfileAdmin, self).queryset(request)
        queryset = queryset.select_related('user', 'active_profile', 'business_profiles')
        return queryset


class BusinessProfileAdmin(admin.ModelAdmin):
    fields = ('business_name', 'creator_link', 'business_description', 'agent', 'address', 'address_zipcode',
              'commission_override', 'address_city', 'logo', 'is_agent', 'active')
    readonly_fields = ('creator_link', )
    list_display = ('business_name', 'contact_person', 'contact_info', 'num_ads', 'num_sold_products',
                    'num_bought_products', 'current_commission_perc')
    search_fields = ('business_name', )

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        formfield = super(BusinessProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'agent':
            formfield.queryset = formfield.queryset.filter(is_agent=True)
        return formfield

    def queryset(self, request):
        queryset = super(BusinessProfileAdmin, self).queryset(request)
        queryset = queryset.select_related('creator')
        return queryset.select_related('profile_data_cache')

    def creator_link(self, instance):
        return u'<a href="{link}">{first_name} {last_name}</a>'.format(
            link=reverse('admin:accounts_userprofile_change', args=(instance.creator.pk,)),
            first_name=instance.creator.user.first_name,
            last_name=instance.creator.user.last_name
        )
    creator_link.allow_tags = True
    creator_link.short_description = _('Contact person')

    def contact_info(self, instance):
        return u'{address} {zipcode} {city}'.format(
            address=instance.address,
            zipcode=instance.address_zipcode,
            city=instance.address_city
        )
    contact_info.allow_tags = True

    def contact_person(self, instance):
        return u'{first_name} {last_name}'.format(
            first_name=instance.creator.user.first_name,
            last_name=instance.creator.user.last_name,
        )

    def num_ads(self, instance):
        return instance.profile_data_cache.num_ads
    num_ads.admin_order_field = 'profile_data_cache__num_ads'

    def num_sold_products(self, instance):
        return instance.profile_data_cache.num_sold_products
    num_sold_products.admin_order_field = 'profile_data_cache__num_sold_products'

    def num_bought_products(self, instance):
        return instance.profile_data_cache.num_bought_products
    num_bought_products.admin_order_field = 'profile_data_cache__num_bought_products'

    def current_commission_perc(self, instance):
        return '%i%s' % (instance.profile_data_cache.current_commission_perc * 100, '%')
    current_commission_perc.admin_order_field = 'profile_data_cache__current_commission_perc'


class AgentProfileAdmin(BusinessProfileAdmin):
    fields = ('business_name', 'business_description', 'address', 'address_zipcode', 'address_city', 'logo', 'active')
    list_display = ('id', 'business_name', 'num_recruited', 'num_sold_products', 'num_interested', 'num_active',
                    'num_completed', 'num_canceled')

    def __init__(self, model, admin_site):
        super(AgentProfileAdmin, self).__init__(model, admin_site)

    def queryset(self, request):
        queryset = super(AgentProfileAdmin, self).queryset(request)
        return queryset.filter(is_agent=True).select_related('agent_data_cache')

    def num_recruited(self, instance):
        return instance.agent_data_cache.num_recruited
    num_recruited.admin_order_field = 'agent_data_cache__num_recruited'

    def num_sold_products(self, instance):
        return instance.agent_data_cache.num_sold_products
    num_sold_products.admin_order_field = 'agent_data_cache__num_sold_products'

    def num_interested(self, instance):
        return instance.agent_data_cache.num_interested
    num_interested.admin_order_field = 'agent_data_cache__num_interested'

    def num_active(self, instance):
        return instance.agent_data_cache.num_active
    num_active.admin_order_field = 'agent_data_cache__num_active'

    def num_completed(self, instance):
        return instance.agent_data_cache.num_completed
    num_completed.admin_order_field = 'agent_data_cache__num_completed'

    def num_canceled(self, instance):
        return instance.agent_data_cache.num_canceled
    num_canceled.admin_order_field = 'agent_data_cache__num_canceled'

admin.site.register(BusinessProfile, BusinessProfileAdmin)
admin.site.register(AgentProfile, AgentProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
