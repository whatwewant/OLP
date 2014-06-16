# -*- coding:utf-8 -*-
import re
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.models import UserProfile
from datetime import date

def index(request):    
	user = request.user.username
	return render(request, 'index.html', {'user':user})

def sign_in(request):
    # 已经登入，直接跳转到主页
    if request.user.is_authenticated():
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_ip = request.META['REMOTE_ADDR']
        login_date = date.today()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                '''ceshi'''
                return redirect('blog_index', request.user.username)
            error = u'用户没有启用'
            return render(request, 'account/sign_in.html', {'error' : error})
        error = u'用户名或密码错误'
        return render(request, 'account/sign_in.html', {'error' : error})
    return render(request, 'account/sign_in.html', {})


def handle_uploaded_file(file, filename):
    with open(filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


# @TODO
def sign_up(request):
    if request.method == "POST":

        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password")
        re_password = request.POST.get("dopassword")
        nickname = request.POST.get("nickname").strip()

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
        if not(len(nickname) >= 2 and len(nickname) <= 10):
            return render(request, "account/sign_up.html",
                    {"error": u"昵称只能是2-10个字符"})
        # @TODO
        name = re.compile("^[_A-Za-z0-9\u4e00-\u9fa5]+$")
        if not name.match(nickname):
            return render(request, "account/sign_up.html",
                    {"error": u'ni cheng 只能是数字、英文字符、下划线和汉字'})
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
                nickname=nickname)
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


@login_required(login_url='index')
def change_password(request):
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        do_newpassword = request.POST.get('do_newpassword')
        if not newpassword or not do_newpassword or (newpassword != do_newpassword):
            return redirect('index')
        user = request.user.user
        if user.check_password(oldpassword):
            user.set_password(newpassword)
            user.save()
            return redirect('index')
    return redirect('index')
