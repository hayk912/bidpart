from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from functions import string_with_title

from application.apps.files.models import Image

import datetime


class BlogEntryManager(models.Manager):
    """ Object manager for BlogEntry class """

    def get_active_entries(self):
        return self.select_related('images').filter(publish__lt=timezone.now(), unpublish__gt=timezone.now(), active=True).order_by('-publish')

    def get_active_entry(self, entry_id):
        return self.get_active_entries().filter(pk=entry_id)[0]

    def get_active_entry_by_slug(self, entry_slug):
        return self.get_active_entries().filter(title_slug=entry_slug)[0]

    def get_latest_entry(self):
        return self.get_active_entries()[0]

    def get_archive(self):
        return self.get_active_entries()  # Todo


class BlogEntry(models.Model):
    """ Main news item class """

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    title_slug = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Title slug'))
    teaser = models.TextField(null=True, blank=True, verbose_name=_('Text teaser'))
    body = models.TextField(null=True, blank=True, verbose_name=_('Text body'))

    created = models.DateTimeField(blank=True, verbose_name=_('Created'), default=timezone.now())
    updated = models.DateTimeField(blank=True, verbose_name=_('Updated'), default=timezone.now())
    publish = models.DateTimeField(blank=True, verbose_name=_('Publish'), default=timezone.now())
    unpublish = models.DateTimeField(blank=True, verbose_name=_('Unpublish'), default=(timezone.now() + datetime.timedelta(weeks=52 * 100)))

    active = models.BooleanField(verbose_name=_('Active'), default=True)

    images = models.ManyToManyField(Image, through="BlogEntryImage", null=True, blank=True)

    objects = BlogEntryManager()

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        if not self.created:
            self.created = timezone.now()
        if not self.updated:
            self.updated = timezone.now()
        if not self.publish:
            self.publish = timezone.now()
        if not self.unpublish:
            self.unpublish = timezone.now() + datetime.timedelta(weeks=52 * 100)

        super(BlogEntry, self).save(*args, **kwargs)

    def number_of_images(self):
        return self.images.count()

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = string_with_title('blog', _('Blog'))
        verbose_name = _("Blog entry")
        verbose_name_plural = _("Blog entries")


class BlogEntryImage(models.Model):
    blog_entry = models.ForeignKey(BlogEntry)
    image = models.ForeignKey(Image, verbose_name=_('Image'))

    def __unicode__(self):
        return str(self.image)

    class Meta:
        app_label = string_with_title('blog', _('Blog'))
        verbose_name = _('Blog entry image')
        verbose_name_plural = _('Blog entry images')
