# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Field.label_en'
        db.add_column('ads_field', 'label_en',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Field.label_sv'
        db.add_column('ads_field', 'label_sv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Field.help_text_en'
        db.add_column('ads_field', 'help_text_en',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Field.help_text_sv'
        db.add_column('ads_field', 'help_text_sv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'ProductCategory.title_en'
        db.add_column('ads_productcategory', 'title_en',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'ProductCategory.title_sv'
        db.add_column('ads_productcategory', 'title_sv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'BusinessDomain.title_en'
        db.add_column('ads_businessdomain', 'title_en',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'BusinessDomain.title_sv'
        db.add_column('ads_businessdomain', 'title_sv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'FieldChoice.name_en'
        db.add_column('ads_fieldchoice', 'name_en',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'FieldChoice.name_sv'
        db.add_column('ads_fieldchoice', 'name_sv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Value.choice_value'
        db.add_column('ads_value', 'choice_value',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ads.FieldChoice'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'ProductType.title_en'
        db.add_column('ads_producttype', 'title_en',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'ProductType.title_sv'
        db.add_column('ads_producttype', 'title_sv',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Field.label_en'
        db.delete_column('ads_field', 'label_en')

        # Deleting field 'Field.label_sv'
        db.delete_column('ads_field', 'label_sv')

        # Deleting field 'Field.help_text_en'
        db.delete_column('ads_field', 'help_text_en')

        # Deleting field 'Field.help_text_sv'
        db.delete_column('ads_field', 'help_text_sv')

        # Deleting field 'ProductCategory.title_en'
        db.delete_column('ads_productcategory', 'title_en')

        # Deleting field 'ProductCategory.title_sv'
        db.delete_column('ads_productcategory', 'title_sv')

        # Deleting field 'BusinessDomain.title_en'
        db.delete_column('ads_businessdomain', 'title_en')

        # Deleting field 'BusinessDomain.title_sv'
        db.delete_column('ads_businessdomain', 'title_sv')

        # Deleting field 'FieldChoice.name_en'
        db.delete_column('ads_fieldchoice', 'name_en')

        # Deleting field 'FieldChoice.name_sv'
        db.delete_column('ads_fieldchoice', 'name_sv')

        # Deleting field 'Value.choice_value'
        db.delete_column('ads_value', 'choice_value_id')

        # Deleting field 'ProductType.title_en'
        db.delete_column('ads_producttype', 'title_en')

        # Deleting field 'ProductType.title_sv'
        db.delete_column('ads_producttype', 'title_sv')


    models = {
        'accounts.businessprofile': {
            'Meta': {'object_name': 'BusinessProfile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'agent'", 'null': 'True', 'to': "orm['accounts.UserProfile']"}),
            'business_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['accounts.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'business_logo'", 'null': 'True', 'to': "orm['files.Image']"}),
            'member_level': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['accounts.MemberLevel']"}),
            'member_level_promoted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'accounts.memberlevel': {
            'Meta': {'object_name': 'MemberLevel'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'business_domains': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ads'", 'blank': 'True', 'to': "orm['ads.BusinessDomain']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.UserProfile']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['currencies.Currency']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.MemberLevel']"}),
            'num_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.BusinessProfile']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ads'", 'to': "orm['ads.ProductType']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'youtube_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'ads.adfile': {
            'Meta': {'object_name': 'AdFile', '_ormbases': ['files.File']},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Ad']", 'null': 'True', 'blank': 'True'}),
            'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['files.File']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ads.adimage': {
            'Meta': {'object_name': 'AdImage', '_ormbases': ['files.Image']},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'to': "orm['ads.Ad']"}),
            'image_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['files.Image']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ads.businessdomain': {
            'Meta': {'object_name': 'BusinessDomain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'title_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'})
        },
        'ads.field': {
            'Meta': {'object_name': 'Field'},
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'help_text_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'help_text_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_filterable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'label_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'label_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.fieldchoice': {
            'Meta': {'object_name': 'FieldChoice'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'field_choices'", 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'})
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
        'ads.value': {
            'Meta': {'object_name': 'Value'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_set'", 'to': "orm['ads.Ad']"}),
            'choice_value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.FieldChoice']", 'null': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_set'", 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'min_value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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
        'files.file': {
            'Meta': {'object_name': 'File'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_short': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_slug': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique_with': '()', 'null': 'True', 'populate_from': "'title'"}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['ads']