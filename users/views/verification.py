# -*- coding: utf-8 -*-
# __author__ = "Anatkh"
# date: 2019/1/17
from django.shortcuts import render
from django.http import JsonResponse
from users import models
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def verifaicate(request, field):
    """
    注册页面前端ajax动态验证
    :param request:
    :param field:
    :return:
    """
    if request.method == "POST":
        response = {"valid": True}
        if field == "username":
            username = request.POST.get("username")
            filter_result = models.UserInfo.objects.filter(username__exact=username)  # exact精准匹配
            if len(filter_result) > 0:
                response["valid"] = False

        elif field == "email":
            username = request.POST.get("email")
            filter_result = models.UserInfo.objects.filter(email__exact=username)  # exact精准匹配
            if len(filter_result) > 0:
                response["valid"] = False
        return JsonResponse(response)
    # 建议自定义404页面进行redirect
    return render(request, "404.html")
