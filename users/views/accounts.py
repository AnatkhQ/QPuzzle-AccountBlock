# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, reverse, render_to_response, HttpResponse
from django.contrib import auth
from django.http import JsonResponse
from users import models
from django.views import View
from users.forms import LoginForm, RegistrationForm, UserModelForm, PassWordChangeForm
from geetest import GeetestLib
from django.conf import settings

# 极验验证,请在官网申请ID使用
pc_geetest_id = settings.PC_GEETEST_ID  # id
pc_geetest_key = settings.PC_GEETEST_KEY  # key


def pcgetcaptcha(request):
    """极验验证函数"""
    user_id = 'test'  # 可自行设置
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def page_not_found(request):
    """
    非开发者模式下404
    :param request:
    :return:
    """
    return render_to_response('404.html')


# 请自行在业务中添加主页
# def index(request):
#     return render(request, 'index.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        response = {"user": None, "msg": None}
        form = LoginForm(data=request.POST)
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # 可以使用自带的authenticate进行校验(使用前提AUTH_USER_MODEL)，推荐自行校验，并使用MD5加密进行密码存储
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if status:
                    result = gt.success_validate(challenge, validate, seccode, user_id)
                else:
                    result = gt.failback_validate(challenge, validate, seccode)
                if result:
                    auth.login(request, user)
                    response['user'] = user.username
                else:
                    response['msg'] = {"verification": ["请进行验证码校验", ]}
                    return JsonResponse(response)
            else:
                response['msg'] = {"password": ["密码错误!", ]}
                return JsonResponse(response)

        response["msg"] = form.errors
        return JsonResponse(response)


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        response = {"user": None, "msg": None}
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            # 使用内置User自带create_user方法创建用户，不需要使用save()，且create_user密码自动加密，默认的create密码不加密
            user = models.UserInfo.objects.create_user(username=username, password=password, email=email)

            response['user'] = user.username
        else:
            response["msg"] = form.errors
        return JsonResponse(response)


class PassWordChangeView(View):
    """
    修改密码
    """

    def get(self, request, pk):
        uid = request.user.id
        if uid == int(pk):
            form = PassWordChangeForm()
            return render(request, "users/change_pwd.html", {"form": form})
        else:
            return render(request, '404.html')

    def post(self, request, pk):
        pwd = request.POST.get('password1')
        new_pwd = request.POST.get('password2')
        uid = request.user.id
        if uid == int(pk):
            if request.user.check_password(pwd):  # 判断旧密码是否正确
                request.user.set_password(new_pwd)
                request.user.save()
                result = {"user": request.user.username}
            else:
                result = {"msg": "原密码不正确！！"}

            return JsonResponse(result)
        else:
            return render(request, '404.html')


def logout(request):
    """
    注销用户
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect(reverse("users:login"))


def center(request, pk):
    """
    用户个人中心，建议自定义
    :param request:
    :param pk:
    :return:
    """
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return render(request, '404.html')
    if request.method == 'GET':
        form = UserModelForm(instance=obj)
        return render(request, 'users/personal_center.html', {'form': form})

    form = UserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        userobj = form.save()
        return redirect(reverse('users:center', kwargs={'pk': userobj.pk}))

    return render(request, 'users/personal_center.html', {'form': form})
