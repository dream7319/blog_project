#!/usr/bin/env python3
# encoding:utf-8
'''
@author: lierl
@file: urls.py
@time: 2018/4/15 9:20
'''
__author__ = 'lierl'

from django.conf.urls import url
from blog import views

# app_name='blog'

urlpatterns = [
    url('^index/$', view=views.index, name="index"),
]