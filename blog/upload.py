#!/usr/bin/env python3
# encoding:utf-8
'''
@author: lierl
@file: upload.py
@time: 2018/4/15 14:37
'''
import datetime

import os
import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
__author__ = 'lierl'

@csrf_exempt
def upload_image(request, dir_name):
    #################################
    # kindeditor 图片上传返回数据说明：
    #{'error':1, 'message':'错误信息'}
    #{'error':0, 'url':'图片地址'}
    #################################
    result = {'error': 1, 'message': '上传错误'}
    print(type(request))#django.core.handlers.wsgi.WSGIRequest
    #django.core.files.uploadedfile.InMemoryUploadedFile
    files = request.FILES.get("imgFile", None) #获取文件 ,文件不存在则赋 None
    print(type(files))
    if files:
        result = image_upload(files, dir_name)
    return HttpResponse(json.dumps(result), content_type='application/json')

def upload_generation_dir(dir_name):
    today = datetime.datetime.today()
    dir_name = dir_name+ '/%d/%d/' % (today.year, today.month)
    if not os.path.exists(settings.MEDIA_ROOT + dir_name):
        os.makedirs(settings.MEDIA_ROOT + dir_name)#如果不存在则需要创建
    return dir_name


# 图片上传
def image_upload(files, dir_name):
    #允许上传的文件类型
    allow_suffix = {"jpg", "png", "jpeg", "gif", "bmp"}
    file_suffix = files.name.split(".")[-1]#获取文件后缀
    if file_suffix not in allow_suffix:
        return {'error': 1, 'message': '图片格式不正确'}
    relative_path_file = upload_generation_dir(dir_name);#创建文件目录
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + "." + file_suffix
    path_file = os.path.join(path, file_name)
    file_url = settings.MEDIA_URL + relative_path_file + file_name

    open(path_file, 'wb').write(files.file.read())#保存图片

    return {'error': 0, 'url': file_url}

