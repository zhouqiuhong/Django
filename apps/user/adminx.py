# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:adminx.py
@time:2018/8/2 00029:05
"""
import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"#菜单
 # @xadmin.register(EmailVerifyRecord)


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'index', 'add_time', 'url']
    search_fields = ['title', 'image', 'index', 'url']
    list_filter = ['title', 'image', 'index', 'add_time', 'url']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)#设置主题
xadmin.site.register(views.CommAdminView, GlobalSettings)#设置网站名