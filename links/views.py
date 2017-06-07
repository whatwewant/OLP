# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from links.models import Links
from account.models import User, UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.cache import cache_page

from utils.shortcuts import is_permitted, get_userprofile_by_username
from utils.shortcuts import get_anonymous

from blog.models import VisitBlog

@cache_page(60 * 15)
def show_friend_links(request, authorname):
    authorprofile = get_userprofile_by_username(authorname)
    authenticated = request.user.is_authenticated()
    permission, userprofile = is_permitted(request, authenticated, authorprofile)
    all_visits = VisitBlog.objects.filter(author=authorprofile).count()
    all_visitors = VisitBlog.objects.filter(author=authorprofile).exclude(visitor=get_anonymous())[:9]
    
    if permission and request.method == "POST":
        owner = userprofile
        url = request.POST.get('urlInput').strip()
        name = request.POST.get('nameInput').strip()
        # image
        # target
        description = request.POST.get('descriptionInput').strip()
        #visible = request.POST.get('visible').strip()
        # rating 

        link, link_creat = Links.objects.get_or_create(owner=owner,
                                                      url=url, name=name,
                                                      description=description,
                                                      # visible=visible
                                                      )
        return redirect('friend_links', userprofile.user.username)
        

    friend_links = Links.objects.filter(owner=authorprofile)

    return render(request, 'links/friend_links.html', {'user':userprofile,
                                'author':authorprofile,
                                'authenticated':authenticated,
                                'permission':permission,
                                'friend_links': friend_links,
                                'all_visits': all_visits,
                                'all_visit': all_visitors,
                               })

@login_required(login_url='sign_in')
def add_friend_links(request, authorname):
    user = request.user.userprofile
    
    if request.method == "POST":
        owner = user
        url = request.POST.get('url').strip()
        name = request.POST.get('name').strip()
        # image
        # target
        description = request.POST.get('description').strip()
        visible = request.POST.get('visible').strip()
        # rating 

        link, link_creat = Links.objects.get_or_create(owner=owner,
                                                      url=url, name=name,
                                                      description=description,
                                                      visible=visible)
        return redirect('friend_links', user.user.name)

    return redirect('friend_links', user.user.name)

@login_required(login_url='sign_in')
def delete_friend_links(request, authorname, pk):
    '''delete friend links'''
    user = request.user.userprofile
    link = get_object_or_404(Links, owner=user, pk=pk)
    link.delete()

    return redirect('friend_links', user.user.username)

