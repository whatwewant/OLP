#coding=utf-8
import re
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from account.models import UserProfile

def index(request):    
    return render(request, 'index.html', {})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('%d' % user.id)
            error = u'用户没有启用'
            return render(request, 'account/login.html', {'error' : error})
        error = u'用户名或密码错误'
        return render(request, 'account/login.html', {'error' : error})
    return render(request, 'account/login.html', {})


def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        nicename = request.POST.get("nicename")

        if not (len(username) >= 3 and len(username) <= 10):
            return render(request, "account/register.html",
                    {"error": u"用户名只能是3-10个字符"})
        name = re.compile("^[_A-Za-z0-9\u4e00-\u9fa5]+$")
        if not name.match(username):
            return render(request, "account/register.html",
                    {"error": u'用户名只能是数字、英文字符、下划线和汉字'})
        if User.objects.filter(username = username).exists():
            return render(request, "account/register.html",
                    {"error": u"用户名已经存在"})
        if not(len(nicename) >= 2 and len(nicename) <= 10):
            return render(request, "account/register.html",
                    {"error": u"昵称只能是2-10个字符"})
        mail = re.compile("[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$")
        if not mail.match(email):
            return render(request, "account/register.html",
                    {"error": u"无效的邮箱格式"})
        if password != re_password:
            return render(request, "account/register.html",
                    {"error": u"两次输入的密码不一致"})
        user = User.objects.create_user(username=username,
                password=password, email=email)
        UserProfile.objects.create(user=user,
                nicename=nicename)
        #return HttpResponseRedirect("/login/")
        return render(request, "account/register_success.html")
    before = request.GET.get("before", "/")
    return render(request, "account/register.html", {"before": before})



