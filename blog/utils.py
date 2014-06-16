#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

import json, os, datetime, time
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
    save_dir = 'upload/images/%d/%d/%d/' % (today.year, today.month, today.day)
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
    save_dir = 'upload/audios/%d/%d/%d/' % (today.year, today.month, today.day)
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
