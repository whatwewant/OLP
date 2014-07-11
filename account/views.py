# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

import re
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.models import UserProfile, UserInfo, UserLoginHistory
import time

# from utils import transform_ip_to_address

def index(request):    
	user = request.user.username
	return render(request, 'index.html', {'user':user})

def sign_in(request):
    '''登录'''
    # 已经登入，直接跳转到主页
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_ip = request.META['REMOTE_ADDR']
        login_date = time.ctime
        # login_address = transform_ip_to_address(login_ip)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                UserLoginHistory.objects.create(
                    user=user,
                    login_ip=login_ip,
                    # login_address=login_address,
                    date=login_date
                    )

                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('blog_author', request.user.username)
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
    '''注册'''
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
        if not name.match(unicode(username)):
            return render(request, "account/sign_up.html",
                    {"error": u'用户名只能是数字、英文字符、下划线和汉字'})
        if User.objects.filter(username = username).exists():
            return render(request, "account/sign_up.html",
                    {"error": u"用户名已经存在"})
        if not(len(nickname) >= 2 and len(nickname) <= 10):
            return render(request, "account/sign_up.html",
                    {"error": u"昵称只能是2-10个字符"})
        # @TODO
        name = re.compile(ur'^[_A-Za-z0-9\u4e00-\u9fa5]+$')
        if not name.match(unicode(nickname)):
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
        # auto sign in 
        user = authenticate(username=username, password=password)
        login(request, user)

        # login history
        login_ip = request.META['REMOTE_ADDR']
        login_date = time.ctime
        # login_address = transform_ip_to_address(login_ip)
        UserLoginHistory.objects.create(
                    user=user,
                    login_ip=login_ip,
                    # login_address=login_address,
                    date=login_date
                    )

        return redirect('blog_author', request.user.username)
        #return redirect('sign_in')
    before = request.GET.get("before", "/")
    return render(request, "account/sign_up.html", {"before": before})


@login_required(login_url='sign_in')
def sign_out(request):
    '''logout'''
    logout(request)
    return redirect('index')


@login_required(login_url='sign_up')
def change_password(request):
    '''修改密码'''
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        do_newpassword = request.POST.get('do_newpassword')
        if not newpassword or not do_newpassword or (newpassword != do_newpassword):
            return redirect('index')
        user = request.user.userprofile.user
        if user.check_password(oldpassword):
            user.set_password(newpassword)
            return redirect('index')
        return redirect('index')
    return redirect('index')

@login_required(login_url='sign_in')
def user_info(request, username=None):
    '''获取/修改个人信息'''
    # if not request.user.is_authenticated():
    #    return redirect('sign_up')

    userprofile = request.user.userprofile
    userinfo, userinfo_created = UserInfo.objects.get_or_create(userprofile=userprofile)
    # userinfo = UserInfo.objects.get(userprofile=userprofile)
    if request.method == 'POST':
        # @TODO
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        hometown = request.POST.get('hometown')
        zip_code = request.POST.get('zip_code')
        qq = request.POST.get('qq')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        country_code = request.POST.get('country_code')
        language = request.POST.get('language')
        recovery_email = request.POST.get('recovery_email')
        web_site = request.POST.get('web_site')

        userinfo.name = name
        userinfo.sex = sex
        userinfo.age = int(age)
        userinfo.hometown = hometown
        userinfo.zip_code = int(zip_code)
        userinfo.qq = int(qq)
        userinfo.phone = int(phone)
        userinfo.country = country
        userinfo.country_code = country_code
        userinfo.language = language
        userinfo.recovery_email = recovery_email
        userinfo.web_site = web_site
        userinfo.save()
        
        # userinfo.sex = sex
        # userinfo.age = age
        # userinfo.hometown = hometown
        # userinfo.zip_code = zip_code
        # userinfo.qq = qq
        # userinfo.phone = phone
        # userinfo.country = country
        # userinfo.country_code = country_code
        # userinfo.language = language
        # userinfo.recovery_mail = recovery_mail
        # userinfo.web_site = web_site
        #
        # temp_info = {'sex': sex,
        #             'age': age,
        #             'hometown': hometown,
        #             'zip_code': zip_code,
        #             'qq': qq,
        #             'phone': phone,
        #             'country': country,
        #             'country_code': country_code,
        #             'language': language,
        #             'recovery_mail': recovery_mail,
        #             'web_site': web_site
        #            }
        #
        #userinfo_dict = userinfo.__dict__
        #for key, value in temp_info.items():
        #    if userinfo_dict[key] != value:
        #        userinfo_dict[key] = value
        #     
        #userinfo.save()
        return render(request, 'user/user_info.html', {'userinfo':userinfo, 
                                                       'user':userprofile,
                                                       'author':userprofile,
                                                       'authenticated':True,
                                                       'permission':True})
    return render(request, 'user/user_info.html', {'userinfo':userinfo,
                                                   'user':userprofile,
                                                   'author':userprofile,
                                                   'authenticated':True,
                                                   'permission':True})

@login_required(login_url='sign_in')
def get_user_login_history(request, username=None):
    '''登入历史'''
    author = request.user.userprofile
    user = author.user
    histories = UserLoginHistory.objects.filter(user=user)[:10]
    return render(request, 'user/user_login_history.html', {'histories': histories,
                                                            'user':author,
                                                            'author':author,
                                                            'authenticated':True,
                                                            'permission':True})

