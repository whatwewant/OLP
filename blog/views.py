# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

from blog.models import Post, Category, PostToCategory, Visit
from blog.models import CollectArticle
from account.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_list_or_404
from django.http import Http404
from django.utils import timezone
from datetime import date

from .utils import ke_upload_image, ke_upload_audio, send_one_mail
from .utils import html_tags_filter
from .utils import get_articles_by_visit, get_categories_by_date

def homePage(request):
    # print dir(request)
    authenticated = request.user.is_authenticated()
    userprofile = None
    articles = Post.objects.filter(show=True) # [:9]
    if authenticated:
        userprofile = request.user.userprofile
    return render(request, 'index.html', {'authenticated':authenticated,
                                          'user':userprofile, 
                                          'articles':articles})

def personPage(request, author=False):
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
    author = get_object_or_404(User, username=author)
    authorprofile = UserProfile.objects.get(user=author)

    userprofile = None
    authenticated = False
    permission = False
    authenticated = request.user.is_authenticated() 
    if authenticated:
        userprofile = request.user.userprofile
        if userprofile == authorprofile:
            permission = True

    # visit
    ip = request.META['REMOTE_ADDR']
    today = date.today()
    if userprofile != authorprofile:
        if not Visit.objects.filter(user=authorprofile, post=-1, ip=ip, date=today).exists():
            Visit.objects.create(user=authorprofile, ip=ip, date=today)
            authorprofile.visits += 1
            authorprofile.save()


    articles = Post.objects.filter(author=authorprofile, show=True)
    articles_by_visit = get_articles_by_visit(authorprofile=authorprofile)
    categories = Category.objects.filter(author=authorprofile)
    categories_by_date = get_categories_by_date(authorprofile=authorprofile)

    return render(request, 'blog/index.html', {'author':authorprofile, 
                                        'user':userprofile,
                                        'articles':articles, 
                                        'articles_by_visit':articles_by_visit,
                                        'authenticated':authenticated,
                                        'permission':permission,
                                        'categories':categories,
                                        'categories_by_date':categories_by_date,
                                        })

@login_required(login_url='sign_in')
def write(request):
    '''publish an article'''
    user = request.user.userprofile
    if request.method == "POST" :
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
            return redirect('blog_index', request.user.username)
        
        name = title
        if len(name) > 10:
            name = name[:10]+'...'

        if not excerpt:
            excerpt = html_tags_filter(content)[:300]

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


        # 文章数 +1
        user.blog_num += 1
        user.save()
        return redirect('blog_index', request.user.username)
    return render(request, 'blog/write.html', {'user':user,
                                               'author':user,
                                               'permission':True,
                                               'authenticated':True})
	
@login_required(login_url='sign_in')
def edit(request, pk):
    '''
	edit view
    '''
    if request.method == "POST":
        user = request.user.userprofile
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
            return redirect('blog_index', request.user.username)

        if not excerpt:
            excerpt = html_tags_filter(content)[:300]

        if categorylist:
            for i in categorylist:
                cp, ccreated = Category.objects.get_or_create(author=user, name=i)

            article = Post.objects.get(author=user, pk=pk, show=True)
            # @TODO 判断是否和旧内容相同，如果相同就不用增加数据库存储负担
            # @TODO 不让空数据传存入数据库
            article.title = title
            article.content = content
            article.excerpt = excerpt
            article.categorylist = categorylist
            article.modified_date = modified_date
            article.modified_date_gmt = modified_date_gmt
            article.save()

            PostToCategory.objects.get_or_create(post=article, category=cp)

        return redirect('blog_index', request.user.username)

    user = request.user.userprofile
    article = get_object_or_404(Post, author=user, pk=pk, show=True)

    return render(request, 'blog/edit.html', {'user':user,
                                              'author':user,
                                              'article':article, 
                                              'authenticated':True})


