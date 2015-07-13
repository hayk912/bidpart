# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BlogEntry.unpublish'
        db.alter_column('blog_blogentry', 'unpublish', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'BlogEntry.unpublish'
        db.alter_column('blog_blogentry', 'unpublish', self.gf('django.db.models.fields.DateField')())

    models = {
        'blog.blogentry': {
            'Meta': {'object_name': 'BlogEntry'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_slug': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'unpublish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2112, 6, 3, 0, 0)', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['blog']