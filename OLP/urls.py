# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OLP.views.home', name='home'),
    # url(r'^OLP/', include('OLP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', 'account.views.index', name='index'),

    # user 
    url(r'^sign_in/$','account.views.sign_in', name='sign_in'),
    url(r'^sign_up/$', 'account.views.sign_up', name='sign_up'),
    url(r'^sign_out/$', 'account.views.sign_out', name='sign_out'),
    url(r'^userinfo/$', 'account.views.user_info', name='user_info'),
    url(r'^loginhistory/$', 'account.views.get_user_login_history', name='history'),

    # blog
    url(r'^$', 'blog.views.homePage', name='homepage'),
    url(r'^blog/$', 'blog.views.homePage'),
    url(r'^blog/index/$', 'blog.views.homePage'),
    url(r'^blog/write/$', 'blog.views.write', name='blog_write'),
    url(r'^blog/edit/(?P<pk>\d+)/$', 'blog.views.edit', name='blog_edit'),
    url(r'^blog/(?P<author>\w+)/$', 'blog.views.personPage', name='blog_author'),
    url(r'^(?P<author>\w+)/$', 'blog.views.personPage', name='blog_index'),
    # article
    url(r'^(?P<author>\w+)/article/(?P<pk>\d+)/$', 'blog.views.post', name='post'),
    url(r'^blog/delete/(?P<pk>\d+)/$', 'blog.views.delete', name='delete'),
    url(r'^blog/undelete/(?P<pk>\d+)/$', 'blog.views.undelete', name='undelete'),
    url(r'^blog/delete/(?P<pk>\d+)?deepdelete=(?P<deepdelete>\w+)/$', 'blog.views.delete', name='deepdelete'),
    # category
    url(r'(?P<author>\w+)/category/(?P<pk>\d+)/$', 'blog.views.category', name='category'),
    # upload
    url(r'uploadimage/$', 'blog.views.ke_upload_image', name='upload_image'),
    url(r'uploadaudio/$', 'blog.views.ke_upload_audio', name='upload_audio'),

    # Mail
    url(r'^sendmail/$', 'blog.views.send_one_mail', name='send_one_mail'),
)
