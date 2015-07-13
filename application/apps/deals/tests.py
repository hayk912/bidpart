# coding=utf-8
from datetime import timedelta
from decimal import Decimal
import random
import string
from time import mktime
from currencies.models import Currency
from django.contrib.auth.models import User
from django.core import mail
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from application import settings
from application.apps.accounts.forms import SignupForm
from application.apps.accounts.models import UserProfile, BusinessProfile
from application.apps.accounts.tests import create_users
from application.apps.ads.models import Ad, ProductType, ProductCategory, BusinessDomain
from application.apps.deals.forms import DealForm, CreateDealForm
from application.apps.deals.models import Deal
from application.apps.invoice.models import Invoice
import func

class DealsTests(TestCase):
    #fixtures = ['test_data.json']

    def test_commission_level(self):

        settings.COMMISSION_LEVELS = (
            (0, 0.10),
            (10000, 0.09),
            (20000, 0.08),
            (30000, 0.07),
            (40000, 0.06),
            (50000, 0.05),
            (60000, 0.04),
            (70000, 0.03),
        )

        deals_sum = Decimal('0')
        price = Decimal('20000')
        commission = func.calc_commission(price, deals_sum, settings.COMMISSION_LEVELS)
        self.assertEqual(commission, 1900)


class DealsApiTest(TestCase):

    def setUp(self):
        create_users(10)
        self.users = list(User.objects.all())

        self._create_ads()
        self._create_deals()
        self.ads = Ad.objects.all()

    def _create_ads(self):
        def get_or_create_product_category():
            return ProductCategory.objects.get_or_create(pk=random.randint(1,10), defaults={
                'title':''.join([random.choice(string.ascii_letters) for x in range(15)]),
            })[0]
        def get_or_create_business_domain():
            return BusinessDomain.objects.get_or_create(pk=random.randint(1,10), defaults={
                'title':''.join([random.choice(string.ascii_letters) for x in range(15)]),
            })[0]

        for i in range(30):
            currency, created = Currency.objects.get_or_create(
                code='EUR',
                defaults={
                    'code':'EUR',
                    'name':'Euro',
                    'symbol': '€',
                    'factor':1,
                    'is_active':True,
                    'is_base': True,
                    'is_default': True
                }
            )
            product_type, created = ProductType.objects.get_or_create(pk=random.randint(1,10), defaults={
                'title':''.join([random.choice(string.ascii_letters) for x in range(15)])
            })
            product_type.product_categories = [get_or_create_product_category() for x in range(3)]
            product_type.save()

            user = random.choice(self.users)
            ad = Ad(
                title=''.join([random.choice(string.ascii_letters) for x in range(15)]),
                price=''.join([random.choice(string.digits) for x in range(4)]),
                currency=currency,
                amount=random.randint(1,10),
                published=True,
                product_type=product_type,
                active=True,
                creator=user.get_userprofile(),
                owner=user.get_business_profile()
            )
            ad.save()
            ad.business_domains.add(*[get_or_create_business_domain() for x in range(3)])
            ad.save()

    def _create_deals(self):
        ads = Ad.objects.all()

        for i in range(10):
            ad = random.choice(ads)

            while True:
                try:
                    creator_user = random.choice(self.users)

                    amount = random.randint(1,ad.amount)
                    factor = random.uniform(0.85, 1.15)
                    unit_price = float(ad.price) * factor
                    bid = unit_price * amount
                    bid = Decimal(bid).quantize(Decimal('.00'))
                    deal = Deal(
                        ad=ad,
                        creator=creator_user.get_userprofile(),
                        owner=creator_user.get_business_profile(),
                        bid=bid,
                        currency=ad.currency,
                        amount=amount
                    )
                    deal.save()
                except IntegrityError:
                    continue

                break

        self.deals = Deal.objects.all()

    def _deal_form(self, data, deal):
        return DealForm(data=data, instance=deal, user=deal.ad.creator.user)

    def test_do_interest(self):
        ads = Ad.objects.all()

        for ad in ads:
            amount = random.randint(1, ad.amount)
            bid = ad.price * amount

            form = CreateDealForm(data={
                'ad': ad.pk,
                'bid': bid,
                'amount': amount
            }, user=random.choice(self.users))

            if form.is_valid():
                deal = form.save()
            else:
                self.fail(dict(form.errors))

            self.assertEqual(deal.state, 'interested')
            self.assertEqual(deal.bid, bid)
            self.assertEqual(deal.ad.pk, ad.pk)
            self.assertEqual(deal.amount, amount)

    def test_do_activate(self):
        for deal in self.deals:
            form = self._deal_form({
                'action':deal.ACTIVATE
            }, deal)

            if form.is_valid():
                form.save()
            else:
                self.fail(dict(form.errors))

            self.assertEqual(deal.state, 'active')
            self.assertEqual(mktime(deal.renewed.timetuple()), mktime(timezone.now().timetuple()))

    def test_fail_activate(self):
        for deal in self.deals:
            # set the deal to canceled first (you can not activate a canceled deal)
            deal.do_action(deal.CANCEL, cancel_reason='Testing')

            form = self._deal_form({
                'action':deal.ACTIVATE
            }, deal)

            if form.is_valid():
                self.fail(dict(form.errors))

            self.assertEqual(deal.state, 'canceled')

    def test_do_extend(self):
        for deal in self.deals:

            deal.do_action(deal.ACTIVATE) # can't extend unless it is active.

            # pretend it was extended yesterday.
            deal.renewed = deal.renewed - timedelta(days=1)
            deal.save()

            form = self._deal_form({
                'action':deal.EXTEND
            }, deal)

            if form.is_valid():
                form.save()
            else:
                self.fail(dict(form.errors))

            self.assertEqual(mktime(deal.renewed.timetuple()), mktime(timezone.now().timetuple()))
            self.assertEqual(deal.state, 'active')

    def test_fail_extend(self):
        for deal in self.deals:
            # can't extend unless it's active.
            form = self._deal_form({
                'action':deal.EXTEND
            }, deal)

            if form.is_valid():
                self.fail(dict(form.errors))

            self.assertEqual(deal.state, 'interested')

    def test_do_cancel(self):
        for deal in self.deals:
            cancel_reason = 'Test cancel.'
            deal.do_action(deal.ACTIVATE)

            form = self._deal_form({
                'action':deal.CANCEL,
                'cancel_reason':cancel_reason
            }, deal)

            if form.is_valid():
                form.save()
            else:
                self.fail(dict(form.errors))

            self.assertEqual(deal.state, 'canceled')
            self.assertEqual(deal.cancel_reason, cancel_reason)

    def test_fail_cancel(self):
        for deal in self.deals:
            # deal is not activated, should not be able to cancel it then.
            cancel_reason = 'Test cancel.'

            form = self._deal_form({
                'action':deal.CANCEL,
                'cancel_reason':cancel_reason
            }, deal)

            if form.is_valid():
                self.fail(dict(form.errors))

            self.assertEqual(deal.state, 'interested')
            self.assertNotEqual(deal.cancel_reason, cancel_reason)

    def test_do_complete(self):
        sell_fully = True
        for deal in self.deals:
            # set to active first.
            deal.do_action(deal.ACTIVATE)

            if deal.ad.amount == 0: # if the ad already has sold everything, we test this later
                continue

            amount = min(deal.ad.amount, deal.amount) # just in case we sold some before this deal, we test this later.

            if sell_fully:
                amount = deal.ad.amount
                sell_fully = False

            form = self._deal_form({
                'action':deal.COMPLETE,
                'price':deal.bid,
                'amount':amount
            }, deal)

            if form.is_valid():
                form.save()
            else:
                self.fail(dict(form.errors))

            invoice = Invoice.objects.get(row__deal__pk=deal.pk)
            row = invoice.row_set.all()[0]

            if amount == deal.ad.amount:
                self.assertEqual(deal.ad.amount, 0)
                self.assertEqual(deal.ad.published, False)

            self.assertEqual(deal.commission, invoice.total_price)
            self.assertEqual(invoice.row_set.count(), 1)
            self.assertEqual(row.deal.pk, deal.pk)
            self.assertEqual(row.price, deal.commission)

            self.assertEqual(deal.state, 'completed')

    def test_fail_complete(self):
        for deal in self.deals:
            # set to active first.
            deal.do_action(deal.ACTIVATE)

            for amount in [-1, deal.ad.amount+1, None]:
                form = self._deal_form({
                    'action':deal.COMPLETE,
                    'price':deal.bid,
                    'amount':amount
                }, deal)

                if form.is_valid():
                    self.fail('Form should fail, we have invalid amount!')

                self.assertRaises(Invoice.DoesNotExist, Invoice.objects.get, row__deal__pk=deal.pk)

                self.assertEqual(deal.state, 'active')

    def test_manual_processing(self):
        for deal in self.deals:
            deal.do_action(deal.ACTIVATE)

            if deal.ad.published == False:
                continue

            # we want at least two items to be sellable
            deal.ad.amount = random.randint(2, 5)
            deal.ad.save()

            if deal.ad.amount < 2:
                continue

            form = self._deal_form({
                'action': deal.COMPLETE,
                'price': deal.ad.price, # two for the price of one
                'amount': 2
            }, deal)

            if form.is_valid():
                form.save()
            else:
                self.fail(dict(form.errors))

            self.assertEqual(deal.state, 'completed')
            self.assertEqual(deal.manual_processing, True)


    def test_send_pdf_attatchment(self):
        deal = self.deals[0]
        deal.do_action(deal.COMPLETE, amount=1, end_price=deal.ad.price)

        self.assertEqual(len(mail.outbox), 2)

