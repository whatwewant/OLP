# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _   

from account.models import UserProfile
# from django.contrib.auth.models import User

class Category(models.Model):
    '''文章分类'''

    author = models.ForeignKey(UserProfile)
    name = models.CharField(u'文章分类', max_length=64)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('category', (), {'pk':self.pk})


class Post(models.Model):
    '''blog '''

    author = models.ForeignKey(UserProfile)
    date = models.DateField(auto_now_add=True)
    # @TODO
    date_gmt = models.DateField(null=True)
    content = models.TextField()
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=500)
    # @TODO
    status = models.CharField(max_length=20, null=True)
    # @TODO
    comment_status = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)

    modified_date = models.DateField(null=True)
    modified_date_gmt = models.DateField(null=True)
    # @TODO
    content_filtered = models.CharField(max_length=200, null=True)
    # @TODO
    parent = models.BigIntegerField(null=True)
    # @TODO
    menu_order = models.IntegerField(null=True)
    content_type = models.CharField(max_length=20, null=True)
    # @TODO
    content_mime_type = models.CharField(max_length=255, null=True)
    comment_count = models.IntegerField(default=0)
    # 文章分类
    po_type = models.ManyToManyField(Category, through='PostToCategory',
                                blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-pk']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    @models.permalink
    def get_absolute_url(self):
        return ('post', (), 
                {'author':self.author.user.username, 'pk':self.pk})

    def get_categories(self):
        return self.po_type.all()


class PostToCategory(models.Model):
    '''Build MemberShip Between Post And Category'''
    post = models.ForeignKey(Post)
    category = models.ForeignKey(Category)
    date_joined = models.DateField(auto_now_add=True)


class PostMeta(models.Model):

    post_id = models.ForeignKey(Post)
    meta_key = models.CharField(max_length=255)
    meta_value = models.TextField()
    
    def __unicode__(self):
        return set(self.meta_key)

class Comment(models.Model):
    
    post_id = models.ForeignKey(Post)
    author = models.CharField(max_length=200, null=True)
    author_IP = models.IPAddressField(null=True)
    author_url = models.CharField(max_length=200, null=True)
    date = models.DateField(auto_now_add=True)
    date_gmt = models.DateField(null=True)
    content = models.TextField()

    approved = models.CharField(max_length=20, null=True)
    parent = models.BigIntegerField(default=0)
    user_id = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['-id']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

class CommentMeta(models.Model):
    comment_id = models.ForeignKey(Comment)
    meta_key = models.CharField(max_length=255)
    meta_value = models.TextField()


    def __unicode__(self):
        return str(self.meta_key)

