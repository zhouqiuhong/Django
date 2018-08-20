# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:urls.py
@time:2018/8/7 000718:13
"""
from django.conf.urls import url, include
from .views import OrgView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, TeacherListView
from .views import TeacherDetailView

urlpatterns = [
    url(r"^org_list/$", OrgView.as_view(), name="org_list"),
    url(r"^add_ask/$", UserAskView.as_view(), name="add_ask"),
    url(r"^home/(?P<org_id>\d+)/$", OrgHomeView.as_view(), name="org_home"),
    url(r"^course/(?P<org_id>\d+)/$", OrgCourseView.as_view(), name="org_course"),
    url(r"^desc/(?P<org_id>\d+)/$", OrgDescView.as_view(), name="org_desc"),
    url(r"^teacher/(?P<org_id>\d+)/$", OrgTeacherView.as_view(), name="org_teacher"),
    #用户收藏
    url(r"^add_fav/$", AddFavView.as_view(), name="add_fav"),
    #讲师列表页
    url(r"^teacher/list/$", TeacherListView.as_view(), name="teacher_list"),
    #讲师详情页面
    url(r"^teacher/detail/(?P<teacher_id>\d+)/$", TeacherDetailView.as_view(), name="teacher_detail"),
]