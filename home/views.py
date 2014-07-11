# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.shortcuts import render

from blog.models import Post

def index(request):
    # print dir(request)
    authenticated = request.user.is_authenticated()
    userprofile = None
    articles = Post.objects.filter(show=True) # [:9]
    if authenticated:
        userprofile = request.user.userprofile
    return render(request, 'index.html', {'authenticated':authenticated,
                                          'user':userprofile, 
                                          'articles':articles})
