# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BlogEntryImage'
        db.create_table('blog_blogentryimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.BlogEntry'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['images.Image'])),
        ))
        db.send_create_signal('blog', ['BlogEntryImage'])


    def backwards(self, orm):
        # Deleting model 'BlogEntryImage'
        db.delete_table('blog_blogentryimage')


    models = {
        'blog.blogentry': {
            'Meta': {'object_name': 'BlogEntry'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 8, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['images.Image']", 'null': 'True', 'through': "orm['blog.BlogEntryImage']", 'blank': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 8, 0, 0)', 'blank': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_slug': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'unpublish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2112, 6, 6, 0, 0)', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 8, 0, 0)', 'blank': 'True'})
        },
        'blog.blogentryimage': {
            'Meta': {'object_name': 'BlogEntryImage'},
            'blog_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.BlogEntry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['images.Image']"})
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

    complete_apps = ['blog']