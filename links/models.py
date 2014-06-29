# -*- coding: utf-8 -*-

from django.db import models
from account.models import UserProfile

class Links(models.Model):
    '''友情链接'''
    url = models.URLField(u'链接URL', max_length=200)
    name = models.CharField(u'链接标题', max_length=50)
    image = models.ImageField(u'链接图片', upload_to='./links', 
                              default='./head_portrait/no-img.jsp', max_length=255)
    target = models.CharField(u'链接的打开方式', max_length=200, blank=True, null=True)
    description = models.CharField(u'链接描述', max_length=255, blank=True, null=True)
    visible = models.CharField(u'是否可见', max_length='4', default="True")
    # 添加者用户ID
    owner = models.ForeignKey(UserProfile)
    rating = models.IntegerField(u'评分等级', default=0)
    updated = models.DateTimeField(u'更新时间', auto_now_add=True)
    rel = models.CharField(u'XFN关系', max_length=255, blank=True, null=True)
    notes = models.CharField(u'XFN注释', max_length=255, blank=True, null=True)
    rss = models.CharField(u'链接RSS地址', max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-updated']

    def __unicode__(self):
        return "%s Links" % self.name
