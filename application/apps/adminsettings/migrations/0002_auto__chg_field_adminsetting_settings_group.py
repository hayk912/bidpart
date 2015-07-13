# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AdminSetting.settings_group'
        db.alter_column('adminsettings_adminsetting', 'settings_group_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adminsettings.AdminSettingsGroup'], null=True))

    def backwards(self, orm):

        # Changing field 'AdminSetting.settings_group'
        db.alter_column('adminsettings_adminsetting', 'settings_group_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['adminsettings.AdminSettingsGroup']))

    models = {
        'adminsettings.adminsetting': {
            'Meta': {'object_name': 'AdminSetting'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'settings_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adminsettings.AdminSettingsGroup']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'test'", 'max_length': '16'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'adminsettings.adminsettingsgroup': {
            'Meta': {'object_name': 'AdminSettingsGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['adminsettings']