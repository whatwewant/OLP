# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

from blog.models import Post, Category, PostToCategory, Visit, PostToVisit
from blog.models import CollectArticle
# from account.models import UserProfile
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_list_or_404
# from django.http import Http404
from django.utils import timezone
from datetime import date

from utils.utils import ke_upload_image, ke_upload_audio, send_one_mail
from utils.utils import html_tags_filter

from utils.shortcuts import *


def personPage(request, authorname):
    '''
        Person Blog Home Page
    '''
    #for k, v in request.META.items():
    #    print k,':',v
    # print author
    # print dir(request.user)
    # print request.user.is_authenticated()
    # user

    # articles author
    authorprofile = get_userprofile_by_username(authorname)

    authenticated = request.user.is_authenticated() 
    permission, userprofile = is_permitted(request, authenticated, authorprofile)

    # 更新排名
    rank_renew()

    # visit blog
    visit_blog(request, userprofile, authorprofile)
    # all visit this blog visitor
    all_visit = VisitBlog.objects.filter(author=authorprofile).exclude(visitor=get_anonymous())[:9]

    articles = get_posts_by_userprofile(authorprofile)
    articles_by_visit = get_posts_by_visit(authorprofile)
    categories = get_categories_by_userprofile(authorprofile)
    categories_by_date = get_categories_by_date(authorprofile)

    return render(request, 'blog/index.html', {'author':authorprofile, 
                                        'user':userprofile,
                                        'articles':articles, 
                                        'articles_by_visit':articles_by_visit,
                                        'authenticated':authenticated,
                                        'permission':permission,
                                        'categories':categories,
                                        'categories_by_date':categories_by_date,
                                        'all_visit':all_visit,
                                        })

@login_required(login_url='sign_in')
def write(request):
    '''publish an article'''
    user = request.user.userprofile
    categories = get_categories_by_userprofile(user)
    # all visit this blog visitor
    all_visit = VisitBlog.objects.filter(author=user).exclude(visitor=get_anonymous())[:9]

    if request.method == "POST" :
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()
        excerpt = request.POST.get('excerpt').strip()
        # new 文章分类
        categorylist = request.POST.get('category').strip().split(',')
        # old categorylist
        oldcategories = request.POST.getlist('oldcategories')
        # password= request.POST.get('password')
        # 文章类型,用于积分
        article_type = None
        modified_date = date.today()
        modified_date_gmt = timezone.now()
        # content_type = request.POST.get('content_type')
        if not title or not content:
            return redirect('blog_author', request.user.username)
        
        name = title
        if len(name) > 10:
            name = name[:10]+'...'

        if not excerpt:
            excerpt = html_tags_filter(content)[:300]

        # 该作者文章不许同名
        # 未做提示处理
        if Post.objects.filter(author=user,title=title).exists:
            return redirect('blog_author', request.user.username)

        # 积分
        integral_plus_plus(author, article_type)
        # 
        pp, pcreated = Post.objects.get_or_create(author=user, 
                            title=title, name = name,
                            content=content, excerpt=excerpt,
                            modified_date=modified_date,
                            modified_date_gmt=modified_date_gmt)

        if categorylist[0] != "":
            for new_category_name in categorylist:
                new_category_name = new_category_name.strip()
                if not new_category_name or new_category_name == "" :
                    continue
                cp, ccreated = Category.objects.get_or_create(author=user, name=new_category_name)
                PostToCategory.objects.get_or_create(post=pp, category=cp)
        else:
            new_category_name = u'未分类'
            cp, ccreated = Category.objects.get_or_create(author=user, name=new_category_name)
            PostToCategory.objects.get_or_create(post=pp, category=cp)

        # oldcategories
        for oldcategory in oldcategories:
            oldcategory = Category.objects.get(author=user, name=oldcategory)
            PostToCategory.objects.get_or_create(post=pp, category=oldcategory)


        # 文章数 +1
        user.blog_num += 1
        user.save()
        return redirect('blog_author', request.user.username)
    return render(request, 'blog/write.html', {'user':user,
                                               'author':user,
                                               'permission':True,
                                               'categories':categories,
                                               'authenticated':True,
                                               'all_visit':all_visit,
                                              })
	
