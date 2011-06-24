# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Submission'
        db.create_table('customcore_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publish_state', self.gf('django.db.models.fields.CharField')(default='published', max_length=50)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 8, 8, 19, 19, 866234))),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('preposition', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('where', self.gf('django.db.models.fields.TextField')()),
            ('who', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('customcore', ['Submission'])


    def backwards(self, orm):
        
        # Deleting model 'Submission'
        db.delete_table('customcore_submission')


    models = {
        'customcore.actioncode': {
            'Meta': {'object_name': 'ActionCode'},
            'code': ('core.fields.CodeField', [], {'unique': 'True', 'max_length': '8', 'name': "'code'", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 8, 8, 19, 19, 866234)'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'customcore.submission': {
            'Meta': {'object_name': 'Submission'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'preposition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 8, 8, 19, 19, 866234)'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'where': ('django.db.models.fields.TextField', [], {}),
            'who': ('django.db.models.fields.TextField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['customcore']
