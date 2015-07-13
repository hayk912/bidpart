# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdminSetting'
        db.create_table('adminsettings_adminsetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('settings_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adminsettings.AdminSettingsGroup'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('adminsettings', ['AdminSetting'])

        # Adding model 'AdminSettingsGroup'
        db.create_table('adminsettings_adminsettingsgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('adminsettings', ['AdminSettingsGroup'])


    def backwards(self, orm):
        # Deleting model 'AdminSetting'
        db.delete_table('adminsettings_adminsetting')

        # Deleting model 'AdminSettingsGroup'
        db.delete_table('adminsettings_adminsettingsgroup')


    models = {
        'adminsettings.adminsetting': {
            'Meta': {'object_name': 'AdminSetting'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'settings_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adminsettings.AdminSettingsGroup']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'adminsettings.adminsettingsgroup': {
            'Meta': {'object_name': 'AdminSettingsGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['adminsettings']