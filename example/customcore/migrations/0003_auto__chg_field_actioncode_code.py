# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'ActionCode.code'
        db.alter_column('customcore_actioncode', 'code', self.gf('core.fields.CodeField')(max_length=8, name='code', blank=True))
    
    
    def backwards(self, orm):
        
        # Changing field 'ActionCode.code'
        db.alter_column('customcore_actioncode', 'code', self.gf('django.db.models.fields.CharField')(max_length=8))
    
    
    models = {
        'customcore.actioncode': {
            'Meta': {'object_name': 'ActionCode'},
            'code': ('core.fields.CodeField', [], {'max_length': '8', 'name': "'code'", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 18, 8, 49, 43, 393593)'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'})
        }
    }
    
    complete_apps = ['customcore']
