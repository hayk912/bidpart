# coding=utf-8
import models
from django.test import TestCase
from django.utils import timezone

import datetime
from pprint import pprint


class BlogTest(TestCase):
    def test_create_entry(self):
        """ Test create entry """
        new = models.BlogEntry()

        new.title = "Test"
        new.teaser = "Test teaser"
        new.body = "Test body"

        new.created = timezone.now()
        new.updated = timezone.now()

        new.save()

        entry = models.BlogEntry.objects.get(pk=new.pk)

        self.failUnless(entry.title == new.title)
        self.failUnless(entry.teaser == new.teaser)
        self.failUnless(entry.body == new.body)
        self.failUnless(entry.created == new.created)
        self.failUnless(entry.updated == new.updated)
        self.failUnless(entry.publish == new.publish)
        self.failUnless(entry.unpublish == new.unpublish)

    def test_get_single_by_slug(self):

        """ Test #1 by slug """
        entry = models.BlogEntry()
        entry.title = "Test abc, - åäö"
        entry.save()

        try:
            models.BlogEntry.objects.get_active_entry_by_slug(entry_slug="test-abc-aao")
        except:
            entry = models.BlogEntry.objects.all()[0]
            print "Saved slug: " + entry.title_slug
            self.fail()

    def test_get_single_by_id(self):
        """ Test #2 by id """
        entry = models.BlogEntry()
        entry.title = "Test"
        entry.save()
        entry = models.BlogEntry()
        entry.title = "Test1"
        entry.save()
        try:
            entry = models.BlogEntry.objects.get_active_entry(entry_id=2)
        except:
            self.fail()

    def test_many_entries(self):
        for i in range(1000):
            entry = models.BlogEntry()
            entry.title = "Test" + str(i + 1)
            entry.save()

        db_entries = models.BlogEntry.objects.get_active_entries()

        self.failUnless(db_entries.count() == 1000)

        for entry in db_entries:
            self.failUnless(entry.title_slug == "test" + str(entry.id))

    def test_get_latest(self):
        """ Test: Get lastest blog entry """
        for i in range(3):
            entry = models.BlogEntry()
            entry.title = "Test" + str(i + 1)
            entry.publish = timezone.now() - datetime.timedelta(hours=5) + datetime.timedelta(hours=i)
            #print entry.title + " " + str(entry.publish)
            entry.save()

        db_entry = models.BlogEntry.objects.get_latest_entry()
        #print dir(models.BlogEntry.objects.get(pk=3))
        #db_entries = models.BlogEntry.objects.get_active_entries().query
        #print db_entries
        #print models.BlogEntry.objects.get_active_entries().count()
        #print
        #for e in db_entries:
        #    print e
        #pprint(dir(models.BlogEntry.objects.get_active_entries().query.sql_with_params))
        #print db_entry.title + " == " + entry.title
        self.failUnless(db_entry.title == entry.title)

    def test_get_active(self):

        """ Test #1 normal, active """
        entry = models.BlogEntry()

        entry.title = "Test"

        entry.save()

        """ Test #2 inactive """
        entry = models.BlogEntry()

        entry.title = "Test2"
        entry.active = False

        entry.save()

        entry = models.BlogEntry()

        """ Test #3: unpublish date passed """
        entry.title = "Test3"
        entry.unpublish = timezone.now() - datetime.timedelta(days=1)

        entry.save()

        """ Test #4 publish date not happened """

        entry = models.BlogEntry()

        entry.title = "Test4"
        entry.publish = timezone.now() + datetime.timedelta(days=1)

        entry.save()

        """ Check for result num = 1 """

        all_entries = models.BlogEntry.objects.all()

        active_entries = models.BlogEntry.objects.get_active_entries()

        self.failUnless(all_entries.count() == 4)
        self.failUnless(active_entries.count() == 1)
