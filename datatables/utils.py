#!/usr/bin/env python

def inittable(modelclass):
    """
    初始化表格页面所需要的数据：按钮和表头
    :param modelclass: 继承serializers的model
    :return: cols 表头
            table_id 表格id
            message_str 表格消息弹窗提示字段
            script_bool 最右边的表格工具
            choices choices模式或者外键字段生成的下拉框数据
            choices_name 字段的name
    """
    placeholder = ""
    if modelclass.search_fields:
        placeholder = '搜索关键字：' + '||'.join(
            [str(modelclass.model._meta.get_field(field).verbose_name) for field in modelclass.search_fields])

    message_str = modelclass.message_str
    cols, script_bool,choices_list = modelclass.get_tableHeader()
    table_id = '-'.join([modelclass.model._meta.label.split('.')[1].lower(),'tables'])
    choices_name=[]
    for i in choices_list:
        for x in i:
            choices_name.append(x)
    return {"search": placeholder,
            "cols": cols,
            "table_id": table_id,
            "message_str": message_str,
            "script_bool": script_bool,
            "choices": choices_list,
            "choices_name":choices_name,
            }