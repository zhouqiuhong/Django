# -*- coding:utf-8 -*-
import json

from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password

from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, ModifyUserPwdForm
from django.db.models import Q

from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username), Q(password=password))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': u"用户已存在"})

            pass_word = request.POST.get('password', "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get('password', "")
            user = authenticate(username=user_name, password=pass_word)
            # print(user)
            if user is not None:
                if user.is_active:
                    login(request=request, user=user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': u"用户未激活"})
            else:
                return render(request, 'login.html', {'msg': u"用户名或密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, active_code):
        active_code = active_code.replace("/", "")
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})

        else:
            return render(request, 'password_reset.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")

            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, "msg": u"密码不一致"})
            else:
                email = request.POST.get("email", "")
                return render(request, "login.html", {"email": email, "modify_form": modify_form})
        else:
            return render(request, 'password_reset.html')


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = UserProfile.objects.all()
        return render(request, "usercenter-info.html", {
        })


class UploadImageView(LoginRequiredMixin, View):
    #修改用户头像
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)#文件类型
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """在个人用户中心修改密码"""
    def post(self, request):
        modify_form = ModifyUserPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# class UpdateEmailView(View):
#     def post(self, request):
#         pass


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get("email", "")
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮件已存在"}', content_type="application/json")
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type="application/json")