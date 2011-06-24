# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'ActionCode'
        db.create_table('customcore_actioncode', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('publish_state', self.gf('django.db.models.fields.CharField')(default='published', max_length=50)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 18, 8, 47, 39, 279458))),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('customcore', ['ActionCode'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'ActionCode'
        db.delete_table('customcore_actioncode')
    
    
    models = {
        'customcore.actioncode': {
            'Meta': {'object_name': 'ActionCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 18, 8, 47, 39, 279458)'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'})
        }
    }
    
    complete_apps = ['customcore']
