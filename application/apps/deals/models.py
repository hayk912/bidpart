# coding=utf-8
from decimal import Decimal
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db import models
from django.template import Context, Template
from django.utils import timezone, importlib
from application.apps.accounts.models import UserProfile, BusinessProfile
from application.apps.ads.models import Ad
from currencies.models import Currency
from django.utils.translation import ugettext_lazy as _
from application.apps.ads.templatetags.ads_extras import convert_price
from application.apps.cms.models import EmailTemplate


class DealManager(models.Manager):
    pass


class Deal(models.Model):
    """ A deal for an Ad """

    class Meta:
        unique_together = ('ad', 'owner')

    STATES = (
        ('interested', _('Interested')),
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('canceled', _('Canceled')),
    )

    creator = models.ForeignKey(UserProfile)
    owner = models.ForeignKey(BusinessProfile)
    ad = models.ForeignKey(Ad, related_name='deals', verbose_name=_('Ad'))
    state = models.CharField(max_length=32, choices=STATES, default='interested', verbose_name=_('State'))
    bid = models.DecimalField(max_digits=20, decimal_places=2, help_text=_('Optional bid'), verbose_name=_('Bid'))
    price = models.DecimalField(max_digits=20, decimal_places=2, help_text=_('End price'), blank=True, null=True, verbose_name=_('Price'))
    amount = models.IntegerField(verbose_name=_('Amount'), help_text=_('The number of items'))
    price_eur = models.DecimalField(max_digits=20, decimal_places=2, help_text=_('End price (Converted to EUR)'), blank=True, null=True, verbose_name=_('Price converted to EUR'))
    commission = models.DecimalField(max_digits=20, decimal_places=2, help_text=_('Commission'), blank=True, null=True, verbose_name=_('Commission'))
    agent_commission = models.DecimalField(max_digits=20, decimal_places=2, help_text=_('Agent Commission'), blank=True, null=True, verbose_name=_('Agent comission'))
    last_reminder = models.DateTimeField(verbose_name=_('Last reminder'), auto_now_add=True)
    manual_processing = models.BooleanField(verbose_name=_('Manual processing'))
    payed_to_agent = models.BooleanField(verbose_name=_('Payed to agent'))
    cancel_reason = models.TextField(blank=True, null=True, verbose_name=_('Cancel reason'))
    invoice = models.ForeignKey('invoice.Invoice', verbose_name=_('The invoice this deal has auto-created'), blank=True, null=True, help_text=_('If this deal auto-created a invoice, it will be referenced here'))
    renewed = models.DateTimeField(auto_now_add=True, verbose_name=_('Renewed'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))

    # actions
    ACTIVATE = 'activate'
    EXTEND = 'extend'
    CANCEL = 'cancel'
    COMPLETE = 'complete'

    @property
    def currency(self):
        return self.ad.currency

    @property
    def float_unit_bid(self):
        if self.bid > 0 and self.amount > 0:
            return str(Decimal(float(self.bid / self.amount)).quantize(Decimal('.00')))
        else:
            return str(Decimal(self.ad.price).quantize(Decimal('.00')))

    def user_has_perm(self, user_obj, perm):
        """
        :type user_obj: User
        """
        if perm == 'change_deal':
            if user_obj.is_anonymous():
                return False
            elif user_obj.get_business_profile().pk == self.ad.owner.pk:
                if self.state == 'completed' or self.state == 'canceled':
                    return False
                else:
                    return True
            else:
                return False

    def do_action(self, action, cancel_reason=None, amount=None, end_price=None):
        if action == self.ACTIVATE:
            self.state = 'active'
            self.renewed = timezone.now()
            self.save()
            threading.Thread(target=self.send_mail,
                             args=('status_changed', self.ad.creator.user.email, self.ad.creator.lang_code)).start()

        elif action == self.EXTEND:
            self.renewed = timezone.now()
            self.save()

        elif action == self.CANCEL:
            self.state = 'canceled'
            if cancel_reason:
                self.cancel_reason = cancel_reason
            else:
                self.cancel_reason = 'No reason supplied.'

            self.save()
            threading.Thread(target=self.send_mail,
                             args=('status_changed', self.ad.creator.user.email, self.ad.creator.lang_code)).start()

        elif action == self.COMPLETE:
            if amount:
                self.amount = amount

            if (self.ad.amount - self.amount) >= 0:
                self.state = 'completed'
                self.ad.amount -= self.amount

                if self.ad.amount == 0:
                    self.ad.published = False
                    other_deals = self.ad.deals.exclude(pk=self.pk)
                    for other_deal in other_deals:
                        other_deal.do_action(self.CANCEL, cancel_reason='Auto cancel, all items are sold.')

                self.ad.save()

                if end_price:
                    self.price = end_price
                else:
                    self.price = self.bid

                self.price_eur = convert_price(self.price, self.currency, Currency.objects.get(code='EUR'))

                commission = importlib.import_module('application.apps.deals.func').commission
                self.commission = commission(self.ad.owner, self.price, self.currency)

                if self.ad.owner.agent_id:
                    agent_commission = importlib.import_module('application.apps.deals.func').agent_commission
                    self.agent_commission = agent_commission(
                        agent=self.ad.owner.agent,
                        bidpart_commission=self.commission,
                        currency=self.currency
                    )

                if (self.price / self.amount) < (self.ad.price * settings.DEAL_MANUAL_PROCESSING_LIMIT):
                    self.manual_processing = True

                _Invoice = importlib.import_module('application.apps.invoice.models').Invoice
                self.invoice = _Invoice.create_from_deals([self], self.ad.owner)

                self.save()

                seller_profile = self.creator if self.ad.is_request else self.ad.creator
                customer_profile = self.ad.creator if self.ad.is_request else self.creator

                if not self.manual_processing:
                    threading.Thread(target=self.send_mail,
                                     args=('invoice', seller_profile.user.email, seller_profile.lang_code)).start()
                    threading.Thread(target=self.send_mail,
                                     args=('completed_customer',customer_profile.user.email, customer_profile.lang_code)).start()

            else:
                raise ValueError('Invalid amount %s of %s' % (amount, self.ad.amount))

        else:
            raise ValueError('Invalid action %s' % action)

        return self

    def created_weeks_ago(self):
        delta = timezone.now() - self.created
        #noinspection PyTypeChecker
        return int(round(delta.days / 7.0, 0))

    def send_mail(self, name, to, lang_code='en'):
        if not isinstance(to, (list, tuple)):
            to = [to]

        template = EmailTemplate.objects.get(name=name)
        context = Context({
            'deal': self,
            'ad_title': self.ad.get_localized('title', lang_code),
            'ad_url': 'http://{0}{1}?next={2}%23deal-{3}'.format(
                settings.BASE_URL,
                reverse('accounts:login'),
                reverse('ads:ad_detail', kwargs={
                    'pk': self.ad.pk
                }),
                self.pk
            )
        })

        lang_code = self.ad.creator.lang_code or 'en'

        subject = template.get_localized('subject', lang_code)
        email_html = Template(template.get_localized('html', lang_code)).render(context)
        email_txt = Template(template.get_localized('txt', lang_code)).render(context)

        message = EmailMultiAlternatives(subject=subject, to=to)
        message.attach_alternative(email_txt, 'text/plain')
        message.attach_alternative(email_html, 'text/html')

        if name == 'invoice':
            if not self.invoice.is_written_to_disk:
                self.invoice.sent_timestamp = timezone.now()
                self.invoice.sent = True
                self.invoice.write_pdf()

            message.attach_file(self.invoice.pdf_path)

        message.send()

    def save(self, *args, **kwargs):
        self.ad.last_deal_updated = timezone.now()
        self.ad.save()
        super(Deal, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s: %s' % (self.ad, self.state)
