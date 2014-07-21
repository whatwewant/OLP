#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from account.models import UserProfile
from blog.models import Post, Category, Visit, VisitBlog
from blog.models import PostToVisit
# from links.models import Links

def get_user(username):
    user = get_object_or_404(User, username=username)
    return user

def get_userprofile_by_username(username):
    user = get_user(username)
    userprofile = get_object_or_404(UserProfile, user=user)
    return userprofile

def get_userprofile_by_user(user):
    userprofile = get_object_or_404(UserProfile, user=user)
    return userprofile

def get_posts_by_username(username):
    userprofile = get_userprofile_by_username(username)
    posts = Post.objects.filter(author=userprofile, show=True)
    return posts

def get_posts_by_userprofile(userprofile):
    posts = Post.objects.filter(author=userprofile, show=True)
    return posts

def get_posts_by_visit(userprofile):
    posts = Post.objects.filter(author=userprofile).order_by('-visit')[:5]
    return posts

def get_one_post_by_username_and_pk(username, pk):
    userprofile = get_userprofile_by_username(username)
    post = get_object_or_404(author=userprofile, show=True, pk=pk)
    return post

def get_one_post_by_userprofile_and_pk(userprofile, pk):
    post = get_object_or_404(author=userprofile, show=True, pk=pk)
    return post

def get_categories_by_username(username):
    userprofile = get_userprofile_by_username(username)
    categories = Category.objects.filter(author=userprofile)
    return categories

def get_categories_by_userprofile(userprofile):
    categories = Category.objects.filter(author=userprofile)
    return categories

def get_categories_by_date(userprofile=None):
    '''
        按日期获得文章, 10个
    '''
    if not userprofile:
        return None

    month_register = userprofile.register_date.month
    year_register = userprofile.register_date.year

    month_now = date.today().month
    year_now = date.today().year

    categories = list()
    articles_all = Post.objects.filter(author=userprofile)
    while year_register <= year_now and month_register <= month_now:
        articles = articles_all.filter(date__year=year_now, 
                                date__month=month_now)
        if articles.count() != 0:
            count = articles.count()
            url = r'/%s/category_by_date/%s/%s/' % (userprofile.user.username, year_now, month_now)
            year_and_month = str(year_now)+'-'+str(month_now)
            
            t = {'date':year_and_month, 'count':count, 'url':url}
            categories.append(t)

        month_now -= 1
        if month_register < 1:
            month_now = 12
            year_now -= 1

    return categories


def get_anonymous():
    # @TODO
    user = None
    userprofile = None
    if not User.objects.filter(username='anonymous').exists():
        user = User.objects.create_user(username='anonymous',password='anonymous')
    else:
        user = User.objects.get(username='anonymous')
    if not UserProfile.objects.filter(user=user).exists():
        userprofile = UserProfile.objects.create(user=user, nickname='anonymous')
    else:
        userprofile = UserProfile.objects.get(user=user)
    return userprofile

def check_anonymous(userprofile):
    anonymous = get_anonymous()
    if userprofile == anonymous:
        return None
    return userprofile

def is_permitted(request, authencated=False, authorprofile=None, userprofile=None):
    '''是否获得各种操作权限'''
    # @TODO 只允许本博客的使用者
    # userprofile = get_anonymous()
    if not authencated:
        return (False, userprofile)
    userprofile = request.user.userprofile
    if userprofile != authorprofile:
        return (False, userprofile)
    return (True, userprofile)

def get_ip(request):
    return request.META.get('REMOTE_ADDR')

def get_request_url(request):
    return request.META.get('HTTP_REFERER', '/')

def visit_post(request, userprofile, authorprofile, post):
    '''访问文章'''
    if not userprofile:
        userprofile = get_anonymous()
    if userprofile != authorprofile:
        geted, created = Visit.objects.get_or_create(
            visitor = userprofile,
            ip = get_ip(request),
            date = date.today()
            )
    PostToVisit.objects.get_or_create(post=post, visit=geted)
    return True

def visit_blog(request, userprofile, authorprofile):
    '''访问博客'''
    if not userprofile:
        userprofile = get_anonymous()
    if userprofile != authorprofile:
        geted, created = VisitBlog.objects.get_or_create(
            author = authorprofile,
            visitor = userprofile,
            ip = get_ip(request),
            date = date.today()
            )
        return geted
    return False

