import math
from operator import __or__
import re
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.utils.text import Truncator
from django import forms
from django.db.models import Count, Q
from django.utils.http import urlencode
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from currencies.models import Currency
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from application import settings
from application.apps.locale.fields import LocalizedModelChoiceField, LocalizedModelMultipleChoiceField
from application.libs.angularjs.forms import AngularSelect
import models


class AdForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    YOUTUBE_REGEX = r'.*(?:youtube|youtu)(?:\.[a-z]{1,5}).*(?:v\=|vi\=|\/)([\w\-_]+).*'

    product_category = LocalizedModelChoiceField(queryset=models.ProductCategory.objects.all(), required=False,
                                                 empty_label=_('Choose here'), label=_('Product category'),
                                                 model_field='title')
    images = forms.MultipleChoiceField(required=False, widget=forms.MultipleHiddenInput())
    files = forms.MultipleChoiceField(required=False, widget=forms.MultipleHiddenInput())
    youtube_code = forms.URLField(required=False, label=_('Youtube URL'), help_text=_('An url to a youtube-clip'))

    product_type = LocalizedModelChoiceField(queryset=models.ProductType.objects.all(), model_field='title')
    business_domains = LocalizedModelMultipleChoiceField(queryset=models.BusinessDomain.objects.all(),
                                                         model_field='title', label=_('Business domains'))

    product_info = forms.Field(required=False)

    class Meta:
        model = models.Ad
        exclude = ('creator', 'owner', 'active', 'updated', 'created', 'last_deal_updated', 'num_views', 'published')
        widgets = {
            'product_type': AngularSelect(
                options_tmpl='<option ng-repeat="c in fields.product_type.choices" value="{! c.key !}">{! c.value !}</option>')
        }

    def __init__(self, *args, **kwargs):
        self.language_code = kwargs.pop('language_code')
        self.user = kwargs.pop('user')
        if 'data' in kwargs and 'price' not in kwargs['data'] and 'quote_wanted' in kwargs['data']:
            kwargs['data']['price'] = 0
        super(AdForm, self).__init__(*args, **kwargs)

        self.fields['product_category'].locale = self.language_code
        self.fields['product_type'].locale = self.language_code
        self.fields['business_domains'].locale = self.language_code

        self.fields['product_category'].queryset.order_by('title_{0}'.format(self.language_code))
        self.fields['product_type'].queryset.order_by('title_{0}'.format(self.language_code))
        self.fields['business_domains'].queryset.order_by('title_{0}'.format(self.language_code))

        self.fields['price'].widget.attrs['ng-model'] = 'fields.price.value'
        self.fields['price'].widget.attrs['ng-disabled'] = 'quote_wanted'
        self.fields['price'].widget.attrs['autocomplete'] = 'off'
        self.fields['currency'].widget.attrs['ng-model'] = 'fields.currency.value'

        if self.initial.get('id'):
            self.initial['images'] = [img.pk for img in self.instance.images.all()]
            self.initial['files'] = [file.pk for file in self.instance.files.all()]
            if self.initial.get('youtube_code'):
                self.initial['youtube_code'] = 'http://www.youtube.com/watch?v=%s' % self.instance.youtube_code

        self._create_fields()

    def _create_fields(self):
        form_data = self.data.copy()
        form_data.update(self.initial.copy())
        values = []
        self._db_fields = dict()

        if form_data.get('id'):
            self.fields['images'].choices = [(c.pk, c.get_thumb('list_thumb')) for c in
                                             models.AdImage.objects.filter(Q(creator=self.user) | Q(ad=self.instance))]
            self.fields['files'].choices = [(f.pk, f.filename) for f in
                                            models.AdFile.objects.filter(Q(creator=self.user) | Q(ad=self.instance))]
        else:
            self.fields['images'].choices = [(c.pk, c.get_thumb('list_thumb')) for c in
                                             models.AdImage.objects.filter(creator=self.user)]
            self.fields['files'].choices = [(f.pk, f.filename) for f in models.AdFile.objects.filter(creator=self.user)]

        self.fields['currency'].default = Currency.objects.get(is_default=True)

        for lang_code, lang_name in settings.LANGUAGES:
            self.fields['description_{0}'.format(lang_code)].widget.attrs['rows'] = 4

        self.fields['notes'].widget.attrs['rows'] = 4
        self.fields['product_category'].widget.attrs['ng-model'] = 'fields.product_category.value'
        self.fields['product_type'].empty_label = ugettext('Choose here')
        self.fields['product_type'].widget.attrs['ng-model'] = 'fields.product_type.value'
        self.fields['product_type'].widget.attrs['ui-select2'] = ''
        self.fields['product_type'].widget.attrs['ng-disabled'] = 'fields.product_type.loading'
        self.fields['youtube_code'].widget.attrs['maxlength'] = ''

        currency_choices = list(self.fields['currency'].choices)
        del currency_choices[0]
        self.fields['currency'].choices = currency_choices

        self.fields['business_domains'].widget.attrs['placeholder'] = self.fields['business_domains'].label

        if form_data.get('product_category'):
            self.fields['product_type'].queryset = models.ProductType.objects.filter(
                product_categories__pk=form_data.get('product_category'))

        if form_data.get('id', False):
            values = models.Value.objects.filter(ad__pk=self.instance.pk)

        if form_data.get('product_type', False):
            product_type = form_data.get('product_type')
            fields_queryset = models.Field.objects.filter(product_types__pk=product_type)

            for field in fields_queryset:
                field_name = 'values_%s' % str(field.pk)
                initial = self._value_for_field(values, field)

                self._db_fields[field_name] = field
                self.fields[field_name] = self._create_field(field)
                if form_data.get('is_request'):
                    self.fields[field_name].required = False
                self.initial[field_name] = initial

    def _value_for_field(self, values, field):
        for value in values:
            if value.field == field:
                return value.get_value()
        return None

    def _create_field(self, field):
        f = getattr(forms, field.type)(
            required=field.required,
            label=field.get_localized('label', self.language_code),
            help_text=field.get_localized('help_text', self.language_code),
        )

        if field.type == 'ChoiceField':
            f.choices = [('', ugettext('Choose here'))]
            f.choices += [(choice.pk, choice.get_localized('name', self.language_code)) for choice in
                          field.field_choices.all()]
            f.widget.attrs['ui-select2'] = ''

        f.widget.attrs['ng-model'] = 'fields.values_%s.value' % field.pk

        return f

    def product_type_fields(self):
        fields = []
        for f in self.fields:
            if re.match(r'^values', f):
                fields.append((self[f], self._db_fields[f]))
        return fields

    def clean_business_domains(self):
        business_domains = self.cleaned_data.get('business_domains')

        for domain in business_domains:
            if domain.is_unique and len(business_domains) > 1:
                raise ValidationError(_("%s can't be comined with other business domains")
                                      % domain.get_localized('title', self.language_code))

        return business_domains

    def clean_youtube_code(self):
        url = self.cleaned_data.get('youtube_code')
        if url:
            matches = re.match(self.YOUTUBE_REGEX, url)
            if matches:
                try:
                    return matches.group(1)
                except IndexError:
                    raise ValidationError(_('We can not find this youtube video.'))
            else:
                raise ValidationError(_('We can not find this youtube video.'))

    def clean_product_info(self):
        for lang_code, lang_name in settings.LANGUAGES:
            title_field = self.cleaned_data['title_{0}'.format(lang_code)]
            descr_field = self.cleaned_data['description_{0}'.format(lang_code)]

            # bail out early if both are filled.
            if title_field and descr_field:
                return

        raise ValidationError(_('Please fill out product information for at least one language'))

    def clean_amount(self):
        amount = int(self.cleaned_data.get('amount'))
        if amount > 0:
            return amount
        else:
            raise ValidationError('Needs to be at least 1.')

    def is_valid(self):
        is_valid = super(AdForm, self).is_valid()
        return is_valid

    def _save_images(self, ad):
        # cleanup old images.
        for image in ad.images.all():
            image.ad = None
            image.save()

        # insert new images.
        for image_id in self.cleaned_data.get('images'):
            try:
                image = models.AdImage.objects.get(pk=image_id)
            except models.AdImage.DoesNotExist:
                continue
            image.ad = ad
            image.save()

    def _save_files(self, ad):
        # cleanup
        for file in ad.files.all():
            file.ad = None
            file.save()

        # insert new
        for file_id in self.cleaned_data.get('files'):
            try:
                file = models.AdFile.objects.get(pk=file_id)
            except models.AdFile.DoesNotExist:
                continue
            file.ad = ad
            file.save()

    def _save_values(self, ad):
        # cleanup old values
        models.Value.objects.filter(ad__pk=ad.pk).delete()

        # insert new values
        product_type = ad.product_type
        fields = product_type.fields
        for field in fields.all():
            cleaned_value = self.cleaned_data.get('values_%s' % str(field.pk), None)
            if cleaned_value or field.type == 'BooleanField':
                kwargs = {'field': field, 'ad': ad, 'value': cleaned_value}
                if field.type == 'ChoiceField':
                    kwargs['choice_value'] = models.FieldChoice.objects.get(pk=cleaned_value)

                kwargs['value'] = cleaned_value
                instance = models.Value(**kwargs)
                instance.save()

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.creator = self.user.get_userprofile()
            self.instance.owner = self.user.get_business_profile()

            created = ADDITION
        else:
            created = CHANGE
        ad = super(AdForm, self).save(commit=commit)
        self._save_images(ad)
        self._save_files(ad)
        self._save_values(ad)

        LogEntry.objects.log_action(
            user_id=self.user.pk,
            content_type_id=ContentType.objects.get_for_model(ad).pk,
            object_id=ad.pk,
            object_repr='(Frontend)' + force_unicode(ad),
            action_flag=created
        )

        return ad


