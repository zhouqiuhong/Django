# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:adminx.py
@time:2018/8/1 000115:21
"""
import xadmin

from .models import City, Teacher, CourseOrganization


class CityAdmin(object):
    list_display = ['name', 'desc_city', 'add_time']
    search_fields = ['name', 'desc_city']
    list_filter = ['name', 'desc_city', 'add_time']


class CourseOrganizationAdmin(object):
    list_display = ['name', 'desc_organization', 'fav_num', 'click_num']
    search_fields = ['name', 'desc_organization', 'fav_num', 'click_num']
    list_filter = ['name', 'desc_organization', 'fav_num', 'click_num', 'add_time']
    pass


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company']
    search_fields = ['org', 'name', 'work_year', 'work_company']
    list_filter = ['org', 'name', 'work_year', 'work_company', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrganization, CourseOrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)