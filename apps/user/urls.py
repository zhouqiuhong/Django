# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:urls.py
@time:2018/8/21 002118:02
"""
from django.conf.urls import url, include
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView
urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    #用户上传头像
    url(r'^image/$', UploadImageView.as_view(), name="user_image"),
    #修改用户密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    #修改邮箱地址
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),


]