#!/usr/bin/env python
from django import forms
from django.contrib import auth
from accounts.models import UserInfo,RoleList,PermissionList

class LoginUserForm(forms.Form):
    username = forms.CharField(label=u'账 号',
                               error_messages={'required': u'账号不能为空'},
                               widget=forms.TextInput(attrs={"class": "layui-input",
                                                             "lay-verify": "required",
                                                             "placeholder": "邮箱地址",
                                                             "autocomplete":"off",}))
    password = forms.CharField(label=u'密 码',
                               error_messages={'required': u'密码不能为空'},
                               widget=forms.PasswordInput(attrs={"class": "layui-input",
                                                                 "lay-verify": "required",
                                                                 "placeholder": "密码"}))
    url=forms.CharField(widget=forms.HiddenInput,required=False)

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class UserAddForm(forms.ModelForm):
    password2 = forms.CharField(label='重复密码', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request=request
        if not self.request.user.is_superuser:
            self.fields['is_superuser'].widget.attrs={'disabled':'disabled','class': 'form-control'}
        self.fields['username'].label = u'账 号'
        self.fields['username'].error_messages = {'required': u'请输入账号'}
        self.fields['email'].label = u'邮 箱'
        self.fields['email'].error_messages = {'required': u'请输入邮箱', 'invalid': u'请输入有效邮箱'}
        self.fields['nickname'].label = u'姓 名'
        self.fields['nickname'].error_messages = {'required': u'请输入姓名'}
        self.fields['is_active'].label = u'状 态'

    class Meta:
        model = UserInfo
        fields = ('username', 'email', 'password', 'password2', 'nickname', 'is_active','is_superuser')
        widgets = {
            'password': forms.PasswordInput(attrs={"class": "form-control"}),
            'username': forms.TextInput(attrs={"class": "form-control", 'autocomplete': 'off'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={"class": "form-control", 'autocomplete': 'off'}),
            'is_active': forms.Select(choices=((True, u'启用'), (False, u'禁用')),
                                      attrs={'class': 'form-control'}),
            'is_superuser':forms.Select(choices=((True, u'启用'), (False, u'禁用')),
                                         attrs={'class': 'form-control'}),
        }

    def _post_clean(self):
        pwd = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password2')
        if pwd != pwd2:
            self.add_error('password', '两次密码不一致')
        return super()._post_clean()

    def save(self, commit=True):
        instance=super().save()
        if not self.request.user.is_superuser:
            if instance.is_superuser:
                instance.is_superuser=False
                instance.save()
        return instance


class UserEditForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'nickname', 'role', 'is_active', 'is_superuser']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'is_active': forms.Select(choices=((True, u'启用'), (False, u'禁用')),
                                      attrs={'class': 'form-control'}),
            'role':forms.Select(attrs={'class': 'form-control'}),
            'is_superuser': forms.Select(choices=((True, u'启用'), (False, u'禁用')),
                                         attrs={'class': 'form-control'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request=request
        if not self.request.user.is_superuser:
            self.fields['is_superuser'].widget.attrs={'disabled':'disabled','class': 'form-control'}
        self.fields['username'].label = u'账 号'
        self.fields['username'].error_messages = {'required': u'请输入账号'}
        self.fields['email'].label = u'邮 箱'
        self.fields['email'].error_messages = {'required': u'请输入邮箱', 'invalid': u'请输入有效邮箱'}
        self.fields['nickname'].label = u'姓 名'
        self.fields['nickname'].error_messages = {'required': u'请输入姓名'}
        self.fields['is_active'].label = u'状 态'



    def save(self, commit=True):
        instance=super().save()
        if not self.request.user.is_superuser and instance.is_superuser:
            instance.is_superuser=False
            if commit:
                instance.save()
        return instance

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'旧密码', error_messages={'required': '请输入旧密码'},
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    new_password1 = forms.CharField(label=u'新密码', error_messages={'required': '请输入新密码'},
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label=u'新密码', error_messages={'required': '请重复新输入密码'},
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))


    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request=request
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.request.user.check_password(old_password):
            raise forms.ValidationError(u'旧密码错误')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1)<6:
            raise forms.ValidationError(u'密码必须大于6位')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.request.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.request.user.save()
        return self.request.user


class RoleEditForm(forms.ModelForm):
    class Meta:
        model = RoleList
        fields = ['name', 'permissions']
        widgets = {
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].label = '可用 用户权限'


class RoleAddForm(forms.ModelForm):
    class Meta:
        model = RoleList
        fields = ['name', 'permissions']
        widgets = {
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].label = '权限'


class PermissionAddForm(forms.ModelForm):
    class Meta:
        model = PermissionList
        exclude = ('id',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = '权限名称'
        self.fields['url'].label = '链接地址'