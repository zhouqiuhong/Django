# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:urls.py
@time:2018/8/7 000718:13
"""
from django.conf.urls import url, include
from .views import OrgView, UserAskView, OrgHomeView


urlpatterns = [
    url(r"^org_list/$", OrgView.as_view(), name="org_list"),
    url(r"^add_ask/$", UserAskView.as_view(), name="add_ask"),
    url(r"^home/(?P<org_id>\d+)/$", OrgHomeView.as_view(), name="org_home"),
]