# -*- coding: utf-8 -*-
# __author__ = "Anatkh"
# date: 2019/1/15
from users import models
import re


class LoginBackend(object):
    # Django1.11版本及以前不用添加request参数
    # def authenticate(self, username=None, password=None):pass

    # Django1.11版本以后必须添加request参数！
    def authenticate(self, request, username=None, password=None):
        if username:
            # email
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", username) != None:
                try:
                    user = models.UserInfo.objects.get(email=username)
                    if user.check_password(password):
                        return user
                except models.UserInfo.DoesNotExist:
                    return None
            # mobile
            elif len(username) == 11 and re.match("^(1[3458]\d{9})$", username) != None:
                try:
                    user = models.UserInfo.objects.get(tel=username)
                    if user.check_password(password):
                        return user
                except models.UserInfo.DoesNotExist:
                    return None
            # nick
            else:
                try:
                    user = models.UserInfo.objects.get(username=username)
                    if user.check_password(password):
                        return user
                except models.UserInfo.DoesNotExist:
                    return None
        else:
            return None

    def get_user(self, user_id):
        """
        该方法是必须有的
        :param user_id:
        :return:
        """
        try:
            return models.UserInfo.objects.get(pk=user_id)
        except models.UserInfo.DoesNotExist:
            return None
