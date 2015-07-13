# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BlogEntry'
        db.create_table('blog_blogentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title_slug', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('teaser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('publish', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('unpublish', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2112, 6, 2, 0, 0), blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('blog', ['BlogEntry'])


    def backwards(self, orm):
        # Deleting model 'BlogEntry'
        db.delete_table('blog_blogentry')


    models = {
        'blog.blogentry': {
            'Meta': {'object_name': 'BlogEntry'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_slug': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'unpublish': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2112, 6, 2, 0, 0)', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['blog']