def search(request, authorname):

    keyword = request.GET.get('search').strip()

    if keyword == "":
        return redirect('blog_index', authorname)

    author = get_object_or_404(User, username=authorname)
    authorprofile = get_object_or_404(UserProfile, user=author)
    userprofile = None
    authenticated = request.user.is_authenticated() 
    permission = False
    if authenticated:
        userprofile = request.user.userprofile
        if userprofile == authorprofile:
            permission = True #request.user.is_authenticated()


    articles = get_list_or_404(Post, author=authorprofile, title__contains=keyword, show=True)
    articles_by_visit = get_articles_by_visit(authorprofile=authorprofile)
    categories = Category.objects.filter(author=authorprofile)
    categories_by_date = get_categories_by_date(authorprofile=authorprofile)
    return render(request, 'blog/search.html', {'author':authorprofile, 
                                        'user': userprofile,
                                        'articles':articles, 
                                        'articles_by_visit':articles_by_visit,
                                        'authenticated':authenticated,
                                        'permission':permission,
                                        'categories':categories,
                                        'categories_by_date':categories_by_date,
                                        })

    


@login_required(login_url='sign_in')
# @TODO 缺省参数deepdelete ???
def delete(request, pk, deepdelete=True):
    author = request.user.userprofile
    # @TODO 永远不能进入
    if deepdelete == 'deepdelete':
        article = get_object_or_404(Post, author=author, pk=pk)
        article.delete()
        return redirect('blog_index', request.user.username)
        
    return redirect('blog_index', request.user.username)
    article = get_object_or_404(Post, author=author, pk=pk, show=True)
    article.show = False
    article.save()
    return redirect('blog_index', request.user.username)
        
@login_required(login_url='sign_in')
def undelete(request, pk):
    author = request.user.userprofile
    article = get_object_or_404(Post, author=author, pk=pk, show=False)
    article.show = True
    article.save()
    return redirect('blog_index', request.user.username)

def post(request, author, pk):
    if User.objects.filter(username=author).exists():
        author = User.objects.get(username=author)
        if UserProfile.objects.filter(user=author).exists():
            author = UserProfile.objects.get(user=author)
            permission = False
            user = None
            authenticated = request.user.is_authenticated() 
            if authenticated :
                user = request.user.userprofile
                if author == user:
                    permission = True

            article = get_object_or_404(Post, author=author, pk=pk) 
            categories = get_list_or_404(Category, author=author)
            articles_by_visit = get_articles_by_visit(authorprofile=author)
            categories_by_date = get_categories_by_date(authorprofile=author)

            # visit
            ip = request.META['REMOTE_ADDR']
            today = date.today()
            if user != author:
                if not Visit.objects.filter(user=author, post=-1, ip=ip, date=today).exists():
                    Visit.objects.create(user=author, ip=ip, date=today)
                    author.visits += 1
                    author.save()

                if not Visit.objects.filter(user=author, post=article.pk, ip=ip, date=today).exists():
                    Visit.objects.create(user=author, post=article.pk, ip=ip, date=today)
                    article.visit += 1
                    article.save()


            return render(request, 'blog/article.html', {'article':article, 
                                                    'categories':categories,
                                                    'categories_by_date':categories_by_date,
                                                    'articles_by_visit':articles_by_visit,
                                                    'author': author,
                                                    'user':user,
                                                    'authenticated':authenticated,
                                                    'permission':permission
                                                    })
        raise Http404
    raise Http404

