# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Ticket.subject'
        db.add_column('contact_ticket', 'subject',
                      self.gf('django.db.models.fields.CharField')(default='subject', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Ticket.subject'
        db.delete_column('contact_ticket', 'subject')


    models = {
        'contact.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['contact']