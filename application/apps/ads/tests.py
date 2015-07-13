# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.contrib.auth.models import User
from currencies.models import  Currency
from django.template import Template
from django.template import Context
from application.apps.ads.paginator import AdsPaginator
import forms
import models


class AdsTests(TestCase):

    fixtures = ['ads_test_data.json']

    def setUp(self):
        super(AdsTests, self).setUp()

        self.user = User.objects.create_user('tester@tester.com', 'tester@tester.com', 'password')

        Currency.objects.create(code='USD', name='US Dollars', symbol='$', factor=1, is_active=True, is_base=False,
            is_default=False)
        self.currency = Currency.objects.create(code='EUR', name='Euro', symbol='€', factor=1.3, is_active=True,
            is_base=False, is_default=True)

        business_profile = models.BusinessProfile(business_name="Test business",
            creator=self.user.get_userprofile())
        business_profile.save()

        self.user.get_userprofile().active_profile = business_profile
        self.user.get_userprofile().business_profiles.add(business_profile)
        self.user.get_userprofile().save()

        product_types = models.ProductType.objects.all()
        for x in range(len(product_types)):

            post_data = {
                'title': 'Title here',
                'description': 'Lorem ipsum dolor site amet.',
                'price': 5000,
                'amount': 1,
                'currency': self.currency.pk,
                'published': True,
                'product_type': product_types[x].pk,
                'business_domains': [domain.pk for domain in models.BusinessDomain.objects.all()],
            }

            for field in product_types[x].fields.all():
                post_data['values[%s]' % field.pk] = field.recast_value(str(x))

            form = forms.AdForm(data=post_data or None, user=self.user)

            if form.is_valid():
                form.instance.creator = self.user.get_userprofile()
                form.instance.owner = self.user.get_business_profile()
                form.save()

    def test_create_ad(self):

        product_type = models.ProductType.objects.all()[0]

        post_data = {
            'title': 'Title here',
            'description': 'Lorem ipsum dolor site amet.',
            'price': 5000,
            'amount': 1,
            'currency': self.currency.pk,
            'published': True,
            'product_type': product_type.pk,
            'business_domains': [domain.pk for domain in models.BusinessDomain.objects.all()],
        }

        for field in product_type.fields.all():
            post_data['values[%s]' % field.pk] = field.recast_value('666')

        form = forms.AdForm(post_data or None)

        if form.is_valid():
            form.instance.creator = self.user.get_userprofile()
            form.instance.owner = self.user.get_business_profile()
            ad = form.save()
        else:
            self.fail(form.errors)

        db_ad = models.Ad.objects.get(pk=ad.pk)

        self.failUnless(db_ad.title == ad.title)
        self.failUnless(db_ad.description == ad.description)
        self.failUnless(db_ad.price == ad.price)
        self.failUnless(db_ad.amount == ad.amount)
        self.failUnless(db_ad.published == ad.published)
        self.failUnless(db_ad.active == ad.active)
        self.failUnless(db_ad.product_type == ad.product_type)

        for domain in ad.business_domains.all():
            self.failUnless(domain in db_ad.business_domains.all())

        for value in ad.value_set.all():
            self.failUnless(value in db_ad.value_set.all())

    def test_update_ad(self):
        ad = models.Ad.objects.get(pk=1)

        # First a GET to get the form and populate it.
        form = forms.AdForm(user=self.user, instance=ad)
        post_data = form.initial.copy()

        # Change the form-data before post
        post_data['title'] = 'A new title'

        # Then a POST with the form-data
        form = forms.AdForm(post_data or None, instance=ad)

        if form.is_valid():
            ad = form.save()
        else:
            self.fail(form.errors)

        db_ad = models.Ad.objects.get(pk=ad.pk)

        self.failUnless(db_ad.title == ad.title)
        self.failUnless(db_ad.description == ad.description)
        self.failUnless(db_ad.price == ad.price)
        self.failUnless(db_ad.amount == ad.amount)
        self.failUnless(db_ad.published == ad.published)
        self.failUnless(db_ad.active == ad.active)
        self.failUnless(db_ad.product_type == ad.product_type)

        for domain in ad.business_domains.all():
            self.failUnless(domain in db_ad.business_domains.all())

        for value in ad.value_set.all():
            self.failUnless(value in db_ad.value_set.all())

    def test_filter(self):
        ad = models.Ad.objects.all()[0]
        business_domain = ad.business_domains.all()[0]
        product_type = ad.product_type
        product_category = product_type.product_categories.all()[0]

        filter_data = {
            'search': 'Title',
            'business_domain': business_domain.slug,
            'product_category': product_category.slug,
            'product_type': product_type.slug
        }

        filter_form = forms.AdsFilter(filter_data)

        if filter_form.is_valid():
            ads = filter_form.filter()
        else:
            self.fail('The filter has form-errors: %s' % filter_form.errors)

        self.failUnless(ads.count() > 0)
        self.failUnless(ad.pk in [a.pk for a in ads])
        self.failUnless(filter_data['search'] in ads[0].title)
        self.failUnless(filter_data['product_type'] == ads[0].product_type.slug)

    def test_ad_list_sidebar_template_tag(self):
        template = Template("""
            {% load ads_extras %}
            {% ad_filter_sidebar form %}
        """)

        form = forms.AdsFilter(None)
        context = Context({'form': form})
        out = template.render(context)

        for choice in form.fields['business_domain'].choices:
            self.failUnless(choice[0] in out)

    def test_order_by_link(self):

        for order_by in ('created', '-created'):
            form = forms.AdsFilter({'order_by': order_by})
            template = Template("""
                {% load ads_extras %}
                {% order_by_link 'Test' 'created' form %}
            """)

            context = Context({'form': form})
            out = template.render(context)

            if order_by == 'created':
                self.failUnless('=-created' in out)
            elif order_by == '-created':
                self.failUnless('=created' in out)

    def test_view_ad(self):
        ad = models.Ad.objects.all()[0]
        client = Client()

        response = client.get(ad.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_ads_paginator(self):
        per_page = 10
        num_items = 100
        num_firstpage = 5
        expected_num_pages = 11

        items = range(num_items)
        paginator = AdsPaginator(items, per_page, deltafirst=per_page-num_firstpage)
        last_item = paginator.page(paginator.num_pages).object_list[-1]

        self.assertEqual(len(paginator.page(1)), num_firstpage)
        self.assertEqual(paginator.num_pages, expected_num_pages)
        self.assertEqual(last_item, items[-1])

