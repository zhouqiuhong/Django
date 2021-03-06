"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from django.views.generic import TemplateView

from django.views.static import serve

import xadmin
from user.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from user.views import LogoutView, IndexView, page_not_found

from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url('^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    #退出登录
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r"^active/(?P<active_code>.*/$)", ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r"^reset/(?P<active_code>.*/$)", ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    #课程机构首页
    url(r"^org/", include("organization.urls", namespace="org")),
    #课程
    url(r'^course/', include("course.urls", namespace="course")),
    #配置上传文件的处理函数
    url(r"^media/(?P<path>.*/$)", serve, {"document_root": MEDIA_ROOT}),
    #生产环境下静态文件的处理
    #url(r"^static/(?P<path>.*/$)", serve, {"document_root": STATIC_ROOT}),
    #用户个人信息相关配置
    url(r'^users/', include("user.urls", namespace="user")),
    #
    #url(r'^ueditor/', include('DjangoUeditor.urls' )),
]
#全局404页面配置
hander404 = "user.views.page_not_found"
#全局500页面配置
hander500 = "user.views.page_error"