class AdImageForm(forms.ModelForm):
    EXTENSION_WHITELIST = ('jpg', 'jpeg', 'png')

    class Meta:
        model = models.AdImage
        fields = ('image_filename', )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AdImageForm, self).__init__(*args, **kwargs)

        self.instance.creator = user

    def clean_image_filename(self):
        image = self.cleaned_data.get('image_filename', None)
        extension = image.name.rpartition('.')[2].lower()
        if image:
            if extension not in self.EXTENSION_WHITELIST:
                raise ValidationError(
                    _('Invalid extension. Valid extensions are: {0}.'.format(', '.join(self.EXTENSION_WHITELIST))))
            if image.size > 8 * 1024 * 1024:
                raise ValidationError(_('Image to large (> 8mb)'))
        else:
            raise ValidationError(_('Could not read uploaded image'))

        return image


class AdFileForm(forms.ModelForm):
    class Meta:
        model = models.AdFile
        fields = ('filename', )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AdFileForm, self).__init__(*args, **kwargs)

        self.instance.creator = user


class AdsFilter(forms.Form):
    ALL = 'all'
    FILTER_CHOICES_TRUNCATE = 20
    AUTOFILTER_ROWS = 5
    CHOICES_CACHE_TIMEOUT = 1800 # in seconds (30 min)
    ORDER_BY_CHOICES = (
        ('-created', _('Created ascending')),
        ('created', _('Created descending')),

        ('-title', _('Title ascending')),
        ('title', _('Title descending')),

        ('-price', _('Price ascending')),
        ('price', _('Price descending')),

        ('converted_price', _('Converted price ascending')),
        ('-converted_price', _('Converted price descending'))
    )

    search = forms.CharField(required=False, label=_('Ads on Bidpart'))
    product_category = forms.ChoiceField(required=False)
    product_type = forms.ChoiceField(required=False)
    business_domain = forms.ChoiceField(required=False)
    order_by = forms.ChoiceField(required=False, choices=ORDER_BY_CHOICES)
    show_buy_sell = forms.ChoiceField(initial=settings.SHOW_BUY_SELL_DEFAULT,
                                      choices=settings.SHOW_BUY_SELL)

    order_by_default_field = '-created'

    filter_names = []
    _fields = None

    exclude_get_params = ('show_buy_sell', 'language_code', 'to_currency')

    def __init__(self, *args, **kwargs):
        self.language_code = kwargs.pop('language_code')
        super(AdsFilter, self).__init__(*args, **kwargs)

        self.fields['business_domain'].choices = self._business_domain_choices()
        self.fields['product_category'].choices = self._product_category_choices()

        if not self.data.get('business_domain'):
            self.data['business_domain'] = self.ALL

        if self.data.get('product_category'):
            self.fields['product_type'].choices = self._product_type_choices()

        if self.data.get('product_type'):
            self._fields = models.Field.objects.filter(
                product_types__slug=self.data.get('product_type'), is_filterable=True)

            ads_queryset = self.all(prefetch=False)
            ads_queryset = self._filter(queryset=ads_queryset, data=self.data)
            ads_queryset = self._filter_fields(ads_queryset, data=self.data)
            ads_queryset = ads_queryset.only('pk')
            ads_pks = [ad.pk for ad in ads_queryset]

            for field in self._fields:
                filter_name = 'f_%i' % field.pk
                self.filter_names.append(filter_name)
                self.fields[filter_name] = forms.ChoiceField(label=field.get_localized('label', self.language_code),
                                                             help_text=field.get_localized('help_text',
                                                                                           self.language_code),
                                                             required=False)

                self.fields[filter_name].choices = self._filter_choices(field, filter_name, ads_pks)

    def _product_type_choices(self):
        choices = list()

        ads = self.all(prefetch=False)
        if self.data.get('business_domain') and self.data.get('business_domain') != self.ALL:
            ads = ads.filter(business_domains__slug=self.data.get('business_domain'))

        ads = ads.filter(product_type__product_categories__slug=self.data.get('product_category'))
        ads = ads.filter(active=True, published=True).only('pk')

        types = models.ProductType.objects.filter(ads__in=ads)
        types = types.annotate(num_ads=Count('ads__pk'))
        types = types.order_by('title')

        for type in types:
            choice = (type.slug, '%s (%s)' % (type.get_localized('title', self.language_code),
                                              type.num_ads))
            choices.append(choice)

        return choices

    def _product_category_choices(self):
        choices = list()

        ads = self.all(prefetch=False)
        if self.data.get('business_domain') and self.data.get('business_domain') != self.ALL:
            ads = ads.filter(business_domains__slug=self.data.get('business_domain'))

        ads = ads.filter(active=True, published=True).only('pk')

        categories = models.ProductCategory.objects.filter(product_types__ads__in=ads)
        categories = categories.annotate(num_ads=Count('product_types__ads__pk'))
        categories = categories.order_by('title_%s' % self.language_code)

        for category in categories:
            choice = (category.slug, '%s (%s)' % (category.get_localized('title', self.language_code),
                                                  category.num_ads))
            choices.append(choice)

        return choices

    def _business_domain_choices(self):
        choices = [(self.ALL, _('All business domains'))]

        ads = self.all(prefetch=False)
        ads = ads.filter(active=True, published=True).only('pk')

        business_domains = models.BusinessDomain.objects.filter(ads__in=ads)
        business_domains = business_domains.annotate(num_ads=Count('ads__pk'))
        business_domains = business_domains.order_by('title')

        for domain in business_domains:
            choice = (domain.slug, '%s (%s)' % (domain.title, domain.num_ads))
            choices.append(choice)

        return choices

    def _filter_choices(self, field, filter_name, ads_pks):
        choices = list()
        name_localized = None

        if self.data.get(filter_name, False):
            filter = self.data[filter_name]
            if field.type == 'ChoiceField':
                choice_name = models.FieldChoice.objects.get(pk=filter).get_localized('name', self.language_code)
                choices.append((filter, Truncator(choice_name).chars(self.FILTER_CHOICES_TRUNCATE)))
            else:
                choices.append((filter, Truncator(filter).chars(self.FILTER_CHOICES_TRUNCATE)))
            return choices

        value_set = field.value_set.all()
        value_set = value_set.filter(ad__in=ads_pks)

        if field.type == 'ChoiceField':
            value_set = value_set.exclude(choice_value=None)
            name_localized = 'choice_value__name_%s' % self.language_code
            values = value_set.values('choice_value', name_localized).distinct().annotate(
                num_ads=Count('ad__pk'))
        else:
            value_set = value_set.exclude(value='')
            values = value_set.values('value').distinct().annotate(num_ads=Count('ad__pk'))

        if field.type == 'IntegerField' and values.count() > self.AUTOFILTER_ROWS:
            values = sorted(list(values), key=lambda row: int(row['value']) if row['value'].isdigit() else 0)
            values = list(reversed(values))

            count = min(len(values), self.AUTOFILTER_ROWS)
            incr = int(math.ceil(math.ceil(float(len(values)) / float(count))))

            for i in range(count):
                start = incr * i
                stop = (incr * (i + 1))

                values_range = values[start:stop]

                if not len(values_range):
                    break

                num_ads = 0
                for val in values_range:
                    num_ads += val['num_ads']

                val = '%s-%s' % (values_range[-1]['value'], values_range[0]['value'])
                name = '%s (%s)' % (val, num_ads)

                choices.append((val, name))
            return choices
        elif field.type == 'ChoiceField':
            for value in values:
                key = value['choice_value']
                value['value'] = Truncator(value[name_localized]).chars(
                    self.FILTER_CHOICES_TRUNCATE - (len(str(value['num_ads'])) + 2))
                value = '%s (%i)' % (value['value'], value['num_ads'])
                choices.append((key, value))

            return choices
        else:
            for value in values:
                key = value['value']
                value['value'] = Truncator(value['value']).chars(
                    self.FILTER_CHOICES_TRUNCATE - (len(str(value['num_ads'])) + 2))
                value = '%s (%i)' % (value['value'], value['num_ads'])
                choices.append((key, value))

            return choices

    def _create_field(self, field):
        return getattr(forms, field.type)(
            label=field.label,
            help_text=field.suffix,
            required=False
        )

    def is_request(self):
        if self.data.get('show_buy_sell', '') == 'sell':
            return False
        elif self.data.get('show_buy_sell', '') == 'buy':
            return True
        else:
            return None

    def filter_fields(self):
        fields = []
        for f in self.fields:
            if re.match(r'^f_[0-9]+', f):
                fields.append((f, self.fields[f]))
        return fields

    def all(self, prefetch=True):
        queryset = models.Ad.objects.filter(amount__gt=0)
        queryset = queryset.filter(active=True, published=True)

        if self.is_request() is not None:
            queryset = queryset.filter(is_request=self.is_request())

        if prefetch:
            queryset = queryset.select_related('product_type')
            queryset = queryset.select_related('currency')
            queryset = queryset.prefetch_related('business_domains')
            queryset = queryset.prefetch_related('images')

        return queryset

    def get_absolute_url(self, kwargs=None):
        temp_data = self.data.copy()

        for to_pop in self.exclude_get_params:
            if to_pop in temp_data.keys():
                temp_data.pop(to_pop)

        if kwargs:
            temp_data.update(kwargs)

        for key in temp_data.keys():
            if not temp_data[key]:
                temp_data.pop(key)

        url_args = []
        for i, url_key in enumerate(('business_domain', 'product_category', 'product_type')):
            value = temp_data.pop(url_key, None)
            if value:
                url_args.append(value)
            else:
                break

        if len(temp_data):
            return '%s?%s' % (reverse('ads:ad_filter', args=url_args or None), urlencode(temp_data))
        else:
            return reverse('ads:ad_filter', args=url_args or None)

    def _filter_fields(self, queryset, data):
        for field in self._fields:
            value = data.get('f_%i' % field.pk, None)

            queryset = queryset.filter(value_set__field__pk=field.pk)
            if value:
                match = re.match('^([0-9]+)-([0-9]+)$', value)
                if match:
                    if match.group(1).isdigit() and match.group(2).isdigit():
                        from_ = int(match.group(1))
                        to = int(match.group(2))

                        # dirty fix, get the alias so the extra gets on correct.
                        alias = queryset.query.where.children[-1].children[-1][0].alias
                        # dirty fix, value is a charfield, django autmaticly casts digits to strings.
                        queryset = queryset.extra(
                            where=['{0}.value >= %s'.format(alias), '{0}.value <= %s'.format(alias)],
                            params=[from_, to]
                        )
                elif field.type == 'ChoiceField':
                    queryset = queryset.filter(value_set__choice_value__pk=value)
                else:
                    queryset = queryset.filter(value_set__value=value)

        return queryset

    def _filter(self, queryset, data):
        kwargs = {}
        if data.get('search'):
            q_objects = []
            for lang_code, lang_name in settings.LANGUAGES:
                q_objects.append(Q(**{
                    'title_{0}__icontains'.format(lang_code): data['search']
                }))
            queryset = queryset.filter(reduce(__or__, q_objects))

        if data.get('product_type'):
            kwargs['product_type__slug'] = data['product_type']
        if data.get('business_domain') and data.get('business_domain') != self.ALL:
            kwargs['business_domains__slug'] = data['business_domain']
        if data.get('product_category'):
            kwargs['product_type__product_categories'] = models.ProductCategory.objects.filter(
                slug=data['product_category'])

        return queryset.filter(**kwargs)

    def _order_by(self, queryset, data):
        if data.get('order_by', None):
            order_by = data['order_by']
        else:
            order_by = self.order_by_default_field

        if 'title' in order_by:
            order_by_list = ['{0}_{1}'.format(order_by, self.language_code)]
            for lang_code, lang_name in settings.LANGUAGES:
                if lang_code != self.language_code:
                    order_by_list.append('{0}_{1}'.format(order_by, lang_code))
            queryset = queryset.order_by(*order_by_list)
        elif 'converted_price' in order_by:
            queryset = queryset.select_related('currency')
            queryset = queryset.extra(
                select={'converted_price': 'price * (%s / ' + ('%s.factor)' % Currency._meta.db_table)},
                select_params=(self.data['to_currency'].factor,),
                order_by=[order_by, ]
            )
        else:
            queryset = queryset.order_by(order_by)

        return queryset

    def filter(self):
        data = self.cleaned_data

        queryset = self.all()
        queryset = self._filter(queryset, data)

        if data.get('product_type', None):
            queryset = self._filter_fields(queryset=queryset, data=data)

        queryset = self._order_by(queryset, data)

        return queryset
