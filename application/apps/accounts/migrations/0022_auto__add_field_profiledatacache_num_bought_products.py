# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProfileDataCache.num_bought_products'
        db.add_column('accounts_profiledatacache', 'num_bought_products',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProfileDataCache.num_bought_products'
        db.delete_column('accounts_profiledatacache', 'num_bought_products')


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
            'Meta': {'ordering': "['business_name']", 'object_name': 'BusinessProfile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.BusinessProfile']", 'null': 'True', 'blank': 'True'}),
            'agent_data_cache': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'businessprofile'", 'unique': 'True', 'null': 'True', 'to': "orm['accounts.AgentDataCache']"}),
            'business_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['accounts.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_agent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'business_logo'", 'null': 'True', 'to': "orm['files.Image']"}),
            'profile_data_cache': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.ProfileDataCache']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'accounts.oldpassword': {
            'Meta': {'object_name': 'OldPassword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_nonce': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'old_password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'accounts.profiledatacache': {
            'Meta': {'object_name': 'ProfileDataCache'},
            'current_commission_perc': ('django.db.models.fields.DecimalField', [], {'default': "'0.1'", 'max_digits': '3', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_ads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_ads_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_bought_products': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_sold_products': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'active_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounts.BusinessProfile']"}),
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['files.Image']", 'null': 'True', 'blank': 'True'}),
            'business_profiles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'business_profiles'", 'symmetrical': 'False', 'to': "orm['accounts.BusinessProfile']"}),
            'cellphone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'userprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
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
        }
    }

    complete_apps = ['accounts']