# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Voter.poll'
        db.add_column(u'polls_voter', 'poll',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Voter.poll'
        db.delete_column(u'polls_voter', 'poll_id')


    models = {
        u'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'polls.voter': {
            'Meta': {'object_name': 'Voter'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Choice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']", 'null': 'True'})
        }
    }

    complete_apps = ['polls']