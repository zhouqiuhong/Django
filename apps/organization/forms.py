# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:forms.py
@time:2018/8/7 000717:12
"""
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'course_name', 'mobile']