from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.forms import ModelForm, forms
from django.utils.translation import ugettext_lazy as _
from application import settings
from application.apps.files.admin import ImageAdmin
import models

class PageImageAdmin(ImageAdmin):
    model = models.SliderImage

class PageImageInline(admin.TabularInline):
    fields = ('title', 'image_filename', 'thumbnail', 'created', 'updated')
    readonly_fields = ('thumbnail', 'created', 'updated')
    model = models.PageImage
    extra = 3

    def thumbnail(self, obj):
        return '<img src="%s">' % obj.get_thumb('admin_thumb')
    thumbnail.short_description = _('Thumbnail')
    thumbnail.allow_tags = True


class PageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        for field_name in self.fields.keys():
            if 'body' in field_name:
                self.fields[field_name].widget = CKEditorWidget()


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_slug', 'created', 'number_of_images', )
    prepopulated_fields = {'title_slug': ('title',)}
    readonly_fields = ('created', 'updated')
    search_fields = ('title', )
    inlines = [PageImageInline]
    form = PageForm

    def __init__(self, model, admin_site):
        super(PageAdmin, self).__init__(model, admin_site)

        localized_titles = ['title_%s' % l[0] for l in settings.LANGUAGES]
        localized_bodies = ['body_%s' % l[0] for l in settings.LANGUAGES]
        self.fieldsets = [
            (_('Title'), {
                'fields': ['title'] + localized_titles
            }),
            (_('Body'), {
                'fields': localized_bodies
            }),
            (None, {
                'fields': ['active', 'show_in_menu', 'title_slug', 'created', 'updated', ]
            })
        ]


class SliderPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    readonly_fields = ('created', 'updated')


class SliderImageAdmin(ImageAdmin):
    model = models.SliderImage


class EmailTemplateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailTemplateForm, self).__init__(*args, **kwargs)

        for field_name in self.fields.keys():
            if 'html' in field_name:
                self.fields[field_name].widget = CKEditorWidget()


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('subject_%s' % settings.LANGUAGES[0][0], 'name')
    readonly_fields = ('name',)
    form = EmailTemplateForm

    def __init__(self, model, admin_site):
        localized_subjects = ['subject_%s' % l[0] for l in settings.LANGUAGES]
        localized_htmls = ['html_%s' % l[0] for l in settings.LANGUAGES]
        localized_txts = ['txt_%s' % l[0] for l in settings.LANGUAGES]
        self.fieldsets = [
            (_('Subject'), {
                'fields': localized_subjects
            }),
            (_('HTML'), {
                'fields': localized_htmls
            }),
            (_('Plain text'), {
                'fields': localized_txts
            }),
            (None, {
                'fields': ['name', ]
            })
        ]
        super(EmailTemplateAdmin, self).__init__(model, admin_site)

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.Page, PageAdmin)
admin.site.register(models.PageImage, PageImageAdmin)
admin.site.register(models.SliderPage, SliderPageAdmin)
admin.site.register(models.SliderImage, SliderImageAdmin)
admin.site.register(models.EmailTemplate, EmailTemplateAdmin)
