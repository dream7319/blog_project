from django.contrib import admin
from blog.models import *

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    # fields = ('title','date_publish','click_count')#输入数据时显示的字段
    # exclude = 不显示哪些列
    # fieldsets = ()#分组显示
    list_display = ('title','date_publish','click_count') #需要显示哪些列
    # list_display_links = () 那些列显示超链接
    # list_editable = () 在列表中哪些可以编辑
    # list_filter = () 那些列作为条件筛选

    class Media:
        js=(
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)