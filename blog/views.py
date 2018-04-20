#!/usr/bin/env python3
# encoding:utf-8
'''
@author: lierl
@file: do_io.py
@time: 2018/3/25 11:00
'''
__author__ = 'lierl'

from django.shortcuts import render
import logging
from blog.models import *
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Count
# Create your views here.

logger = logging.getLogger('blog.views')

def global_setting(request):
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC

    # 获取所有的分类
    category_list = Category.objects.all()
    # 获取广告列表
    ad_list = Ad.objects.all()
    # 设置slider data 广告图片
    slider_data = []
    for ad in ad_list:
        data = {}
        data['id'] = ad.id
        data['client'] = ad.title
        data['desc'] = ad.description
        slider_data.append(data)
    # 标签云
    tag_list = Tag.objects.all()
    # 友情链接
    links_list = Links.objects.all()

    # 浏览排行
    browse_list = Article.objects.all().order_by("-click_count")[:6]
    # 站长推荐
    station_master_list = Article.objects.filter(is_recommend=1).order_by("-click_count")[:6]
    # 评论排行
    '''
    注释：
    1、Comment.objects.values('article') 获取拥有评论的文章，即返回的是所有的article_id的json数据
    2、annotate(article_count = Count('article')) 聚合函数，返回每个article_id的个数
    '''
    comment_rank_list = Comment.objects.values('article').annotate(article_count=Count('article')).order_by(
        "-article_count")
    # [data for data in comment_rank_list]
    # 返回：[{'article_count': 2, 'article': 2}, {'article_count': 1, 'article': 6}]
    article_comment_rank_list = [Article.objects.get(pk=data['article']) for data in comment_rank_list]

    archive_list = Article.objects.distinct_date_public()

    return locals()

def index(request):
    try:
        #获取所有的文章
        article_list = Article.objects.all()
        #所有文章分页查询
        article_list = getPage(request, article_list)

    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())

def getPage(request, article_list):
    paginator = Paginator(object_list=article_list, per_page= 2)#每页两条数据
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger) as e:
        logger.error(e)
        article_list = paginator.page(1)
    return article_list

#文章详情
def article_detail(request):
    article_id = request.GET.get('id', None)
    try:
        article = Article.objects.get(pk=article_id)
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Article.DoesNotExist as e:
        logger.error(e)
        return render(request, 'failure.html', {'reason': '没有找到对应的文章'})
    return render(request,'article_detail.html', locals())