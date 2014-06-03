# -*- coding:utf-8 -*-

from blog.models import Post, Comment
from account.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from datetime import date

def homePage(request):
    return render(request, 'index.html', {})

def personPage(request, author=False):
    '''
        Person Blog Home Page
    '''
    if User.objects.filter(username=author).exists():
        author_user = User.objects.get(username=author)
        if UserProfile.objects.filter(user=author_user).exists():
            author_profile = UserProfile.objects.get(user=author_user)
            arrays = Post.objects.filter(author=author_profile)
            return render(request, 'blog/index.html', {'user': author_profile.nicename,
                'arrays':arrays})
        raise Http404
    raise Http404

@login_required(login_url='sign_in')
def write(request):
    if request.method == "POST" :
        author = request.user.userprofile
        title = request.POST.get('title')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt')
        # password= request.POST.get('password')
        modified_date = date.today()
        modified_date_gmt = timezone.now()
        # content_type = request.POST.get('content_type')
        if not title or not content or not excerpt:
            return redirect('blog_index')
        Post.objects.create(author=author, title=title,
                            content=content, excerpt=excerpt,
                            modified_date=modified_date,
                            modified_date_gmt=modified_date_gmt)

        return redirect('/blog/'+request.user.username+'/')
    return render(request, 'blog/write.html', {})
	
@login_required()
def edit(request, id):
    '''
	edit view
    '''
    if request.method == "POST":
        author = request.user.userprofile
        title = request.POST.get('title')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt')
        # password= request.POST.get('password')
        modified_date = date.today()
        modified_date_gmt = timezone.now()
        # content_type = request.POST.get('content_type')
        if not title or not content or not excerpt:
            return redirect('blog_index')
        
        array = Post.objects.get(author=author, id=id)
        print dir(array)

        array.title = title
        array.content = content
        array.excerpt = excerpt
        array.modified_date = modified_date
        array.modified_date_gmt = modified_date_gmt
        array.save()

        return redirect('/blog/'+request.user.username+'/')

    author = request.user.userprofile
    array = get_object_or_404(Post, author=author, id=id)
    return render(request, 'blog/edit.html', {'array':array})
