# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ticket'
        db.create_table('contact_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('contact', ['Ticket'])


    def backwards(self, orm):
        # Deleting model 'Ticket'
        db.delete_table('contact_ticket')


    models = {
        'contact.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['contact']