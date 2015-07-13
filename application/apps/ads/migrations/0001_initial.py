# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ad'
        db.create_table('ads_ad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ads', to=orm['ads.ProductType'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ads', ['Ad'])

        # Adding M2M table for field business_domains on 'Ad'
        db.create_table('ads_ad_business_domains', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ad', models.ForeignKey(orm['ads.ad'], null=False)),
            ('businessdomain', models.ForeignKey(orm['ads.businessdomain'], null=False))
        ))
        db.create_unique('ads_ad_business_domains', ['ad_id', 'businessdomain_id'])

        # Adding model 'Values'
        db.create_table('ads_values', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['ads.Ad'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['ads.Field'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('ads', ['Values'])

        # Adding model 'BusinessDomain'
        db.create_table('ads_businessdomain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('ads', ['BusinessDomain'])

        # Adding model 'ProductType'
        db.create_table('ads_producttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('ads', ['ProductType'])

        # Adding M2M table for field fields on 'ProductType'
        db.create_table('ads_producttype_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('producttype', models.ForeignKey(orm['ads.producttype'], null=False)),
            ('field', models.ForeignKey(orm['ads.field'], null=False))
        ))
        db.create_unique('ads_producttype_fields', ['producttype_id', 'field_id'])

        # Adding M2M table for field product_categories on 'ProductType'
        db.create_table('ads_producttype_product_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('producttype', models.ForeignKey(orm['ads.producttype'], null=False)),
            ('productcategory', models.ForeignKey(orm['ads.productcategory'], null=False))
        ))
        db.create_unique('ads_producttype_product_categories', ['producttype_id', 'productcategory_id'])

        # Adding model 'ProductCategory'
        db.create_table('ads_productcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('ads', ['ProductCategory'])

        # Adding model 'Field'
        db.create_table('ads_field', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('ads', ['Field'])


    def backwards(self, orm):
        # Deleting model 'Ad'
        db.delete_table('ads_ad')

        # Removing M2M table for field business_domains on 'Ad'
        db.delete_table('ads_ad_business_domains')

        # Deleting model 'Values'
        db.delete_table('ads_values')

        # Deleting model 'BusinessDomain'
        db.delete_table('ads_businessdomain')

        # Deleting model 'ProductType'
        db.delete_table('ads_producttype')

        # Removing M2M table for field fields on 'ProductType'
        db.delete_table('ads_producttype_fields')

        # Removing M2M table for field product_categories on 'ProductType'
        db.delete_table('ads_producttype_product_categories')

        # Deleting model 'ProductCategory'
        db.delete_table('ads_productcategory')

        # Deleting model 'Field'
        db.delete_table('ads_field')


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
        'ads.values': {
            'Meta': {'object_name': 'Values'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['ads.Ad']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['ads']