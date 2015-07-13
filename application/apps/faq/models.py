from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from application.apps.faq.func import string_with_title
# Create your models here.


class FAQGroup(MPTTModel):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        app_label = string_with_title('faq', 'FAQ')
        verbose_name = _('FAQ group')
        verbose_name_plural = _('FAQ groups')

    def __unicode__(self):
        return self.name


class FAQQuestion(models.Model):
    group = models.ManyToManyField(FAQGroup, db_table="faq_question_groups", verbose_name=_("Groups"))
    question = models.CharField(max_length=255, verbose_name=_("Question"))
    answer = models.TextField(verbose_name=_("Answer"))
    only_logged_in = models.BooleanField(verbose_name=_("Only allow logged in users to view this question"))

    class Meta:
        app_label = string_with_title('faq', 'FAQ')
        verbose_name = _('FAQ question')
        verbose_name_plural = _('FAQ questions')

    def __unicode__(self):
        return self.question
