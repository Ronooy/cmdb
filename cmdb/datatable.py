#!/usr/bin/env python
from datatables.core import CreateTable
from cmdb.models import (Asset, IDC, Server, NetworkDevice, Software, Manufacturer,
                         BusinessUnit,Contract)


class AssetTable(CreateTable):
    model = Asset
    list_display = ['id', 'sn', 'asset_type', 'name', 'status', 'manage_ip',
                    'contract', 'admin', 'approved_by', 'memo', 'm_time']
    sort_field = ['sn', 'asset_type', 'name', 'status', 'manage_ip']
    search_fields = ['sn', 'name']  # 查询字段
    message_str = 'name'  # layui alert弹窗时候的提醒字段
    choices_field = ['asset_type', 'status', 'contract']


class IDCTable(CreateTable):
    model = IDC
    list_display = '__all__'
    sort_field = ['name', 'ids', 'address']
    search_fields = ['name', ]  # 查询字段
    message_str = 'name'  # layui alert弹窗时候的提醒字段


class ServerTable(CreateTable):
    model = Server
    list_display = '__all__'
    exclude = ['asset']
    sort_field = ['hosted_on', 'model']
    search_fields = ['model', ]  # 查询字段
    message_str = 'model'  # layui alert弹窗时候的提醒字段
    choices_field = ['sub_asset_type', 'created_by']


class NetworkTable(CreateTable):
    model = NetworkDevice
    list_display = '__all__'
    sort_field = ['vlan_ip', 'model']
    message_str = 'model'  # layui alert弹窗时候的提醒字段
    choices_field = ['sub_asset_type']


class SoftwareTable(CreateTable):
    model = Software
    list_display = '__all__'
    sort_field = ['license_num', 'version']
    message_str = 'version'  # layui alert弹窗时候的提醒字段
    choices_field = ['sub_asset_type']


class ManufacturerTable(CreateTable):
    model = Manufacturer
    list_display = '__all__'
    sort_field = ['name', 'telephone']
    search_fields = ['name']
    message_str = 'name'  # layui alert弹窗时候的提醒字段


class BusinessUnitTable(CreateTable):
    model = BusinessUnit
    list_display = '__all__'
    exclude = ['parent_unit', ]
    search_fields = ['name']
    message_str = 'name'


class ContractTable(CreateTable):
    model = Contract
    list_display = '__all__'
    sort_field = ['sn','name','price','license_num']
    search_fields = ['sn','name']
    message_str = 'name'