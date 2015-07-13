# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageText'
        db.create_table('cms_pagetext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('locale', self.gf('django.db.models.fields.CharField')(default='en', max_length=16)),
        ))
        db.send_create_signal('cms', ['PageText'])

        # Adding model 'PageTextString'
        db.create_table('cms_pagetextstring', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('text_string', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('locale', self.gf('django.db.models.fields.CharField')(default='en', max_length=16)),
        ))
        db.send_create_signal('cms', ['PageTextString'])

        # Adding model 'PageImage'
        db.create_table('cms_pageimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['images.Image'])),
        ))
        db.send_create_signal('cms', ['PageImage'])

        # Adding model 'Page'
        db.create_table('cms_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('default_title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('title_slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 10, 12, 0, 0), null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 10, 12, 0, 0), null=True, blank=True)),
        ))
        db.send_create_signal('cms', ['Page'])


    def backwards(self, orm):
        # Deleting model 'PageText'
        db.delete_table('cms_pagetext')

        # Deleting model 'PageTextString'
        db.delete_table('cms_pagetextstring')

        # Deleting model 'PageImage'
        db.delete_table('cms_pageimage')

        # Deleting model 'Page'
        db.delete_table('cms_page')


    models = {
        'cms.page': {
            'Meta': {'object_name': 'Page'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 12, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'default_title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['images.Image']", 'null': 'True', 'through': "orm['cms.PageImage']", 'blank': 'True'}),
            'title_slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 12, 0, 0)', 'null': 'True', 'blank': 'True'})
        },
        'cms.pageimage': {
            'Meta': {'object_name': 'PageImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['images.Image']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"})
        },
        'cms.pagetext': {
            'Meta': {'object_name': 'PageText'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '16'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.pagetextstring': {
            'Meta': {'object_name': 'PageTextString'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '16'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"}),
            'text_string': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'images.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_description': ('django.db.models.fields.TextField', [], {}),
            'image_description_short': ('django.db.models.fields.TextField', [], {}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_slug': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['cms']