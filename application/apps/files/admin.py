from models import Image, File, SiteFile
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'filename', 'formatted_filesize', )
    readonly_fields = ('title_slug', 'unique_hash', 'filesize',)

    def formatted_filesize(self, instance):
        if instance.filesize < 1000:
            return "%s B" % instance.filesize
        return "%s kB" % (instance.filesize / 1000, )

    formatted_filesize.short_description = _('Filesize')


class SiteFileAdmin(FileAdmin):
    list_display = ('title', 'id', 'filename', 'formatted_filesize', 'file_key' )


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin_thumb', 'id', 'image_filename', 'formatted_filesize', )
    readonly_fields = ('title_slug', 'unique_hash', 'admin_image', 'filesize', 'width', 'height',
                       'created', 'updated')

    def formatted_filesize(self, instance):
        if instance.filesize < 1000:
            return "%s B" % instance.filesize
        return "%s kB" % (instance.filesize / 1000, )

    formatted_filesize.short_description = _('Filesize')

    def admin_image(self, instance):
        return '<img src="%s"/>' % instance.get_url()

    admin_image.allow_tags = True
    admin_image.short_description = _("Image")

    def admin_thumb(self, instance):
        return '<img src="%s"/>' % instance.get_thumb('admin_thumb')

    admin_thumb.allow_tags = True
    admin_thumb.short_description = _("Image")


admin.site.register(Image, ImageAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(SiteFile, SiteFileAdmin)
