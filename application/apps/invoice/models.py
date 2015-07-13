# coding=utf-8
import datetime
from decimal import Decimal
import subprocess
import threading
import urlparse
from currencies.models import Currency
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
import os
from django.db.models.signals import post_save
import uuid
import hashlib
from django.utils.translation import ugettext_lazy as _
from application.apps.deals.models import Deal
from application.apps.accounts.models import BusinessProfile
from application.apps.accounts.functions import string_with_title


VAT = Decimal('0.25')


class SavePDFCommand(object):
    def __init__(self, url, pdf_path):
        url = settings.SITE_URL + url
        self.cmd = 'wkhtmltopdf %s %s' % (url, pdf_path)
        self.process = None

    def run(self, timeout=15):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()


class Invoice(models.Model):
    STATES = (
        ('created', 'Created (not sent)'),
        ('sent', 'Sent'),
        ('paid', 'Paid')
    )

    receiver = models.ForeignKey(BusinessProfile, blank=True, null=True)
    title = models.CharField(verbose_name=_('Invoice title'), default=_('Commission Invoice'), max_length=64)
    our_reference = models.ForeignKey(User, null=True, blank=True, related_name="our_reference")
    your_reference = models.ForeignKey(User, related_name="your_reference")
    sent = models.BooleanField()
    sent_timestamp = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=16, choices=STATES, default='created', db_index=True)
    identifier = models.CharField(max_length=32, blank=True, null=True, unique=True)
    terms_net_days = models.IntegerField(max_length=2, default=10, verbose_name=_('Terms days net'))
    is_basis = models.BooleanField(default=False, verbose_name=_('Is basis for invoice'))
    is_written_to_disk =  models.BooleanField(default=False, verbose_name=_('Is the pdf written to disk'))
    currency = models.ForeignKey(Currency)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_from_deals(cls, deals, reveiver=None, sender=None, from_agent=False):
        # make sure every deal is the same currency.
        if isinstance(deals, QuerySet):
            deals = deals.select_related('currency')
            deals = deals.select_related('ad__creator__user')

        if sender is None:
            defaults = settings.DEAL_INVOICE_SENDER[1]
            defaults.update({
                'is_active': False
            })
            sender, created = User.objects.get_or_create(username=settings.DEAL_INVOICE_SENDER[0], defaults=defaults)

        currency = deals[0].currency
        for deal in deals:
            if deal.currency != currency:
                raise ValidationError('All deals must be the same currency')

        invoice = cls()
        invoice.receiver = reveiver
        invoice.your_reference = sender
        invoice.our_reference = deals[0].ad.creator.user
        invoice.currency = currency
        if from_agent:
            invoice.is_basis = True
            invoice.title = _('Invoice basis')
        invoice.save()

        for deal in deals:
            row = Row.create_from_deal(deal, is_agent=from_agent)
            invoice.row_set.add(row)

        return invoice

    @property
    def expiration(self):
        if self.sent_timestamp:
            return self.sent_timestamp + datetime.timedelta(days=self.terms_net_days)
        else:
            return None

    @property
    def total_price(self):
        total_price = Decimal('0')
        for row in self.row_set.all():
            total_price += row.price

        return total_price.quantize(Decimal('.00'))

    @property
    def total_vat(self):
        return (self.total_price * VAT).quantize(Decimal('.00'))

    @property
    def total_inc_vat(self):
        price = self.total_price + self.total_vat
        return price.quantize(Decimal('.00'))

    @property
    def pdf_path(self):
        return os.path.join(settings.MEDIA_ROOT, 'invoices/%s.pdf' % self.identifier)

    def get_absolute_url(self):
        return urlparse.urljoin(settings.MEDIA_URL, 'invoices/%s.pdf' % self.identifier)

    def write_pdf(self):
        url = reverse('invoice:index', kwargs={'identifier': self.identifier})

        SavePDFCommand(url=url, pdf_path=self.pdf_path).run()

        self.is_written_to_disk = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = hashlib.md5(str(uuid.uuid1())).hexdigest()

        return super(Invoice, self).save(*args, **kwargs)

    class Meta:
        app_label = string_with_title('invoice', _('Invoice'))
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


class Row(models.Model):
    invoice = models.ForeignKey(Invoice)
    deal = models.ForeignKey(Deal, null=True, blank=True)
    identifier = models.CharField(max_length=16)
    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = string_with_title('invoice', _('Invoice'))
        verbose_name = _("Invoice row")
        verbose_name_plural = _("Invoice rows")

    @classmethod
    def create_from_deal(cls, deal, is_agent=False):
        row = cls()
        row.deal = deal

        if is_agent:
            row.identifier = 'A-%i-%i' % (deal.ad.pk, deal.pk)
            row.price = deal.agent_commission
        else:
            row.identifier = '%i-%i' % (deal.ad.pk, deal.pk)
            row.price = deal.commission

        row.title = deal.ad.get_localized('title', 'en')

        return row


class InvoiceLogEntry(models.Model):
    ACTIONS = (
        ('created', 'Created'),
        ('sent', 'Sent'),
    )

    invoice = models.ForeignKey(Invoice)
    action = models.CharField(max_length=16, choices=ACTIONS, default='created')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = string_with_title('invoice', _('Invoice'))
        verbose_name = _("Invoice log entry")
        verbose_name_plural = _("Invoices log entries")


def create_invoice_log_entry(sender, instance, created, **kwargs):
    if created:
        invoice_log_entry, created = InvoiceLogEntry.objects.get_or_create(invoice=instance)
        invoice_log_entry.save()


post_save.connect(create_invoice_log_entry, sender=Invoice, dispatch_uid="CreateInvoiceLogEntryOnce")
