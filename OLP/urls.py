# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

# @TODO he included urlconf OLP.urls doesn't have any patterns in it
# I donot know why, but if you close admin.autodiscover(), may work
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OLP.views.home', name='home'),
    # url(r'^OLP/', include('OLP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^index/$', 'account.views.index', name='index'),

    # upload
    url(r'^uploadimage/$', 'blog.views.ke_upload_image', name='upload_image'),
    url(r'^(?P<authorname>\w+)/uploadimage/$', 'blog.views.ke_upload_image', name='upload_image'),
    url(r'^(P<authorname>\w+)/uploadaudio/$', 'blog.views.ke_upload_audio', name='upload_audio'),

    # user 
    url(r'^sign_in/$','account.views.sign_in', name='sign_in'),
    url(r'^sign_up/$', 'account.views.sign_up', name='sign_up'),
    url(r'^sign_out/$', 'account.views.sign_out', name='sign_out'),
    url(r'^(?P<username>\w+)/userinfo/$', 'account.views.user_info', name='user_info'),
    url(r'^(?P<username>\w+)/loginhistory/$', 'account.views.get_user_login_history', name='history'),
    # upload portrait
    url(r'^(?P<username>\w+)/upload_portrait/$', 'account.views.upload_portrait', name='upload_portrait'),

    # blog
    url(r'^$', 'home.views.index', name='index'),
    url(r'^blog/write/$', 'blog.views.write', name='blog_write'),
    url(r'^(?P<authorname>\w+)/$', 'blog.views.personPage', name='blog_author'),
    # article
    url(r'^blog/edit/(?P<pk>\d+)/$', 'blog.views.edit', name='article_edit'),
    url(r'^(?P<authorname>\w+)/article/(?P<pk>\d+)/$', 'blog.views.post', name='post'),
    url(r'^blog/delete/(?P<pk>\d+)/$', 'blog.views.delete', name='article_delete'),
    url(r'^blog/undelete/(?P<pk>\d+)/$', 'blog.views.undelete', name='article_undelete'),
    url(r'^blog/deepdelete/(?P<pk>\d+)/$', 'blog.views.delete', name='article_deepdelete'),
    # 收藏别人的文章
    url(r'^(?P<authorname>\w+)/collectarticle/(?P<pk>\d+)/$', 'blog.views.collect', name='article_collect'),
    url(r'^(?P<authorname>\w+)/deletecollection/(?P<pk>\d+)/$', 'blog.views.delete_collect', name='delete_collect'),
    # 自己收藏的所有文章
    url(r'^(?P<authorname>\w+)/collections/$', 'blog.views.collections', name='collections'),
    # category
    url(r'(?P<authorname>\w+)/category/(?P<pk>\d+)/$', 'blog.views.category', name='category'),
    # category_by_date
    url(r'^(?P<author>\w+)/category_by_date/(?P<year>\d+)/(?P<month>\d+)/$', 'blog.views.category_by_date', name='category_by_date'),
    # Search 
    url(r'^(?P<authorname>\w+)/search/$', 'blog.views.search', name='search'),

    # Mail
    url(r'^(?P<authorname>\w+)/sendmail/$', 'blog.views.send_one_mail', name='send_one_mail'),

    # links
    url(r'^(?P<authorname>\w+)/friendlinks/$', 'links.views.show_friend_links', name='friend_links'),
    url(r'(?P<authorname>\w+)/friendlinks/delete/(?P<pk>\d+)', 'links.views.delete_friend_links', name='delete_friend_links'),
)
