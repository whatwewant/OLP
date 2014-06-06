# -*- coding:utf-8 -*-

from blog.models import Post, Category, PostToCategory
from account.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from datetime import date

def homePage(request):
    authenticated = request.user.is_authenticated()
    userprofile = None
    if authenticated:
        userprofile = request.user.userprofile
    return render(request, 'index.html', {'authenticated':authenticated,
                                        'user':userprofile})

def personPage(request, author=False):
    '''
        Person Blog Home Page
    '''
    if User.objects.filter(username=author).exists():
        author_user = User.objects.get(username=author)
        if UserProfile.objects.filter(user=author_user).exists():
            userprofile = UserProfile.objects.get(user=author_user)
            articles = Post.objects.filter(author=userprofile, show=True)
            authenticated = request.user.is_authenticated()
            categories = None
            if Category.objects.filter(author=userprofile).exists():
                categories = Category.objects.filter(author=userprofile)
            # categories = Category.objects.all()
            return render(request, 'blog/index.html', {'user':userprofile, 
                                                       'articles':articles, 
                                                       'authenticated':authenticated,
                                                       'categories':categories})
        raise Http404
    raise Http404

@login_required(login_url='sign_in')
def write(request):
    if request.method == "POST" :
        author = request.user.userprofile
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
            return redirect('blog_index')

        if not excerpt:
            excerpt = content[:300]

        for i in categorylist:
            cp, ccreated = Category.objects.get_or_create(author=author, name=i)
            pp, pcreated = Post.objects.get_or_create(author=author, title=title,
                            content=content, excerpt=excerpt,
                            modified_date=modified_date,
                            modified_date_gmt=modified_date_gmt)
            PostToCategory.objects.get_or_create(post=pp, category=cp)

        return redirect('blog_index', request.user.username)
    return render(request, 'blog/write.html', {'authenticated':True})
	
@login_required(login_url='sign_in')
def edit(request, pk):
    '''
	edit view
    '''
    if request.method == "POST":
        author = request.user.userprofile
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
            excerpt = content[:300]

        for i in categorylist:
            cp, ccreated = Category.objects.get_or_create(author=author, name=i)

            article = Post.objects.get(author=author, pk=pk, show=True)
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

    author = request.user.userprofile
    article = get_object_or_404(Post, author=author, pk=pk, show=True)
    print article
    return render(request, 'blog/edit.html', {'article':article, 
                                              'authenticated':True})

@login_required(login_url='sign_in')
# @TODO 缺省参数deepdelete ???
def delete(request, pk, deepdelete=True):
    author = request.user.userprofile
    # @TODO 永远不能进入
    if deepdelete:
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
    article = get_object_or_404(Post, author=author, pk=pk)
    article.show = True
    article.save()
    return redirect('blog_index', request.user.username)

def post(request, author, pk):
    if User.objects.filter(username=author).exists():
        user = User.objects.get(username=author)
        if UserProfile.objects.filter(user=user).exists():
            author = UserProfile.objects.get(user=user)
            article = get_object_or_404(Post, author=author, pk=pk) 
            return render(request, 'blog/article.html', {'article':article, 
                'post':True, 
                'authenticated':request.user.is_authenticated()})
        raise Http404
    raise Http404

