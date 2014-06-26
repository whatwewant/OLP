# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _   

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=30, default=u'Just arrived')
    integral = models.IntegerField(null=False, default=0)
    registration = models.BooleanField(default=False)
    blog_num = models.IntegerField(u'文章数量', default=0)
    grade = models.CharField(u'等级', max_length=9, default='--- --- ---')
    visits = models.IntegerField(u'访问量', default=0)
    rank = models.IntegerField(u'排名', default=0)
    head_portrait = models.ImageField(upload_to='./head_portrait', 
                                      default='./head_portrait/no-img.jsp',
    #                                  height_field=100, width_field=100,
                                      max_length=255)

    def __unicode__(self):
        return u'user name is %s, id = %s' %(self.user.username, self.id)

    class Meta:
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfiles')

class UserMeta(models.Model):
    user_id = models.ForeignKey(UserProfile)
    meta_key = models.CharField(max_length=255)
    meta_value = models.TextField()

    def __unicode__(self):

        return u'user name is %s and mete_key is %s' %(self.user_id.user.username,
                                                       self.meta_key)

# @TODO
class UserInfo(models.Model):
    # @TODO
    name = models.CharField(u'真实姓名', max_length=255, null=True)
    sex = models.CharField(u'性别', default='None', max_length='5')
    age = models.IntegerField(u'年龄', default=0, max_length=3)
    userprofile = models.ForeignKey(UserProfile)
    hometown = models.CharField(u'家乡', max_length=255, null=True)
    zip_code = models.IntegerField(u'邮编', max_length=7, null=True)
    qq = models.IntegerField(u'QQ', max_length=25, null=True)
    phone = models.IntegerField(u'Phone', max_length=255, null=True)
    country = models.CharField(u'国家', max_length=255, null=True)
    country_code = models.CharField(u'国家代号', max_length=3, default='+86')
    language = models.CharField(u'语言', max_length=255, default='Chinese')
    recovery_email = models.EmailField(u'辅助邮箱', max_length=255, null=True)
    web_site = models.URLField(u'个人网站', max_length=255, null=True)

    def __unicode__(self):

        return u'{username}\'s Detailed UserInfo'.format(username=self.userprofile.user.username)


class UserLoginHistory(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(u'当前时间', auto_now=True)
    login_ip = models.CharField(u'当前登入ip', max_length=255, null=True)
    login_address = models.CharField(u'当前地点', max_length=255, default=u'未知')

    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):

        return u'{username}\'s Detailed User Login Histories'.format(username=self.userprofile.user.username)
