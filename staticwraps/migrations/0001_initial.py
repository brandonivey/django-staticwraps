# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'StaticWrap'
        db.create_table('staticwraps_staticwrap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url_path', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('originating_site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('metadata', self.gf('jsonfield.fields.JSONField')(default='{"category_slug" : "/news/opinion-blogs", "content_type": "blog"}', blank=True)),
        ))
        db.send_create_signal('staticwraps', ['StaticWrap'])

        # Adding unique constraint on 'StaticWrap', fields ['url_path', 'originating_site']
        db.create_unique('staticwraps_staticwrap', ['url_path', 'originating_site_id'])


    def backwards(self, orm):

        # Deleting model 'StaticWrap'
        db.delete_table('staticwraps_staticwrap')

        # Removing unique constraint on 'StaticWrap', fields ['url_path', 'originating_site']
        db.delete_unique('staticwraps_staticwrap', ['url_path', 'originating_site_id'])


    models = {
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'market': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'music_format': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'staticwraps.staticwrap': {
            'Meta': {'unique_together': "(('url_path', 'originating_site'),)", 'object_name': 'StaticWrap'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('jsonfield.fields.JSONField', [], {'default': '\'{"category_slug" : "/news/opinion-blogs", "content_type": "blog"}\'', 'blank': 'True'}),
            'originating_site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['staticwraps']
