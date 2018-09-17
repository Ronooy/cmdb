#!/usr/bin/env python
from datatables.core import CreateTable
from accounts.models import UserInfo,RoleList,PermissionList

class UserTable(CreateTable):
    model = UserInfo
    list_display = ['id','nickname','username','email','role','is_active','is_superuser','last_login']
    ordering = 'id'
    sort_field = ['username','email']
    search_fields = ['username','email']  # 查询字段
    message_str = 'username'  # layui alert弹窗时候的提醒字段



class RoleTable(CreateTable):
    model = RoleList
    list_display = ['id', 'name']
    ordering = 'id'
    sort_field = ['name']
    search_fields = ['name',]  # 查询字段
    message_str = 'name'  # layui alert弹窗时候的提醒字段


class PermissionTable(CreateTable):
    model = PermissionList
    list_display = ['id', 'name','url']
    ordering = 'id'
    sort_field = ['name']
    search_fields = ['name',]  # 查询字段
    message_str = 'name'  # layui alert弹窗时候的提醒字段
