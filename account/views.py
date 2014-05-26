# -*- coding:utf-8 -*-
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.models import UserProfile

def index(request):    
	user = request.user.username
	return render(request, 'index.html', {'user':user})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                '''ceshi'''
                return redirect('blog_index')
            error = u'用户没有启用'
            return render(request, 'account/sign_in.html', {'error' : error})
        error = u'用户名或密码错误'
        return render(request, 'account/sign_in.html', {'error' : error})
    return render(request, 'account/sign_in.html', {})


def sign_up(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("dopassword")
        nicename = request.POST.get("nickname")

        if not (len(username) >= 3 and len(username) <= 10):
            return render(request, "account/sign_up.html",
                    {"error": u"用户名只能是3-10个字符"})
        name = re.compile(ur'[a-zA-Z0-9_]|[\u4e00-\u9fa5]+$')
        if not name.match(username):
            return render(request, "account/sign_up.html",
                    {"error": u'用户名只能是数字、英文字符、下划线和汉字'})
        if User.objects.filter(username = username).exists():
            return render(request, "account/sign_up.html",
                    {"error": u"用户名已经存在"})
        if not(len(nicename) >= 2 and len(nicename) <= 10):
            return render(request, "account/sign_up.html",
                    {"error": u"昵称只能是2-10个字符"})
        mail = re.compile("[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$")
        if not mail.match(email):
            return render(request, "account/sign_up.html",
                    {"error": u"无效的邮箱格式"})
        if password != re_password:
            return render(request, "account/sign_up.html",
                    {"error": u"两次输入的密码不一致"})
        user = User.objects.create_user(username=username,
                password=password, email=email)
        UserProfile.objects.create(user=user,
                nicename=nicename)
        #return HttpResponseRedirect("/sign_in/")
        return redirect('sign_in')
    before = request.GET.get("before", "/")
    return render(request, "account/sign_up.html", {"before": before})


@login_required(login_url='sign_in')
def sign_out(request):
	'''
		logout
	'''
	logout(request)
	return redirect('index')
