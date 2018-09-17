#!/usr/bin/env python
from accounts.models import UserInfo
from django.contrib.auth.backends import ModelBackend

class CheckEmailBackend(ModelBackend):
    """自定义验证后端，用来验证邮箱和密码"""

    def authenticate(self, request, **credentials):
        username = credentials.get('username')
        try:
            user = UserInfo.objects.get(email=username)
        except UserInfo.DoesNotExist:
            pass
        else:
            if user.check_password(credentials.get('password')):
                return user

class CheckUserNameBackend(ModelBackend):
    """自定义验证后端，用来验证用户名和密码"""

    def authenticate(self, request, **credentials):
        username = credentials.get('username')
        try:
            user = UserInfo.objects.get(username=username)
        except UserInfo.DoesNotExist:
            pass
        else:
            if user.check_password(credentials.get('password')):
                return user