# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AdminSetting.settings_group'
        db.delete_column('adminsettings_adminsetting', 'settings_group_id')

        # Adding M2M table for field settings_group on 'AdminSetting'
        db.create_table('adminsettings_adminsetting_settings_group', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('adminsetting', models.ForeignKey(orm['adminsettings.adminsetting'], null=False)),
            ('adminsettingsgroup', models.ForeignKey(orm['adminsettings.adminsettingsgroup'], null=False))
        ))
        db.create_unique('adminsettings_adminsetting_settings_group', ['adminsetting_id', 'adminsettingsgroup_id'])

        # Adding unique constraint on 'AdminSetting', fields ['value', 'key']
        db.create_unique('adminsettings_adminsetting', ['value', 'key'])


    def backwards(self, orm):
        # Removing unique constraint on 'AdminSetting', fields ['value', 'key']
        db.delete_unique('adminsettings_adminsetting', ['value', 'key'])

        # Adding field 'AdminSetting.settings_group'
        db.add_column('adminsettings_adminsetting', 'settings_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adminsettings.AdminSettingsGroup'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field settings_group on 'AdminSetting'
        db.delete_table('adminsettings_adminsetting_settings_group')


    models = {
        'adminsettings.adminsetting': {
            'Meta': {'unique_together': "(('key', 'value'),)", 'object_name': 'AdminSetting'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'settings_group': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['adminsettings.AdminSettingsGroup']", 'null': 'True', 'symmetrical': 'False'}),
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