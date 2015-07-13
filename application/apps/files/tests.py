from django.test import TestCase
from models import Image, File


class TestFiles(TestCase):
    def test_create(self):
        """
        Simple test (without image file) to see if image can be created
        """

        i = Image()
        i.title = "Test"
        i.description = "Long image image description"
        i.description_short = "Short image description"
        i.save()

        db_i = Image.objects.get(pk=1)

        self.assertEqual(i.title, db_i.title)
        self.assertEqual(i.description, db_i.description)
        self.assertEqual(i.description_short, db_i.description_short)
