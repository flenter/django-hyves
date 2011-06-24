# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ActionCode.used'
        db.add_column('customcore_actioncode', 'used', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ActionCode.used'
        db.delete_column('customcore_actioncode', 'used')


    models = {
        'customcore.actioncode': {
            'Meta': {'object_name': 'ActionCode'},
            'code': ('core.fields.CodeField', [], {'unique': 'True', 'max_length': '8', 'name': "'code'", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 8, 8, 4, 24, 429641)'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['customcore']
