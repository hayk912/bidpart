# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        if not db.dry_run:
            for product_type in orm.ProductType.objects.all():
                product_type.save()
            for business_domain in orm.BusinessDomain.objects.all():
                business_domain.save()
            for product_category in orm.ProductCategory.objects.all():
                product_category.save()

        # Changing field 'ProductCategory.slug'
        db.alter_column('ads_productcategory', 'slug', self.gf('autoslug.fields.AutoSlugField')(default='', unique=True, max_length=50, populate_from='title', unique_with=()))

        # Changing field 'BusinessDomain.slug'
        db.alter_column('ads_businessdomain', 'slug', self.gf('autoslug.fields.AutoSlugField')(default='', unique=True, max_length=50, populate_from='title', unique_with=()))

        # Changing field 'ProductType.slug'
        db.alter_column('ads_producttype', 'slug', self.gf('autoslug.fields.AutoSlugField')(default='', unique=True, max_length=50, populate_from='title', unique_with=()))

    def backwards(self, orm):

        # Changing field 'ProductCategory.slug'
        db.alter_column('ads_productcategory', 'slug', self.gf('autoslug.fields.AutoSlugField')(populate_from='title', unique=True, max_length=50, null='True', unique_with=()))

        # Changing field 'BusinessDomain.slug'
        db.alter_column('ads_businessdomain', 'slug', self.gf('autoslug.fields.AutoSlugField')(populate_from='title', unique=True, max_length=50, null='True', unique_with=()))

        # Changing field 'ProductType.slug'
        db.alter_column('ads_producttype', 'slug', self.gf('autoslug.fields.AutoSlugField')(populate_from='title', unique=True, max_length=50, null='True', unique_with=()))

    models = {
        'accounts.businessprofile': {
            'Meta': {'object_name': 'BusinessProfile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'address_zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'agent'", 'null': 'True', 'to': "orm['accounts.UserProfile']"}),
            'business_description': ('django.db.models.fields.TextField', [], {}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['accounts.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['files.Image']", 'null': 'True', 'blank': 'True'}),
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
            'active_profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['accounts.BusinessProfile']"}),
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['files.Image']", 'null': 'True', 'blank': 'True'}),
            'business_profiles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'business_profiles'", 'blank': 'True', 'to': "orm['accounts.BusinessProfile']"}),
            'cellphone': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.MemberLevel']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.BusinessProfile']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ads'", 'to': "orm['ads.ProductType']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'youtube_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'ads.businessdomain': {
            'Meta': {'object_name': 'BusinessDomain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.field': {
            'Meta': {'object_name': 'Field'},
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.fieldchoice': {
            'Meta': {'object_name': 'FieldChoice'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'field_choice'", 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'ads.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'product_types'", 'blank': 'True', 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'product_types'", 'symmetrical': 'False', 'to': "orm['ads.ProductCategory']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'ads.value': {
            'Meta': {'object_name': 'Value'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['ads.Ad']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['ads.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'files.image': {
            'Meta': {'object_name': 'Image'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_short': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title_slug': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique_with': '()', 'null': 'True', 'populate_from': "'title'"}),
            'unique_hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ads']
