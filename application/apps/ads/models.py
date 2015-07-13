import hashlib
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.core.urlresolvers import reverse, resolve
from autoslug import AutoSlugField
from decimal import Decimal
from currencies.models import Currency
from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils.datastructures import SortedDict
from application.apps.accounts.models import UserProfile, BusinessProfile
from django.utils.translation import ugettext_lazy as _, ugettext
from application.apps.accounts.functions import string_with_title
from application.apps.files.models import Image, File
from application.apps.locale.models import locale_model, DEFAULT_FIELD


def cached_queryset(queryset, timeout, cache_key=None):
    if cache_key is None:
        cache_key = hashlib.md5(str(queryset.query)).hexdigest()
    cache_ = cache.get(cache_key)
    if cache_:
        queryset = cache_
    else:
        cache.set(cache_key, queryset, timeout)
    return queryset


class AdsQuerySet(QuerySet):
    def annotate_deal_state_count(self, state):
        return self.extra(
            select=SortedDict([
                ('num_%s' % state, "SELECT COUNT(*) FROM deals_deal "
                                   "WHERE deals_deal.ad_id = ads_ad.id "
                                   "AND state = %s"),
            ]),
            select_params=(str(state),)
        )


class AdsManager(Manager):

    def get_query_set(self):
        return AdsQuerySet(self.model, using=self._db)

    def annotate_deal_state_count(self, *args, **kwargs):
        return self.get_query_set().annotate_deal_state_count(*args, **kwargs)

    def featured(self, prefetch=True):
        queryset = self.filter(active=True, amount__gt=0)
        queryset = queryset.order_by('-featured', '-num_views', '-created')

        if prefetch:
            queryset = queryset.select_related('product_type')
            queryset = queryset.select_related('currency')
            queryset = queryset.prefetch_related('product_type')
            queryset = queryset.prefetch_related('business_domains')
            queryset = queryset.prefetch_related('images')

        return queryset

ad_localized = locale_model({
    'title': ('CharField', {
        'max_length': 64, 'blank': True, 'verbose_name': _('Title'), 'help_text': _('The title of your ad'), 'db_index': True}),
    'description': ('TextField', {
        'blank': True, 'verbose_name': _('Description'),
        'help_text': _('A detailed description of your ad. Use English language to reach a wider audience.')})
})
class Ad(ad_localized):
    """ Ad """

    objects = AdsManager()

    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Price / pcs'), help_text=_('Help text for the price'))
    currency = models.ForeignKey(Currency, related_name='+', verbose_name='Currency', help_text=_('Help text for the currency'))
    amount = models.IntegerField(verbose_name=_('Amount'), help_text=_('The amount of items you are selling.'))
    published = models.BooleanField(default=True, verbose_name='Published', help_text=_('Help text for published'), db_index=True)

    product_type = models.ForeignKey('ProductType', related_name='ads', verbose_name=_('Product type'), help_text=_('Help text for product type'))
    business_domains = models.ManyToManyField('BusinessDomain', related_name='ads', verbose_name=_('Business domains'), help_text=_('Help text for business domains'))

    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'), help_text=_('When the ad was last edited'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'), help_text=_('When the ad was created'))
    last_deal_updated = models.DateTimeField(verbose_name=_('Last Deal updated'), blank=True, null=True, help_text=_('When was the last deal updated'))

    active = models.BooleanField(default=True, verbose_name=_('Active'), help_text=_('Use this instead of deleting the ad'), db_index=True)
    creator = models.ForeignKey(UserProfile, verbose_name=_('Creator'), help_text=_('The person who created the ad'))
    owner = models.ForeignKey(BusinessProfile, verbose_name=_('Owner'), help_text=_('The business who owns the ad'))

    youtube_code = models.CharField(max_length=16, blank=True, null=True, verbose_name=_('Youtube url'), help_text=_('An url to a youtube-clip'))

    is_request = models.BooleanField(default=False, verbose_name=_('Buying'), help_text=_('If the ad is wanted'), db_index=True)

    featured = models.BooleanField(default=False, verbose_name=_('Featured'), help_text=_('Featured on the frontpage'), db_index=True)
    num_views = models.IntegerField(default=0, verbose_name=_('Number of views'), help_text=_('Total number of views this ad has'))

    notes = models.TextField(blank=True, verbose_name=_('Your own notes'), help_text=_('Your own notes is not visible to anyone else.'))

    def get_absolute_url(self):
        return reverse('ads:ad_detail', kwargs={'pk': self.pk})

    @property
    def float_price(self):
        return str(float(self.price))

    @property
    def total_price(self):
        return self.price * self.amount

    def user_has_perm(self, user_obj, perm):
        """
        :type user_obj: User
        """
        if perm == 'change_ad':
            if user_obj.is_anonymous():
                return False
            elif user_obj.get_business_profile().pk == self.owner.pk:
                return True
            else:
                return False

    def __unicode__(self):
        return self.get_localized('title', 'en')

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')


