# -*- coding:utf-8 -*-
"""
@author:zhouqiuhong
@file:mixin_utils.py
@time:2018/8/17 001718:09
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(self, request, *args, **kwargs)