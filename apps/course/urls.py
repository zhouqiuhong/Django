# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:urls.py
@time:2018/8/14 00148:50
"""
from django.conf.urls import url
from .views import CourseListView, CourseDetailView


urlpatterns = [
    url(r"^list/$", CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
]