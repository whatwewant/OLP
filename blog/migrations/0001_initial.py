# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table(u'blog_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_gmt', self.gf('django.db.models.fields.DateField')(null=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('excerpt', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('comment_status', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('modified_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('modified_date_gmt', self.gf('django.db.models.fields.DateField')(null=True)),
            ('content_filtered', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('parent', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('menu_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('content_mime_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('comment_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'blog', ['Post'])

        # Adding model 'PostMeta'
        db.create_table(u'blog_postmeta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Post'])),
            ('meta_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'blog', ['PostMeta'])

        # Adding model 'Comment'
        db.create_table(u'blog_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Post'])),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('author_IP', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True)),
            ('author_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_gmt', self.gf('django.db.models.fields.DateField')(null=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('approved', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('parent', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.UserProfile'])),
        ))
        db.send_create_signal(u'blog', ['Comment'])

        # Adding model 'CommentMeta'
        db.create_table(u'blog_commentmeta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Comment'])),
            ('meta_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'blog', ['CommentMeta'])

        # Adding model 'Category'
        db.create_table(u'blog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'blog', ['Category'])


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table(u'blog_post')

        # Deleting model 'PostMeta'
        db.delete_table(u'blog_postmeta')

        # Deleting model 'Comment'
        db.delete_table(u'blog_comment')

        # Deleting model 'CommentMeta'
        db.delete_table(u'blog_commentmeta')

        # Deleting model 'Category'
        db.delete_table(u'blog_category')


    models = {
        u'account.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'blog_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'head_portrait': ('django.db.models.fields.files.ImageField', [], {'default': "'./head_protrait/no-img.jsp'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nicename': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'registration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'blog.category': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'blog.comment': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Comment'},
            'approved': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'author_IP': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'author_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_gmt': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'post_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Post']"}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.UserProfile']"})
        },
        u'blog.commentmeta': {
            'Meta': {'object_name': 'CommentMeta'},
            'comment_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Comment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_value': ('django.db.models.fields.TextField', [], {})
        },
        u'blog.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.UserProfile']"}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_filtered': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'content_mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_gmt': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'excerpt': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'modified_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'modified_date_gmt': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'parent': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'blog.postmeta': {
            'Meta': {'object_name': 'PostMeta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_value': ('django.db.models.fields.TextField', [], {}),
            'post_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Post']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blog']