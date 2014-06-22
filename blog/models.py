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
    # post_count = models.IntegerField(u'文章数统计', default=0)

    class Meta:
        ordering = ['-pk']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('category', (), {'pk':self.pk})
    
    # 文章数统计
    def get_post_count(self):
        return self.post_set.count()


class Post(models.Model):
    '''blog '''

    author = models.ForeignKey(UserProfile)
    date = models.DateField(u'发布时间', auto_now_add=True)
    # @TODO
    date_gmt = models.DateField(u'发布时间', null=True)
    content = models.TextField()
    title = models.CharField(u'文章标题', max_length=200)
    name = models.CharField(u'文章标题缩写', max_length=40)
    excerpt = models.CharField(u'摘录', max_length=500)
    # @TODO
    status = models.CharField(u'文章状态(publish/auto-draft/inherit)', max_length=20, default='public')
    # @TODO
    comment_status = models.CharField(u'评论状态(open/close)', max_length=20, default='open')
    password = models.CharField(u'文章密码', max_length=20, null=True)

    modified_date = models.DateField(null=True)
    modified_date_gmt = models.DateField(null=True)
    # @TODO
    content_filtered = models.CharField(max_length=200, null=True)
    # @TODO
    parent = models.BigIntegerField(u'父文章', null=True)
    # @TODO
    menu_order = models.IntegerField(u'排序ID', null=True)
    content_type = models.CharField(max_length=20, null=True)
    # @TODO
    content_mime_type = models.CharField(u'MIME类型', max_length=255, null=True)
    comment_count = models.IntegerField(u'评论总数', default=0)
    # 文章分类
    po_type = models.ManyToManyField(Category, through='PostToCategory',
                                blank=True, null=True)
    # 默认显示， 用于删除文章进入垃圾箱
    show = models.BooleanField(default=True)

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

    def get_full_of_article(self):
        return self.content

    def get_excerpt_of_article(self):
        return self.excerpt

    # 重载delete方法


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
    author = models.CharField(u'评论者', max_length=200, null=True)
    author_email = models.EmailField(u'评论者邮箱', null=True)
    author_url = models.CharField(u'评论者URL', max_length=200, null=True)
    author_IP = models.IPAddressField(u'评论者IP', null=True)
    date = models.DateField(u'评论时间', auto_now_add=True)
    date_gmt = models.DateField(null=True)
    content = models.TextField()

    approved = models.CharField(u'评论是否被批准', max_length=20, null=True)
    parent = models.BigIntegerField(u'父评论ID', default=0)
    # @TODO 评论者用户ID(不一定存在)
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