@login_required(login_url='sign_in')
def edit(request, pk):
    '''
	edit view
    '''
    user = request.user.userprofile
    article = get_object_or_404(Post, author=user, pk=pk, show=True)
    categories = get_categories_by_userprofile(user)
    
    # all visit this blog visitor
    all_visit = VisitBlog.objects.filter(author=authorprofile).exclude(visitor=get_anonymous())[:9]

    if request.method == "POST":
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()
        excerpt = request.POST.get('excerpt').strip()
        # new 文章分类
        categorylist = request.POST.get('category').strip().split(',')
        # password= request.POST.get('password')
        modified_date = date.today()
        modified_date_gmt = timezone.now()
        # content_type = request.POST.get('content_type')
        if not title or not content:
            return redirect('blog_author', request.user.username)

        if not excerpt:
            excerpt = html_tags_filter(content)[:300]

        if categorylist[0] != "":
            for new_category_name in categorylist:
                new_category_name = new_category_name.strip()
                if new_category_name == "":
                    continue
                cp, ccreated = Category.objects.get_or_create(author=user, name=new_category_name)

                PostToCategory.objects.get_or_create(post=article, category=cp)

        # @TODO 判断是否和旧内容相同，如果相同就不用增加数据库存储负担
        # @TODO 不让空数据传存入数据库
        article.title = title
        article.content = content
        article.excerpt = excerpt
        article.categorylist = categorylist
        article.modified_date = modified_date
        article.modified_date_gmt = modified_date_gmt
        article.save()

        return redirect('blog_author', request.user.username)

    return render(request, 'blog/edit.html', {'user':user,
                                              'author':user,
                                              'article':article, 
                                              'categories':categories,
                                              'authenticated':True,
                                              'all_visit':all_visit,
                                             })


def search(request, authorname):

    keyword = request.GET.get('search').strip()

    if keyword == "":
        return redirect('blog_author', authorname)

    authorprofile = get_userprofile_by_username(authorname)
    authenticated = request.user.is_authenticated() 
    permission, userprofile = is_permitted(request, authenticated, authorprofile)
    
    # 更新排名
    rank_renew()
    # visit blog
    visit_blog(request, userprofile, authorprofile)
    # all visit this blog visitor
    all_visit = VisitBlog.objects.filter(author=authorprofile).exclude(visitor=get_anonymous())[:9]

    articles = get_list_or_404(Post, author=authorprofile, title__contains=keyword, show=True)
    articles_by_visit = get_posts_by_visit(authorprofile)
    categories = Category.objects.filter(author=authorprofile)
    categories_by_date = get_categories_by_date(authorprofile)
    return render(request, 'blog/search.html', {'author':authorprofile, 
                                        'user': userprofile,
                                        'articles':articles, 
                                        'articles_by_visit':articles_by_visit,
                                        'authenticated':authenticated,
                                        'permission':permission,
                                        'categories':categories,
                                        'categories_by_date':categories_by_date,
                                        'all_visit':all_visit,
                                        })


@login_required(login_url='sign_in')
def delete(request, pk, deepdelete=True):
    '''浅度删除'''
    author = request.user.userprofile
        
    article = get_object_or_404(Post, author=author, pk=pk, show=True)
    article.show = False
    article.save()
    return redirect('blog_author', request.user.username)


@login_required(login_url='sign_in')
def deepdelete(request, pk):
    '''深度删除'''
    author = request.user.userprofile

    article = get_object_or_404(Post, author=author, pk=pk)
    article.delete()
    return redirect('blog_author', request.user.username)
        

@login_required(login_url='sign_in')
def undelete(request, pk):
    author = request.user.userprofile
    article = get_object_or_404(Post, author=author, pk=pk, show=False)
    article.show = True
    article.save()
    return redirect('blog_author', request.user.username)

def post(request, authorname, pk):
    '''访问单篇文章'''
    authorprofile = get_userprofile_by_username(authorname)
    authenticated = request.user.is_authenticated()
    permission, userprofile = is_permitted(request, authenticated, authorprofile)

    article = get_object_or_404(Post, author=authorprofile, pk=pk) 
    categories = get_list_or_404(Category, author=authorprofile)
    articles_by_visit = get_posts_by_visit(authorprofile)
    categories_by_date = get_categories_by_date(authorprofile)

    # 更新排名
    rank_renew()
    # visit post recorded
    visit_post(request, userprofile, authorprofile, article)
    # visit blog recorded
    visit_blog(request, userprofile, authorprofile)
    # all visit this blog visitor
    all_visit = VisitBlog.objects.filter(author=authorprofile).exclude(visitor=get_anonymous())[:9]
    # if userprofile != authorprofile:
    #    geted, created = Visit.objects.get_or_create(visitor=userprofile, 
    #                                ip=request.META['REMOTE_ADDR'], 
    #                                date=date.today())
    #    PostToVisit.object.get_or_create(post=article, visit=geted)

    return render(request, 'blog/article.html', {'article':article, 
                                                'categories':categories,
                                                'categories_by_date':categories_by_date,
                                                'articles_by_visit':articles_by_visit,
                                                'author': authorprofile,
                                                'user':userprofile,
                                                'authenticated':authenticated,
                                                'permission':permission,
                                                'all_visit':all_visit,
                                                })

