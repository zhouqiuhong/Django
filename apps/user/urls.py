# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:urls.py
@time:2018/8/21 002118:02
"""
from django.conf.urls import url, include
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, UserCourseView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView


urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    #用户上传头像
    url(r'^image/$', UploadImageView.as_view(), name="user_image"),
    #修改用户密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    #获取邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    #修改个人邮箱地址
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    #个人课程
    url(r'^my_course/$', UserCourseView.as_view(), name="my_course"),
    #收藏机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),

    #收藏公开课
    url(r'myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),

    #收藏讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),

    #我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),



]