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
     url(r'^login/$','account.views.user_login', name='login'),
     url(r'^index/$', 'account.views.index', name='index'),
     url(r'^register/$', 'account.views.register', name='register'),

)
