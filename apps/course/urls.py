# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:urls.py
@time:2018/8/14 00148:50
"""
from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommntView, AddCommentView


urlpatterns = [
    url(r"^list/$", CourseListView.as_view(), name="course_list"),
    #课程详情页面
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    #课程页面
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    #课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommntView.as_view(), name="course_comment"),
    #添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
]