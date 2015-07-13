# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Invoice.is_basis'
        db.add_column('invoice_invoice', 'is_basis',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Invoice.is_basis'
        db.delete_column('invoice_invoice', 'is_basis')


    models = {
        'accounts.agentdatacache': {
            'Meta': {'object_name': 'AgentDataCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_active': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_canceled': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_completed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_interested': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_recruited': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_sold_products': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'accounts.businessprofile': {
            'Meta': {'object_name': 'BusinessProfile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.BusinessProfile']", 'null': 'True', 'blank': 'True'}),
            'agent_data_cache': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.AgentDataCache']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'business_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['accounts.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'business_logo'", 'null': 'True', 'to': "orm['files.Image']"}),
            'member_level': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['accounts.MemberLevel']"}),
            'member_level_promoted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'profile_data_cache': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.ProfileDataCache']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'accounts.memberlevel': {
            'Meta': {'object_name': 'MemberLevel'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'accounts.profiledatacache': {
            'Meta': {'object_name': 'ProfileDataCache'},
            'current_commission_perc': ('django.db.models.fields.DecimalField', [], {'default': "'0.1'", 'max_digits': '3', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_ads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_ads_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_sold_products': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'active_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounts.BusinessProfile']"}),
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['files.Image']", 'null': 'True', 'blank': 'True'}),
            'business_profiles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'business_profiles'", 'symmetrical': 'False', 'to': "orm['accounts.BusinessProfile']"}),
            'cellphone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'userprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'ads.ad': {
            'Meta': {'object_name': 'Ad'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'business_domains': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ads'", 'symmetrical': 'False', 'to': "orm['ads.BusinessDomain']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.UserProfile']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['currencies.Currency']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_request': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'member_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.MemberLevel']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.BusinessProfile']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ads'", 'to': "orm['ads.ProductType']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'youtube_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'ads.businessdomain': {
            'Meta': {'object_name': 'BusinessDomain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_unique': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'title_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'})
        },
        'ads.field': {
            'Meta': {'object_name': 'Field'},
            'help_text_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'help_text_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_filterable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'label_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'title_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'})
        },
        'ads.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'product_types'", 'blank': 'True', 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'product_types'", 'symmetrical': 'False', 'to': "orm['ads.ProductCategory']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'title_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'currencies.currency': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'factor': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_base': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        'deals.deal': {
            'Meta': {'unique_together': "(('ad', 'owner'),)", 'object_name': 'Deal'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deals'", 'to': "orm['ads.Ad']"}),
            'agent_commission': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'bid': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'cancel_reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.UserProfile']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'currency'", 'null': 'True', 'to': "orm['currencies.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_reminder': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'manual_processing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.BusinessProfile']"}),
            'payed_to_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'price_eur': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'renewed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'interested'", 'max_length': '32'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'files.image': {
            'Meta': {'object_name': 'Image'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_short': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_slug': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique_with': '()', 'null': 'True', 'populate_from': "'title'"}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'invoice.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['currencies.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'is_basis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'our_reference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'our_reference'", 'null': 'True', 'to': "orm['auth.User']"}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.BusinessProfile']"}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'created'", 'max_length': '16', 'db_index': 'True'}),
            'terms_net_days': ('django.db.models.fields.IntegerField', [], {'default': '10', 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Commission Invoice'", 'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'your_reference': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'your_reference'", 'to': "orm['auth.User']"})
        },
        'invoice.invoicelogentry': {
            'Meta': {'object_name': 'InvoiceLogEntry'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'created'", 'max_length': '16'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoice.Invoice']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'invoice.row': {
            'Meta': {'object_name': 'Row'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deals.Deal']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoice.Invoice']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['invoice']