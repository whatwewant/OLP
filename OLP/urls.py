# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from account import views
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

	# blog
	url(r'^blog/index/$', 'blog.views.index', name='blog_index'),
	url(r'^blog/write/$', 'blog.views.write', name='blog_write'),
)