def category(request, authorname, pk):
    '''
        按分类名获取分类
    '''
    # 登入用户
    authorprofile = get_userprofile_by_username(authorname)
    authenticated = request.user.is_authenticated() 
    permission, userprofile = is_permitted(request, authenticated, authorprofile)

    # 更新排名
    rank_renew()
    # visit blog
    visit_blog(request, userprofile, authorprofile)
    # all visit this blog visitor
    all_visit = VisitBlog.objects.filter(author=authorprofile).exclude(visitor=get_anonymous())[:9]

    category = get_object_or_404(Category, author=authorprofile, pk=pk)
    articles = category.post_set.all()
    categories = get_list_or_404(Category, author=authorprofile)
    articles_by_visit = get_posts_by_visit(authorprofile)
    categories_by_date = get_categories_by_date(authorprofile)
    return render(request, 'blog/category.html', {'author':authorprofile,
                                                  'user':userprofile, 
                                                  'authenticated':authenticated,
                                                  'permission':permission,
                                                  'articles':articles,
                                                  'articles_by_visit':articles_by_visit,
                                                  'categories':categories,
                                                  'categories_by_date':categories_by_date,
                                                  'all_visit':all_visit,
                                                 })

def category_by_date(request, author, year, month):
    '''
        按月份获取分类
    '''
    authorprofile = get_userprofile_by_username(author)
    authenticated = request.user.is_authenticated()
    permission, userprofile = is_permitted(request, authenticated, authorprofile)

    # 更新排名
    rank_renew()
    # visit blog
    visit_blog(request, userprofile, authorprofile)
    # all visit this blog visitor
    all_visit = VisitBlog.objects.filter(author=authorprofile).exclude(visitor=get_anonymous())[:9]

    categories = get_list_or_404(Category, author=authorprofile)
    categories_by_date = get_categories_by_date(authorprofile)
    articles = Post.objects.filter(author=authorprofile, date__year=year, date__month=month).order_by('-date')
    articles_by_visit = get_posts_by_visit(authorprofile)

    return render(request, 'blog/category.html', {'author':authorprofile,
                                                  'user':userprofile, 
                                                  'authenticated':authenticated,
                                                  'permission':permission,
                                                  'articles':articles,
                                                  'articles_by_visit':articles_by_visit,
                                                  'categories':categories,
                                                  'categories_by_date':categories_by_date,
                                                  'all_visit':all_visit,
                                                 })


@login_required(login_url='sign_in')
def collect(request, authorname, pk):
    '''收藏文章'''
    # @TODO 这样做不好，要局部ajax
    # 收藏者
    userprofile = request.user.userprofile
    # 文章作者
    authorprofile = get_userprofile_by_username(authorname)
    post = get_object_or_404(Post, author=authorprofile, pk=pk)
    
    errorcode = -1
    errorinfo = u'已收藏过了'
    if userprofile != authorprofile:
        if not CollectArticle.objects.filter(user=userprofile, authorname=authorname, post=post).exists():
            CollectArticle.objects.create(user=userprofile, authorname=authorname, post=post)
            post.collected += 1
            post.save()
            errorcode = 0
            errorinfo = u'收藏成功'
    
    where_you_come = request.META.get('HTTP_REFERER', '/')
    return redirect(where_you_come)

@login_required(login_url='sign_in')
def delete_collect(request, authorname, pk):
    '''删除一篇藏的文章'''
    userprofile = request.user.userprofile
    # authorprofile = get_userprofile_by_username(authorname)
    # post = get_object_or_404(Post, author=author, pk=pk)
    
    collection = get_object_or_404(CollectArticle, user=userprofile, pk=pk)
    collection.delete()
    
    return redirect('collections', user.user.username)
    

def collections(request, authorname):
    '''显示收藏的文章'''
    authorprofile = get_userprofile_by_username(authorname)
    authenticated = request.user.is_authenticated()
    permission, userprofile = is_permitted(request, authenticated, authorprofile)
    
    articles = CollectArticle.objects.filter(user=authorprofile)

    # 更新排名
    rank_renew()
    # visit blog
    visit_blog(request, userprofile, authorprofile)
    # all visit this blog visitor
    all_visit = VisitBlog.objects.filter(author=authorprofile).exclude(visitor=get_anonymous())[:9]
        
    return render(request, 'blog/collect.html', {'user':userprofile,
                                                 'author':authorprofile,
                                                 'articles':articles,
                                                 'authenticated':authenticated,
                                                 'permission':permission,
                                                 'all_visit':all_visit,
                                                })
