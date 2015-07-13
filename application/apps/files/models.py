from django.db import models
from django.utils.translation import ugettext_lazy as _
from functions import string_with_title
from storage import OverwriteStorage
from autoslug import AutoSlugField
from application import settings
from django.contrib.auth.models import User
import uuid
import hashlib
#import Image as PILImage
import os


class BaseFile(models.Model):
    """ Abstract base class for Image and File """

    file_dir = 'files'  # Subdirectory in MEDIA_ROOT and MEDIA_URL

    def get_media_upload_path(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        if not extension:
            raise IOError('No file extension!')
        return "%s/%s_%s.%s" % (instance.file_dir, instance.unique_hash, instance.title_slug, extension.lower(), )

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    title_slug = AutoSlugField(always_update=True, null=True, populate_from='title',
                               verbose_name=_('Title slug'))  # Ej unique
    description_short = models.TextField(verbose_name=_('Short description'), blank=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    unique_hash = models.CharField(max_length=32, null=True, blank=True, unique=True,
                                   verbose_name=_('Unique identifier'))
    filesize = models.IntegerField(default=0, verbose_name=_('File size'), blank=True)
    creator = models.ForeignKey(User, null=True, blank=True, verbose_name=_('Creator'))

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.unique_hash:
            self.unique_hash = hashlib.md5(str(uuid.uuid1())).hexdigest()[16:]
        super(BaseFile, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class File(BaseFile):
    """ Class for representing and handling genreric non-image files """

    filename = models.FileField(upload_to=BaseFile.get_media_upload_path, blank=True, null=True,
                                storage=OverwriteStorage(), verbose_name=_('File'))

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.filename.name
        if self.filename:
            self.filesize = self.filename.size
        super(File, self).save(*args, **kwargs)

    def get_url(self):
        return settings.MEDIA_URL + str(self.filename)

    def get_absolute_url(self):
        return settings.MEDIA_URL + str(self.filename)

    class Meta:
        app_label = string_with_title('files', _('Files'))
        verbose_name = _('File')
        verbose_name_plural = _('Files')


class SiteFile(File):
    file_dir = 'sitefiles'
    file_key = models.CharField(max_length=64, unique=True, verbose_name=_('File key'))

    class Meta:
        app_label = string_with_title('files', _('Files'))
        verbose_name = _('Site file')
        verbose_name_plural = _('Site files')


class Image(BaseFile):
    """ Class for representing and creating an image and handling its thumbnails """

    file_dir = 'images'
    image_filename = models.ImageField(upload_to=BaseFile.get_media_upload_path, blank=True, null=True,
                                       storage=OverwriteStorage(), width_field='width', height_field='height',
                                       verbose_name=_('Image file'))

    width = models.IntegerField(default=0, verbose_name=_('Width'), help_text=_('The width in pixels.'))
    height = models.IntegerField(default=0, verbose_name=_('Height'), help_text=_('The height in pixels.'))

    def get_thumb(self, thumb_format):
        """ Returns the thumbnail URL, creates it if necessary """

        if thumb_format not in [t for t, d in settings.IMAGE_THUMB_FORMATS]:
            return False
        thumb_filename = self._get_thumb_filename(thumb_format=thumb_format)
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, thumb_filename)):
            self._generate_thumb(thumb_format=thumb_format)

        return settings.MEDIA_URL + thumb_filename

    def get_url(self):
        """ Returns the absolute file path (URL) for the original image """

        return settings.MEDIA_URL + str(self.image_filename)

    def _get_thumb_filename(self, thumb_format):
        """ Returns the absolute file path (URL) without first slash for a thumb """

        fname, dot, extension = str(self.image_filename).rpartition('.')
        return "%s/%s/%s_%s.%s" % (self.file_dir, thumb_format, self.unique_hash, self.title_slug, extension, )

    def _generate_thumb(self, thumb_format):
        """ Generate thumbformat for selected format """

        if thumb_format not in [t for t, d in settings.IMAGE_THUMB_FORMATS]:
            raise ValueError("Invalid thumb format: '%s'" % thumb_format)

        if not self.image_filename:
            return

        # Infile is the original source file
        infile = os.path.join(settings.MEDIA_ROOT, str(self.image_filename))

        # Check for the thumb directory
        thumb_dir = os.path.join(settings.MEDIA_ROOT, self.file_dir, thumb_format)
        if not os.path.exists(thumb_dir):
            os.mkdir(thumb_dir)

        # Get the outfile, full system path (settings.MEDIA_ROOT)
        thumb_format_data = None
        outfile = os.path.join(settings.MEDIA_ROOT, self._get_thumb_filename(thumb_format=thumb_format))
        for t in settings.IMAGE_THUMB_FORMATS:
            if t[0] == thumb_format:
                thumb_format_data = t[1]
                break

        if infile != outfile and thumb_format_data:
            try:
                im = PILImage.open(infile)
                size = int(thumb_format_data[0]), int(thumb_format_data[1])
                if thumb_format_data[2]:  # Fit thumb precisely
                    im = self._fit_thumb(im, size)
                else:
                    im.thumbnail(size, PILImage.ANTIALIAS)
                im.save(outfile)
            except IOError:
                pass

    def get_dimensions(self):
        """ Returns the width and height of the original image """

        infile = os.path.join(settings.MEDIA_ROOT, str(self.image_filename))
        try:
            im = PILImage.open(infile)
            width, height = im.size
            return width, height
        except IOError:
            return 0, 0

    def _fit_thumb(self, img, size):
        """ Scale then crop """

        src_width, src_height = img.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = size
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = int(float(src_width - crop_width) / 2)
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = int(float(src_height - crop_height) / 3)
        img = img.crop((x_offset, y_offset, x_offset + int(crop_width), y_offset + int(crop_height)))
        img = img.resize((dst_width, dst_height), PILImage.ANTIALIAS)
        return img

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.image_filename.name
        if self.image_filename:
            self.filesize = self.image_filename.size
        super(Image, self).save(*args, **kwargs)

        if self.image_filename:
            for t, d, in settings.IMAGE_THUMB_FORMATS:
                self._generate_thumb(t)

    class Meta:
        app_label = string_with_title('files', _('Files'))
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

