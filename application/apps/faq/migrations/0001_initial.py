# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FAQGroup'
        db.create_table('faq_faqgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['faq.FAQGroup'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('faq', ['FAQGroup'])

        # Adding model 'FAQQuestion'
        db.create_table('faq_faqquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answer', self.gf('django.db.models.fields.TextField')()),
            ('only_logged_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('faq', ['FAQQuestion'])

        # Adding M2M table for field group on 'FAQQuestion'
        db.create_table('faq_question_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('faqquestion', models.ForeignKey(orm['faq.faqquestion'], null=False)),
            ('faqgroup', models.ForeignKey(orm['faq.faqgroup'], null=False))
        ))
        db.create_unique('faq_question_groups', ['faqquestion_id', 'faqgroup_id'])


    def backwards(self, orm):
        # Deleting model 'FAQGroup'
        db.delete_table('faq_faqgroup')

        # Deleting model 'FAQQuestion'
        db.delete_table('faq_faqquestion')

        # Removing M2M table for field group on 'FAQQuestion'
        db.delete_table('faq_question_groups')


    models = {
        'faq.faqgroup': {
            'Meta': {'object_name': 'FAQGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['faq.FAQGroup']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'faq.faqquestion': {
            'Meta': {'object_name': 'FAQQuestion'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['faq.FAQGroup']", 'db_table': "'faq_question_groups'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'only_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['faq']