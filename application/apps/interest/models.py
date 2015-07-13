import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context, Template
from django.utils.translation import gettext_lazy as _
from application.apps.cms.models import EmailTemplate


class Interest(models.Model):
    first_name = models.CharField(max_length=40, verbose_name=_('First name'))
    last_name = models.CharField(max_length=40, verbose_name=_('Last name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))

    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))

    comment = models.TextField(verbose_name=_('Comment'), blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # new
            threading.Thread(target=self.send_mail).start()

        return super(Interest, self).save(*args, **kwargs)

    def send_mail(self):
        to = [settings.INTEREST_CONTACT_SENT_TO]

        template = EmailTemplate.objects.get(name='interest_contact')
        context = Context({
            'object': self,
        })

        lang_code = 'sv'

        subject = template.get_localized('subject', lang_code)
        email_html = Template(template.get_localized('html', lang_code)).render(context)
        email_txt = Template(template.get_localized('txt', lang_code)).render(context)

        message = EmailMultiAlternatives(subject=subject, to=to)
        message.attach_alternative(email_txt, 'text/plain')
        message.attach_alternative(email_html, 'text/html')

        message.send()

    def __unicode__(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)
