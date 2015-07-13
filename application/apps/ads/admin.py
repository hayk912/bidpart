from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _, ugettext
from application import settings
import models


# Inlines

class AdImageInline(admin.TabularInline):
    fields = ('image_filename', 'admin_image', )
    readonly_fields = ('admin_image', )
    model = models.AdImage
    extra = 0

    def admin_image(self, instance):
        return '<img src="%s"/><p>%s x %s px (%s kB)</p>' % (
            instance.image.get_thumb('admin_thumb'), instance.image.width, instance.image.height,
            instance.image.filesize / 1000, )

    admin_image.allow_tags = True
    admin_image.short_description = ''

    def queryset(self, request):
        queryset = super(AdImageInline, self).queryset(request)
        queryset = queryset.select_related()
        return queryset

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(AdImageInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'image':
            # dirty trick so queryset is evaluated and cached in .choices
            formfield.choices = formfield.choices
        return formfield


class AdFileInline(admin.TabularInline):
    model = models.AdFile
    list_select_related = True
    extra = 0

    def queryset(self, request):
        queryset = super(AdFileInline, self).queryset(request)
        queryset = queryset.select_related()
        return queryset

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(AdFileInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'file':
            # dirty trick so queryset is evaluated and cached in .choices
            formfield.choices = formfield.choices
        return formfield


class ValuesAdminInline(admin.TabularInline):
    fields = ('field', 'value', 'choice_value')

    def queryset(self, request):
        queryset = super(ValuesAdminInline, self).queryset(request)
        queryset = queryset.select_related()
        return queryset

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ValuesAdminInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'field':
            # dirty trick so queryset is evaluated and cached in .choices
            formfield.choices = formfield.choices
        return formfield

    model = models.Value
    extra = 0


class ProductTypesAdminInline(admin.TabularInline):
    verbose_name = _('Product type')
    verbose_name_plural = _('Product types')
    model = models.ProductType.product_categories.through
    extra = 0


class FieldChoiceAdminInline(admin.TabularInline):
    model = models.FieldChoice
    extra = 0


class AdAdmin(admin.ModelAdmin):
    readonly_fields = ('last_deal_updated', 'created', 'updated', 'num_views')
    filter_horizontal = ('business_domains', )
    raw_id_fields = ('creator', 'owner', 'product_type')
    inlines = [
        ValuesAdminInline, AdImageInline, AdFileInline
    ]
    list_display = ['__unicode__', 'price', 'currency', 'amount', 'product_type', 'published', 'active', 'featured',
                    'num_views', 'is_request']
    actions = ['toggle_published', 'toggle_featured', 'toggle_active']
    search_fields = []
    list_filter = ('published', 'active', 'product_type__title', 'owner')

    fieldsets = [
        (_('Product information'), {
            'fields': ['price', 'currency', 'amount', 'youtube_code']
        }),
        (_('Product type'), {
            'fields': ('product_type', 'business_domains')
        }),
        (_('Other'), {
            'fields': ('creator', 'owner', 'featured', 'active')
        }),
        (_('Information'), {
            'fields': ('last_deal_updated', 'created', 'updated', 'num_views')
        })
    ]

    def __init__(self, model, admin_site):
        print self.fieldsets[0]
        for lang_code, lang_name in reversed(settings.LANGUAGES):
            self.search_fields.append('title_{0}'.format(lang_code))
            fieldset = (lang_name, {
                'fields': [
                    'title_{0}'.format(lang_code),
                    'description_{0}'.format(lang_code)
                ]
            })
            self.fieldsets.insert(0, fieldset)



        super(AdAdmin, self).__init__(model, admin_site)

    def _success_message(self, request, rows_updated, thing):
        if rows_updated == 0:
            return
        elif rows_updated == 1:
            message_bit = '1 Ad was'
        else:
            message_bit = '%s Ads where' % rows_updated

        self.message_user(request,
                          '%s successfully %s.' % (message_bit, thing))

    def _toggle_bool(self, queryset, field):
        rows_true = 0
        rows_false = 0
        for i, item in enumerate(queryset):
            bool = getattr(item, field)
            setattr(item, field, not bool)
            item.save()

            if bool:
                rows_false += 1
            else:
                rows_true += 1

        return rows_true, rows_false

    def toggle_published(self, request, queryset):
        rows_published, rows_unpublished = self._toggle_bool(queryset, 'published')
        self._success_message(request, rows_published, 'published')
        self._success_message(request, rows_unpublished, 'unpublished')

    toggle_published.short_description = 'Toggle published'

    def toggle_featured(self, request, queryset):
        rows_featured, rows_unfeatured = self._toggle_bool(queryset, 'featured')
        self._success_message(request, rows_featured, 'featured')
        self._success_message(request, rows_unfeatured, 'unfeatured')

    toggle_featured.short_description = 'Toggle featured'

    def toggle_active(self, request, queryset):
        rows_activated, rows_deactivated = self._toggle_bool(queryset, 'active')
        self._success_message(request, rows_activated, 'activated')
        self._success_message(request, rows_deactivated, 'deactivated')

    toggle_active.short_description = 'Toggle active'


class BusinessDomainAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductTypesAdminInline,
    ]
    list_display = ('title',)
    search_fields = ('title',)


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'required', 'type', 'suffix')
    inlines = [FieldChoiceAdminInline]
    list_filter = ('suffix', 'type', 'required',)
    search_fields = ('name', )


admin.site.register(models.Ad, AdAdmin)
admin.site.register(models.BusinessDomain, BusinessDomainAdmin)
admin.site.register(models.ProductType, ProductTypeAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.Field, FieldAdmin)
admin.site.register(models.Value)
