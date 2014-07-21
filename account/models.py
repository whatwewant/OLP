# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _   

# @TODO This Will report error
# from blog.models import Visit
# from blog.models import UserProfileToVisit

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=30, default=u'Just arrived')
    integral = models.IntegerField(null=False, default=0)
    registration = models.BooleanField(default=False)
    register_date = models.DateField(u'注册时间', auto_now_add=True)
    blog_num = models.IntegerField(u'文章数量', default=0)
    grade = models.CharField(u'等级', max_length=9, default='--- --- ---')
    visits = models.IntegerField(u'访问量', default=0)
    # visits = models.ManyToManyField(Visit, through='UserProfileToVisit', blank=True, null=True)
    rank = models.IntegerField(u'排名', default=0)
    head_portrait = models.ImageField(upload_to='head_portrait', 
                                      default='./head_portrait/no-img.jsp',
    #                                  height_field=100, width_field=100,
                                      max_length=255)

    class Meta:
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfiles')

    def __unicode__(self):
        return u'user name is %s, id = %s' %(self.user.username, self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('blog_author', (), {'authorname':self.user.username})

    # 获取本作者家目录提交的search
    @models.permalink
    def get_search_url(self):
        return ('search', (), {'authorname':self.user.username})


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
    userprofile = models.ForeignKey(UserProfile)
    name = models.CharField(u'真实姓名', max_length=255, default='')
    sex = models.CharField(u'性别', max_length='5', default='')
    age = models.CharField(u'年龄', max_length=3, default='')
    hometown = models.CharField(u'家乡', max_length=255, default='')
    zip_code = models.CharField(u'邮编', max_length=7, default='')
    qq = models.IntegerField(u'QQ', max_length=25, blank=True, null=True)
    phone = models.IntegerField(u'Phone', max_length=255, blank=True, null=True)
    country = models.CharField(u'国家', max_length=255, default='')
    country_code = models.CharField(u'国家代号', max_length=3, default='+86')
    language = models.CharField(u'语言', max_length=255, default='Chinese')
    recovery_email = models.EmailField(u'辅助邮箱', max_length=255, blank=True, default='@gmail.com')
    web_site = models.URLField(u'个人网站', max_length=255, blank=True, default='http://')

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

        return u'{username}\'s Detailed User Login Histories'.format(username=self.user.username)


