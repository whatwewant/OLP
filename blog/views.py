# -*- coding:utf-8 -*-

from blog.models import Post, Category, PostToCategory
from account.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_list_or_404
from django.http import Http404
from django.utils import timezone
from datetime import date

from utils import ke_upload_image, ke_upload_audio, send_one_mail

def homePage(request):
    # print dir(request)
    authenticated = request.user.is_authenticated()
    userprofile = None
    articles = Post.objects.filter(show=True)[:9]
    if authenticated:
        userprofile = request.user.userprofile
    return render(request, 'index.html', {'authenticated':authenticated,
                                          'user':userprofile, 'articles':articles})

def personPage(request, author=False):
    '''
        Person Blog Home Page
    '''
    for k, v in request.META.items():
        print k,':',v
    # print author
    # print dir(request.user)
    # print request.user.is_authenticated()
    # user
    userprofile = None
    authenticated = False
    if request.user.is_authenticated():
        userprofile = request.user.userprofile
        authenticated = True #request.user.is_authenticated()
    # articles author
    author = get_object_or_404(User, username=author)
    authorprofile = UserProfile.objects.get(user=author)
    articles = Post.objects.filter(author=authorprofile, show=True)
    categories = Category.objects.filter(author=authorprofile)
    return render(request, 'blog/index.html', {'author':authorprofile, 
                                        'user': userprofile,
                                        'articles':articles, 
                                        'authenticated':authenticated,
                                        'categories':categories})

@login_required(login_url='sign_in')
def write(request):
    author = request.user.userprofile
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
            excerpt = content[:300]

        for i in categorylist:
            cp, ccreated = Category.objects.get_or_create(author=author, name=i)
            pp, pcreated = Post.objects.get_or_create(author=author, 
                            title=title, name = name,
                            content=content, excerpt=excerpt,
                            modified_date=modified_date,
                            modified_date_gmt=modified_date_gmt)
            PostToCategory.objects.get_or_create(post=pp, category=cp)

        return redirect('blog_index', request.user.username)
    return render(request, 'blog/write.html', {'author':author,
                                               'authenticated':True})
	
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

        if categorylist:
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
    return render(request, 'blog/edit.html', {'author':author,
                                              'article':article, 
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
        author = User.objects.get(username=author)
        if UserProfile.objects.filter(user=author).exists():
            author = UserProfile.objects.get(user=author)
            article = get_object_or_404(Post, author=author, pk=pk) 
            categories = get_list_or_404(Category, author=author)
            return render(request, 'blog/article.html', {'article':article, 
                'post':True, 
                'categories':categories,
                'author': author,
                'authenticated':request.user.is_authenticated()})
        raise Http404
    raise Http404

def category(request, author, pk):
    # 登入用户
    user = None
    if request.user.is_authenticated():
        user = request.user.userprofile
    author = get_object_or_404(User, username=author)
    authorprofile = get_object_or_404(UserProfile, user=author)
    categories = get_list_or_404(Category, author=authorprofile)
    category = get_object_or_404(Category, author=authorprofile, pk=pk)
    articles = category.post_set.all()
    return render(request, 'blog/category.html', {'author':authorprofile,
                                                  'user':user, 
                                                  'articles':articles,
                                                  'categories':categories})
