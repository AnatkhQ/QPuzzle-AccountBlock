# -*- coding: utf-8 -*-
# __author__ = "Anatkh"
# date: 2019/1/15

from django.urls import re_path
from users.views import accounts, verification

app_name = 'users'
urlpatterns = [
    re_path(r'^register/$', accounts.RegisterView.as_view(), name='register'),
    re_path(r'^login/$', accounts.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', accounts.logout, name='logout'),

    re_path(r'^user/(?P<pk>\d+)/center/$', accounts.center, name='center'),
    re_path(r'^user/(?P<pk>\d+)/pwdchange/$', accounts.PassWordChangeView.as_view(), name='pwd_change'),

    # 极验验证
    re_path(r'^pc-geetest/register', accounts.pcgetcaptcha, name='pcgetcaptcha'),
    # 动态校验注册用户名、邮箱是否已经存在
    re_path(r'^verification/(?P<field>username|email)/$', verification.verifaicate)
]
# 在settings DEBUG = False 非开发者模式下， ALLOWED_HOSTS添加指定域名或者IP
handler404=accounts.page_not_found

