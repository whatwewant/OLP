# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.shortcuts import render

from blog.models import Post
from utils.shortcuts import get_hot_read_articles_by_userprofile_for_index
from utils.shortcuts import get_hot_comments_articles_by_userprofile_for_index
from utils.shortcuts import get_active_userprofiles

def index(request):
    # print dir(request)
    authenticated = request.user.is_authenticated()
    userprofile = None
    articles = Post.objects.filter(show=True) # [:9]
    articles_hot_read = get_hot_read_articles_by_userprofile_for_index()
    articles_hot_comments = get_hot_comments_articles_by_userprofile_for_index()
    if authenticated:
        userprofile = request.user.userprofile
    active_users = get_active_userprofiles()

    return render(request, 'index.html', {'authenticated':authenticated,
                                          'user':userprofile, 
                                          'articles':articles,
                                          'articles_hot_read': articles_hot_read,
                                          'articles_hot_comments': articles_hot_comments,
                                          'active_users': active_users,
                                         })
