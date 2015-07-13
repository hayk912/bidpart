# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.conf import settings

from django.test import TestCase
import os
from application.apps.invoice.models import SavePDFCommand


class SimpleTest(TestCase):
    def test_save_pdf(self):
        pdf_path = settings.MEDIA_ROOT + '/invoices/%s.pdf' % 'google'

        SavePDFCommand('http://www.google.com', pdf_path).run()

        self.failUnless(os.path.isfile(pdf_path), 'The PDF was not generated')

        os.remove(pdf_path)