def category(request, author, pk):
    '''
        按分类名获取分类
    '''
    # 登入用户
    user = None
    permission = None
    author = get_object_or_404(User, username=author)
    authorprofile = get_object_or_404(UserProfile, user=author)
    authenticated = request.user.is_authenticated() 
    if authenticated:
        user = request.user.userprofile
        if user == authorprofile:
            permission = True

    # visit
    ip = request.META['REMOTE_ADDR']
    today = date.today()
    if user != author:
        if not Visit.objects.filter(user=authorprofile, post=-1, ip=ip, date=today).exists():
            Visit.objects.create(user=authorprofile, ip=ip, date=today)
            authorprofile.visits += 1
            authorprofile.save()

    categories = get_list_or_404(Category, author=authorprofile)
    category = get_object_or_404(Category, author=authorprofile, pk=pk)
    articles = category.post_set.all()
    articles_by_visit = get_articles_by_visit(authorprofile=authorprofile)
    categories_by_date = get_categories_by_date(authorprofile=authorprofile)
    return render(request, 'blog/category.html', {'author':authorprofile,
                                                  'user':user, 
                                                  'authenticated':authenticated,
                                                  'permission':permission,
                                                  'articles':articles,
                                                  'articles_by_visit':articles_by_visit,
                                                  'categories':categories,
                                                  'categories_by_date':categories_by_date,})

def category_by_date(request, author, year, month):
    '''
        按月份获取分类
    '''
    # 登入用户
    user = None
    permission = None
    author = get_object_or_404(User, username=author)
    authorprofile = get_object_or_404(UserProfile, user=author)
    authenticated = request.user.is_authenticated() 
    if authenticated:
        user = request.user.userprofile
        if user == authorprofile:
            permission = True

    # visit
    ip = request.META['REMOTE_ADDR']
    today = date.today()
    if user != author:
        if not Visit.objects.filter(user=authorprofile, post=-1, ip=ip, date=today).exists():
            Visit.objects.create(user=authorprofile, ip=ip, date=today)
            authorprofile.visits += 1
            authorprofile.save()

    categories = get_list_or_404(Category, author=authorprofile)
    categories_by_date = get_categories_by_date(authorprofile=authorprofile)
    articles = Post.objects.filter(author=authorprofile, date__year=year, date__month=month).order_by('-date')
    articles_by_visit = get_articles_by_visit(authorprofile=authorprofile)

    return render(request, 'blog/category.html', {'author':authorprofile,
                                                  'user':user, 
                                                  'authenticated':authenticated,
                                                  'permission':permission,
                                                  'articles':articles,
                                                  'articles_by_visit':articles_by_visit,
                                                  'categories':categories,
                                                  'categories_by_date':categories_by_date,})


@login_required(login_url='sign_in')
def collect(request, authorname, pk):
    '''收藏文章'''
    # @TODO 这样做不好，要局部ajax
    # 收藏者
    user = request.user.userprofile
    # 文章作者
    author = get_object_or_404(User, username=authorname)
    author = get_object_or_404(UserProfile, user=author)
    post = get_object_or_404(Post, author=author, pk=pk)
    
    errorcode = -1
    errorinfo = u'已收藏过了'
    if user!= author:
        if not CollectArticle.objects.filter(user=user, authorname=authorname, post=post).exists():
            CollectArticle.objects.create(user=user, authorname=authorname, post=post)
            post.collected += 1
            post.save()
            errorcode = 0
            errorinfo = u'收藏成功'
    
    url = post.get_absolute_url()
    return redirect(url)

@login_required(login_url='sign_in')
def delete_collect(request, authorname, pk):
    '''删除一篇藏的文章'''
    user = request.user.userprofile
    author = get_object_or_404(User, username=authorname)
    author = get_object_or_404(UserProfile, user=author)
    # post = get_object_or_404(Post, author=author, pk=pk)
    
    collection = get_object_or_404(CollectArticle, user=user, pk=pk)
    collection.delete()
    
    return redirect('collections', user.user.username)
    

def collections(request, authorname):
    '''显示收藏的文章'''
    user = None
    authenticated = request.user.is_authenticated()
    if authenticated:
        user = request.user.userprofile

    author = get_object_or_404(User, username=authorname)
    author = get_object_or_404(UserProfile, user=author)

    permission = False
    if user == author:
        permission = True
    
    articles = CollectArticle.objects.filter(user=author)
        
    return render(request, 'blog/collect.html', {'user':user,
                                                 'author':author,
                                                 'articles':articles,
                                                 'authenticated':authenticated,
                                                 'permission':permission
                                                })
