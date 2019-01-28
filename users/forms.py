# -*- coding: utf-8 -*-
# __author__ = "Anatkh"
# date: 2019/1/15
import re
from django import forms
from .models import UserInfo
from django.forms import widgets


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


def phone_check(phone):
    pattern = re.compile(r"^(1[3458]\d{9})$")
    return re.match(pattern, phone)


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RegistrationForm(BootstrapForm):
    username = forms.CharField(label='用户名', max_length=50, error_messages={"required": "用户名不能为空！"},
                               widget=widgets.TextInput(attrs={'placeholder': '请输入用户名/邮箱/电话'}))
    email = forms.EmailField(label='邮箱', error_messages={"required": "邮箱不能为空！"},
                             widget=widgets.TextInput(attrs={'placeholder': '请输入邮箱'}))
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}),
                                error_messages={"required": "密码不能为空！"})
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'placeholder': '请确认密码'}),
                                error_messages={"required": "重新确认密码！"})

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 6:
            raise forms.ValidationError("用户名必须大于等于6位")
        elif len(username) > 18:
            raise forms.ValidationError("用户名需小于18位")
        else:
            filter_result = UserInfo.objects.filter(username__exact=username)  # exact精准匹配
            if len(filter_result) > 0:
                raise forms.ValidationError("用户名已存在")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = UserInfo.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("邮箱已存在")
        else:
            raise forms.ValidationError("请输入有效邮箱")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码必须大于等于6位")
        elif len(password1) > 20:
            raise forms.ValidationError("密码过长")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码不一致，请重新输入")

        return password2


class LoginForm(BootstrapForm):
    username = forms.CharField(label='用户名', max_length=50, error_messages={"required": "用户名不能为空！"},
                               widget=widgets.TextInput(attrs={'placeholder': '请输入用户名/邮箱/电话'}))
    password = forms.CharField(label='密码', widget=widgets.PasswordInput(attrs={'placeholder': '请输入密码'}),
                               error_messages={"required": "密码不能为空！"})

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = UserInfo.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("此邮箱不存在")
            return username

        if phone_check(username):
            filter_result = UserInfo.objects.filter(tel__exact=username)
            if not filter_result:
                raise forms.ValidationError("此号码不存在")
        else:
            filter_result = UserInfo.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("此账号不存在")

        return username


class PassWordChangeForm(BootstrapForm):
    password1 = forms.CharField(label='旧密码', widget=forms.PasswordInput(attrs={'placeholder': '请输入旧密码'}),
                                error_messages={"required": "密码不能为空！"})
    password2 = forms.CharField(label='新密码', widget=forms.PasswordInput(attrs={'placeholder': '请输入新密码'}),
                                error_messages={"required": "重新确认密码！"})
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'placeholder': '请确认新密码'}),
                                       error_messages={"required": "重新确认密码！"})

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password2')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码不一致，请重新输入")

        return password2


class UserModelForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'nickname', 'email', 'tel', 'gender', ]
