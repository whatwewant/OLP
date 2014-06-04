from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _   

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=30)
    integral = models.IntegerField(null=False, default=0)
    registration = models.BooleanField(default=False)
    blog_num = models.IntegerField(default=0)
    head_portrait = models.ImageField(upload_to='./head_protrait', default='./head_protrait/no-img.jsp')

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
