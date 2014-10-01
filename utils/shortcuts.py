#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpRequest
from django.utils import timezone

from account.models import UserProfile
from blog.models import Post, Category, Visit, VisitBlog
from blog.models import PostToVisit, PostToCategory
# from links.models import Links
from utils import html_tags_filter

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
    posts = Post.objects.filter(author=userprofile, show=True).order_by('-visits')[:5]
    return posts

def visit_plus_plus(article):
    # 访问单篇文章，访问量修正/增加
    # article.visits = article.visit.count()
    article.visits += 1
    article.save()
    return True

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
    articles_all = Post.objects.filter(author=userprofile, show=True)
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
    return HttpRequest.get_host(request)

def get_request_url(request):
    return request.META.get('HTTP_REFERER', '/')

def visit_post(request, userprofile, authorprofile, post):
    '''访问单篇文章'''
    # 相同ip + userprofile + date 一天访问增加一次
    if not userprofile:
        userprofile = get_anonymous()
    if userprofile != authorprofile:
        if not Visit.objects.filter(
            visitor = userprofile,
            ip = get_ip(request),
            date_visited = date.today(),
            ).exists() :
            geted, created = Visit.objects.get_or_create(
                visitor = userprofile,
                ip = get_ip(request),
                date_visited = date.today(),
                )
            PostToVisit.objects.get_or_create(post=post, visit=geted)
            visit_plus_plus(post)
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
            date_visited = date.today(),
            )
        return geted
    return False

def anonymous_redirected(function=None, redirect_url=None):
    def wrapper(request, authorname, pk=None):
        if authorname == 'anonymous':
            return redirect('/')
        return function(request, authorname, pk)
    return wrapper

def LinkPostToCategory(post, category):
    PostToCategory.objects.get_or_create(post=post, category=category)

def store_article(author, title, content):
    """
        create article
    """
    return Post.objects.create(author=author, 
                        title=title, 
                        name=title[:10],
                        content=content, 
                        excerpt=html_tags_filter(content)[:300],
                        modified_date=date.today(),
                        modified_date_gmt=timezone.now())

def get_category_by_author_and_name(author, name):
    get, created = Category.objects.get_or_create(author=author, name=name)
    return get


def write_article(author, title, content, category_name):
    '''
        store article
    '''
    if Post.objects.filter(author=author, title=title).exists():
        return 
    # 积分增加
    integral_plus_plus(author)
    # create Post
    post = store_article(author, title, content)
    # get or create category
    category = get_category_by_author_and_name(author, category_name)
    # Links post and category
    PostToCategory.objects.get_or_create(
                    post=post, 
                    category=category)

def write_article_unknown_category(author, title, content):
    '''未分类'''
    write_article(author, title, content, u'未分类')

def write_article_unknown_category_and_author(title, content):
    '''
        临时存储
    '''  
    author = get_userprofile_by_username('Rainy')
    write_article_unknown_category(author, title, content)

def integral_plus_plus(author, article_type=None):
    # 只有新写文章时会积分
    # article_type 原创,转载,
    article_types = {'original': 10, # 原创
                     'reprint': 4, # 转载
                     'translation': 6, # 翻译
                     'default': 2, # 默认
                    }
    if article_type != None:
        author.integral += article_types[article_type]
    else:
        author.integral += article_types['default']
    author.save()
    return True

def integral_plus_plus_by_authorname(authorname, article_type=None):
    return integral_plus_plus(get_userprofile_by_username(authorname), article_type)

def rank_renew():
    # 定期进行等级排序, 这里每天更新,timedelta(n)表示n天
    if date.today() - UserProfile.objects.all()[0].rank_renew_date == datetime.timedelta(0):
        return False
    
    # ... 顺便更新jianshu
    #from JianShu_Django import store 
    #store()

    all_user = UserProfile.objects.order_by('-integral', '-blog_num', '-visits', 'register_date')
    k = 1
    for user in all_user:
        user.rank = k
        user.rank_renew_date = date.today()
        user.save()
        k += 1
    return True

def get_hot_read_articles_by_userprofile(userprofile):
    if userprofile == None:
        return Post.objects.filter(show=True).order_by('-visits')[:10]
    return Post.objects.filter(author=userprofile, show=True).order_by('-visits')[:10]

def get_hot_read_articles_by_userprofile_for_index():
    return get_hot_read_articles_by_userprofile(None)
    
def get_hot_comments_articles_by_userprofile(userprofile):
    if userprofile == None:
        return Post.objects.filter(show=True).order_by('-visits')[:10]
    return Post.objects.filter(author=userprofile, show=True).order_by('-visits')[:10]

def get_hot_comments_articles_by_userprofile_for_index():
    return get_hot_read_articles_by_userprofile(None)
    

