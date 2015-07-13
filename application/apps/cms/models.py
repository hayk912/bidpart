from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.template.defaultfilters import slugify
from application.apps.files.models import Image
from application.apps.locale.models import locale_model, DEFAULT_FIELD


class PageManager(models.Manager):
    """ Object manager for Page class """

    def get_active_page(self, title_slug):
        return self.get(title_slug=title_slug, active=True)


class SliderImage(Image):
    pass


slider_page_localized = locale_model({
    'title': DEFAULT_FIELD,
    'body': ('TextField', {'blank': True, 'default': ''})
})
class SliderPage(slider_page_localized):

    image = models.ForeignKey(SliderImage, verbose_name=_('Image'), related_name='pages', null=True, blank=True)
    order = models.IntegerField(max_length=3, default=0)
    active = models.BooleanField(default=True, verbose_name=_('Active on site'))
    title = models.CharField(max_length=32, verbose_name=_('Internal title'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Slider page')
        verbose_name_plural = _('Slider pages')

    def __unicode__(self):
        return self.title


page_localized = locale_model({
    'title': DEFAULT_FIELD,
    'body': ('TextField', {'blank': True, 'default': ''})
})

class Page(page_localized):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=64, verbose_name=_('Internal title'))
    title_slug = models.CharField(max_length=64, unique=True, verbose_name=_('URL slug'))

    created = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(null=True, blank=True, auto_now=True, verbose_name=_('Updated'))

    show_in_menu = models.BooleanField(verbose_name=_('Show in top menu'))

    objects = PageManager()

    def number_of_images(self):
        return self.images.count()

    def save(self, *args, **kwargs):
        if not self.title_slug:
            self.title_slug = slugify(self.default_title)
        super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class PageImage(Image):
    page = models.ForeignKey(Page, related_name='images', null=True, blank=True)


email_template_localized = locale_model({
    'subject': ('CharField', {'verbose_name': _('Subject'), 'blank': True, 'max_length':64}),
    'html': ('TextField', {'verbose_name': _('HTML Template'), 'blank': True}),
    'txt': ('TextField', {'verbose_name': _('Text Template'), 'blank': True})
})
class EmailTemplate(email_template_localized):
    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Email template')
        verbose_name_plural = _('Email templates')
