# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Poll.answers'
        db.delete_column(u'polls_poll', 'answers')


    def backwards(self, orm):
        # Adding field 'Poll.answers'
        db.add_column(u'polls_poll', 'answers',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'polls.voter': {
            'Meta': {'object_name': 'Voter'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Choice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']"})
        }
    }

    complete_apps = ['polls']