class Value(models.Model):
    """ The values for ProductType Fields for the Ad """

    ad = models.ForeignKey('Ad', related_name='value_set')
    field = models.ForeignKey('Field', related_name='value_set')
    value = models.CharField(max_length=256)
    choice_value = models.ForeignKey('FieldChoice', blank=True, null=True)
    min_value = models.CharField(max_length=128, blank=True, default="", help_text=_('Used for requests.'))
    max_value = models.CharField(max_length=128, blank=True, default="", help_text=_('Used for requests.'))

    def get_value(self):
        if self.field.type == 'ChoiceField':
            return self.choice_value
        else:
            return self.field.recast_value(self.value)

    def get_localized(self, field, language_code):
        if field == 'value':
            if self.field.type == 'ChoiceField' and self.choice_value:
                return self.choice_value.get_localized('name', language_code)
            elif self.field.type == 'BooleanField':
                value = self.get_value()
                if value:
                    return _('Yes')
                else:
                    return _('No')
            else:
                return self.get_value()
        else:
            return ''

    def __unicode__(self):
        return unicode(self.value or '')

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Ad product field value')
        verbose_name_plural = _('Ad product field values')


class BusinessDomain(locale_model('title')):
    """ The business domains that the Ad fits into """

    title = models.CharField(max_length=64)
    slug = AutoSlugField(always_update=True, populate_from='title', unique=True)
    is_unique = models.BooleanField(default=False, verbose_name=_('Is Unique'), help_text=_('If this business domain is selected no other business domain can be selected.'))
    def __unicode__(self):
        return self.title

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Business domain')
        verbose_name_plural = _('Business domains')
        ordering = ['title']


class ProductType(locale_model('title')):
    """ The product type that the Ad lies in """

    title = models.CharField(max_length=64)
    fields = models.ManyToManyField('Field', related_name='product_types',
        blank=True)
    product_categories = models.ManyToManyField('ProductCategory',
        related_name='product_types')
    slug = AutoSlugField(always_update=True, populate_from='title', unique=True)

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Product type')
        verbose_name_plural = _('Product types')
        ordering = ['title']

    def __unicode__(self):
        return self.title


class ProductCategory(locale_model('title')):
    """ The categories that the ProductType lies in """

    title = models.CharField(max_length=64)
    slug = AutoSlugField(always_update=True, populate_from='title', unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')
        ordering = ['title']


class Field(locale_model(['label', 'help_text'])):
    """ The fields for the ProductType """

    TYPE_CHOICES = (
        ('IntegerField', 'Natural number'),
        ('CharField', 'Textfield'),
        ('TextField', 'Textarea'),
        ('BooleanField', 'Checkbox'),
        ('DecimalField', 'Decimalfield'),
        ('ChoiceField', 'Choices'),
    )

    name = models.CharField(max_length=64)
    required = models.BooleanField()
    type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    suffix = models.CharField(max_length=4, blank=True)
    is_filterable = models.BooleanField(default=False)

    def recast_value(self, value):
        try:
            if self.type == 'IntegerField':
                return int(value)
            elif self.type == 'BooleanField':
                if value == 'False':
                    return False
                else:
                    return True
            elif self.type == 'DecimalField':
                return Decimal(value)
            else:
                return value
        except (TypeError, ValueError):
            return ''

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Product field')
        verbose_name_plural = _('Product fields')


class FieldChoice(locale_model('name')):
    name = models.CharField(max_length=32)
    field = models.ForeignKey(Field, related_name="field_choices")

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Product field choice')
        verbose_name_plural = _('Product field choices')


class AdImage(Image):
    ad = models.ForeignKey(Ad, verbose_name=_('Ad'), related_name='images', null=True, blank=True)

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Ad image')
        verbose_name_plural = _('Ad images')


class AdFile(File):
    ad = models.ForeignKey(Ad, verbose_name=_('Ad'), related_name='files', null=True, blank=True)

    def __unicode__(self):
        return str(self.filename)

    class Meta:
        app_label = string_with_title('ads', _('Ads'))
        verbose_name = _('Ad file')
        verbose_name_plural = _('Ad files')
