# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Values'
        db.delete_table('ads_values')

        # Adding model 'Value'
        db.create_table('ads_value', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['ads.Ad'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['ads.Field'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('ads', ['Value'])


    def backwards(self, orm):
        # Adding model 'Values'
        db.create_table('ads_values', (
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['ads.Field'])),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['ads.Ad'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('ads', ['Values'])

        # Deleting model 'Value'
        db.delete_table('ads_value')


    models = {
        'ads.ad': {
            'Meta': {'object_name': 'Ad'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'business_domains': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ads'", 'blank': 'True', 'to': "orm['ads.BusinessDomain']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ads'", 'to': "orm['ads.ProductType']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ads.businessdomain': {
            'Meta': {'object_name': 'BusinessDomain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.field': {
            'Meta': {'object_name': 'Field'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'product_types'", 'blank': 'True', 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'product_types'", 'symmetrical': 'False', 'to': "orm['ads.ProductCategory']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.value': {
            'Meta': {'object_name': 'Value'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['ads.Ad']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['ads']