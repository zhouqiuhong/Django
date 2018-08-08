# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:forms.py
@time:2018/8/7 000717:12
"""

import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'course_name', 'mobile']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REXGN = "^((1[3,5,8][0-9])|(14[5,7])|(17[0,6,7,8])|(19[7]))\\d{8}$"
        p = re.compile(REXGN)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")