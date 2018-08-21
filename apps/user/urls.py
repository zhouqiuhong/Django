# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:urls.py
@time:2018/8/21 002118:02
"""
from django.conf.urls import url, include
from .views import UserInfoView
urlpatterns = [
    url(r'^info/', UserInfoView.as_view(), name="user_info"),

]