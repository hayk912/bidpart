from django.test import TestCase
from application import settings
import models


class CMSTest(TestCase):
    def test_create_page(self):
        """
        Test create multi-language page
        """
        page = models.Page(default_title="TestDefault")
        page.save()

        for lang_code in settings.LANGUAGES:
            body = models.PageText(page=page, text="Test_%s" % lang_code[0], locale=lang_code[0])
            body.save()

            title = models.PageTextString(page=page, text_string="Test_%s" % lang_code[0], locale=lang_code[0])
            title.save()

            db_page = models.Page.objects.all()[0]

            self.assertEqual(db_page.get_body(locale=lang_code[0]), body.text)
            self.assertEqual(db_page.get_title(locale=lang_code[0]), title.text_string)
