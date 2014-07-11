#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from blog.models import Post

from datetime import date
import json, os, datetime, time

import re

@login_required(login_url='sign_in')
def upload_image(request):
    file = request.FILES.get('imgFile')
    print dir(file)
    filename = file.name
    absolute_path = settings.MEDIA_ROOT+'head_portrait/'
    with open(absolute_path+filename, 'wb+') as img:
        for chunk in file.chunks():
            img.write(chunk)
    return redirect('index')

@login_required(login_url='sign_in')
@csrf_exempt
def ke_upload_image(request):
    ext_allowed = ['gif', 'jpg', 'jpeg', 'png']
    max_size = 2621440
    today = datetime.datetime.today()
    save_dir = 'upload/images/%s/%d/%d/%d/' % (request.user.username, 
                                    today.year, today.month, today.day)
    save_path = settings.MEDIA_ROOT+save_dir
    # @TODO
    # save_url = settings.MEDIA_URL+save_dir
    save_url = settings.STATIC_URL+save_dir
    # print save_dir, save_path, save_url

    if request.method == 'POST':
        file = request.FILES['imgFile']

        if not file.name:
            return HttpResponse(json.dumps(
                {'error':1, 'message':u'请选择上传的文件夹'}
                ))

        ext = file.name.split('.').pop()
        if ext not in ext_allowed:
            return HttpResponse(json.dumps(
                {'error':1, 'message':u'请上传后缀为%s的文件' % ext_allowed}
                ))

        if file.size > max_size:
            return HttpResponse(json.dumps(
                {'error':1, 'message':u'上传的文件大小不能超过2.5MB'}
                ))

        if not os.path.isdir(save_path):
            os.makedirs(save_path)

        new_file = '%s.%s' % (int(time.time()), ext)

        with open(save_path+new_file, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return HttpResponse(json.dumps(
            {'error':0, 'url':save_url+new_file}
            ))

@login_required(login_url='sign_in')
@csrf_exempt
def ke_upload_audio(request):
    ext_allowed = ['mp3', 'wav', 'wma', 'ogg', 'aac', 'ape']
    # max_size = 10485760 # 10 MB
    max_size = 1048576000 # 1000 MB
    today = datetime.datetime.today()
    save_dir = 'upload/audios/%s/%d/%d/%d/' % (request.user.username,
                                    today.year, today.month, today.day)
    save_path = settings.MEDIA_ROOT+save_dir
    # @TODO
    # save_url = settings.MEDIA_URL+save_dir
    save_url = settings.STATIC_URL+save_dir
    # print save_dir, save_path, save_url

    if request.method == 'POST':
        file = request.FILES['imgFile']

        if not file.name:
            return HttpResponse(json.dumps(
                {'error':1, 'message':u'请选择上传的文件夹'}
                ))

        ext = file.name.split('.').pop()
        if ext not in ext_allowed:
            return HttpResponse(json.dumps(
                {'error':1, 'message':u'请上传后缀为%s的文件' % ext_allowed}
                ))

        if file.size > max_size:
            return HttpResponse(json.dumps(
                {'error':1, 'message':u'上传的文件大小不能超过2.5MB'}
                ))

        if not os.path.isdir(save_path):
            os.makedirs(save_path)

        new_file = '%s.%s' % (int(time.time()), ext)

        with open(save_path+new_file, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return HttpResponse(json.dumps(
            {'error':0, 'url':save_url+new_file}
            ))

@login_required(login_url='sign_in')
def send_one_mail(request):
    '''单邮件'''
    if request.method == 'POST':
        subject = request.get('subject')
        messages = request.get('messages')
        from_user = request.get('from_user')
        to_user = request.get('to_user')
        result = send_mail(subject, messages, from_user, [to_user], fail_silently=False)
        if not result:
            return_message = {'error':1, 'message':'发送失败'}
        else:
            return_message = {'error':0, 'message':'发送成功'}
        return HttpResponse(json.dumps(return_message))
    return render(request, '', {})

def html_tags_filter(html):
    '''
        过滤html标签
        Example : <li>as<span>pq</span></li>
        return : aspq
    '''
    str = re.sub(r'</?\w+[^>]*>', '', html).replace(' ', '').replace('\n', '')

    return str

def get_categories_by_date(authorprofile=None):
    '''
        按日期获得文章, 10个
    '''
    if not authorprofile:
        return None

    month_register = authorprofile.register_date.month
    year_register = authorprofile.register_date.year

    month_now = date.today().month
    year_now = date.today().year

    categories = list()
    articles_all = Post.objects.filter(author=authorprofile)
    while year_register <= year_now and month_register <= month_now:
        articles = articles_all.filter(date__year=year_now, 
                                date__month=month_now)
        if articles.count() != 0:
            count = articles.count()
            url = r'/%s/category_by_date/%s/%s/' % (authorprofile.user.username, year_now, month_now)
            year_and_month = str(year_now)+'-'+str(month_now)
            
            t = {'date':year_and_month, 'count':count, 'url':url}
            categories.append(t)

        month_now -= 1
        if month_register < 1:
            month_now = 12
            year_now -= 1

    return categories

def get_articles_by_visit(authorprofile=None):
    '''
        按阅读排行文章，5篇
    '''
    if not authorprofile:
        return None

    # author = get_object_or_404(User, username=authorname)
    # authorprofile = get_object_or_404(UserProfile, user=author)
    articles = Post.objects.filter(author=authorprofile).order_by('-visit')[:5]

    return articles
