#!/usr/bin/env python
from datatables.core import CreateTable
from navigation.models import NavStore


class NavTable(CreateTable):
    model = NavStore
    list_display = '__all__'
    ordering = 'id'
    sort_field = ['name','url','c_date']
    search_fields = ['name']  # 查询字段
    message_str = 'name'  # layui alert弹窗时候的提醒字段
    choices_field = []  # 前端显示 choices 或者外键的下拉框
    choices_field_blank = {}  # 下拉框空白提示{'字段':'资产类型'}
    limit = 'limit'
    page = 'page'
    query = 'q'
