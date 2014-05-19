from django.db import models
from django.utils.translation import ugettext_lazy as _   

from account.models import UserProfile
class Post(models.Model):
    '''blog '''

    author = models.ForeignKey(UserProfile)
    date = models.DateField(auto_now_add=True)
    date_gmt = models.DateField(null=True)
    content = models.TextField()
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=500)
    status = models.CharField(max_length=20, null=True)
    comment_status = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)

    modified_date = models.DateField(null=True)
    modified_date_gmt = models.DateField(null=True)
    content_filtered = models.CharField(max_length=200, null=True)
    parent = models.BigIntegerField(null=True)
    menu_order = models.IntegerField(null=True)
    content_type = models.CharField(max_length=20, null=True)
    content_mime_type = models.CharField(max_length=255, null=True)
    comment_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


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
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')



class CommentMeta(models.Model):
    comment_id = models.ForeignKey(Comment)
    meta_key = models.CharField(max_length=255)
    meta_value = models.TextField()


    def __unicode__(self):
        return str(self.meta_key)


