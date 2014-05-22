#coding=utf-8
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render

def index(request):
    return HttpResponse("Welcome to index page")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None :
            if user.is_active:
                login(request, user)
                return HttpResponse('%d' % user.id) 

            error = u'用户没有启用'
            return render(request, 'account/login.html', {'error' : error})
        
        error = u'用户名或密码错误'
        return render(request, 'account/login.html', {'error' : error})
    
    return render(request, 'account/login.html', {})


