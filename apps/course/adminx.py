# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:adminx.py
@time:2018/8/1 000114:49
"""
import xadmin

from .models import Course, Lesson, Vedio, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'add_time']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VedioAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Vedio, VedioAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)