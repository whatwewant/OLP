# -*- coding:utf-8 -*-
from blog.models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from time import asctime, gmtime

def index(request):
	'''
		Person Blog Home Page
	'''
	user = "anonymous"
	return render(request, 'blog/index.html', {'user': user})

# @login_required(login_url='sign_in')
def write(request):
	if request.method == "POST":
		author	= request.user.userprofile
		title	= request.POST.get('title')
		content	= request.POST.get('content')
		excerpt = request.POST.get('excerpt')
		password= request.POST.get('password')
		modified_date = asctime()
		modified_date_gmt = gmtime()
		content_type = request.POST.get('content_type')

		

	return render(request, 'blog/write.html', {})
	
