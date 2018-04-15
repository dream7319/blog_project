import json

from django.shortcuts import render
import logging
from blog.models import *
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
# Create your views here.

logger = logging.getLogger('blog.views')

def global_setting(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESC
    }

def index(request):
    try:
        #获取所有的分类
        category_list = Category.objects.all()
        #获取所有的文章
        article_list = Article.objects.all()
        #获取广告列表
        ad_list = Ad.objects.all()
        #设置slider data
        slider_data = []
        for ad in ad_list:
            data = {}
            data['id'] = ad.id
            data['client'] = ad.title
            data['desc'] = ad.description
            slider_data.append(data)
        #标签云
        tag_list = Tag.objects.all()
        #友情链接
        links_list = Links.objects.all()

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