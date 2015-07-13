from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
import models


class BlogEntryImageInline(admin.TabularInline):
    fields = ('image', 'admin_image', )
    readonly_fields = ('admin_image', )

    def admin_image(self, instance):
        return '<img src="%s"/><p>%s x %s px (%s kB)</p>' % (instance.image.get_thumb('admin_thumb'), instance.image.width, instance.image.height, instance.image.filesize / 1000, )

    admin_image.allow_tags = True
    admin_image.short_description = ''

    model = models.BlogEntryImage
    extra = 1


class BlogEntryAdmin(admin.ModelAdmin):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/core/js/tinymce_setup.js',
            ]
    list_display = ('title', 'created', 'publish', 'unpublish', 'number_of_images', )
    fieldsets = [
        (None,
            {
                'classes': ['markdown', ],
                'fields': ['title', 'teaser', 'body', ]
            },
        ),
        (_('Publish'),
            {
               'fields': ['publish', 'unpublish', 'created', 'updated', 'active', ]
            }
        ),
    ]
    readonly_fields = ('created', 'title_slug', )
    search_fields = ('title', )
    inlines = [BlogEntryImageInline]


admin.site.register(models.BlogEntry, BlogEntryAdmin)
