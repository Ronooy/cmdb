#!/usr/bin/env python
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import mark_safe
from django.utils import timezone
import json


def paginated(query_set, page=None, limit=None):
    try:
        paginator = Paginator(query_set, int(limit))
    except Exception:
        paginator = Paginator(query_set, 10)
    try:
        pageObj = paginator.page(int(page))
    except:
        pageObj = paginator.page(1)
    return paginator, pageObj


def create_link_field(html, script_id, fie):
    html += """<script type="text/html" id="%s">""" % script_id
    html += """{{#  if(d.%s === true){ }}""" % fie.name
    html += """<i class="fa fa-check-circle" style="color: #009688"></i>"""
    html += """{{#  } else { }}"""
    html += """<i class="fa fa-times-circle" style="color: #FF5722"></i>"""
    html += """{{#  } }}</script>"""
    return html


class BaseTable(object):
    model = None
    list_display = []
    exclude = []
    ordering = 'id'
    sort_field = []
    list_display_links = []
    search_fields = []  # 查询字段
    message_str = 'id'  # layui alert弹窗时候的提醒字段
    choices_field = []  # 前端显示 choices 或者外键的下拉框
    choices_field_blank = {}  # 下拉框空白提示{'字段':'资产类型'}
    limit = 'limit'
    page = 'page'
    query = 'q'


class CreateTable(BaseTable):
    def __init__(self, request):
        """
        序列化表格数据 create_date生成fields所允许的字段数据
        """
        limit = request.GET.get(self.limit)
        page = request.GET.get(self.page)
        q = request.GET.get(self.query)
        choices = {}
        if isinstance(self.choices_field, (list, tuple)):
            for cf in self.choices_field:
                post = request.GET.get(cf)
                if post:
                    choices[cf] = post
        q_choice = self.filter_choices(**choices)
        q_query = Q()
        q_query.connector = 'OR'
        if q:
            for qw in self.search_fields:
                q_query.children.append((qw + '__icontains', q.strip()))
        query_set = self.model.objects.filter(q_query, q_choice).order_by(self.ordering if self.ordering else 'id')
        self.paginator, self.pageObj = paginated(query_set, page, limit)

    def filter_choices(self, connector='AND', **kwargs):
        """
        查询choices类型字段
        :param kwargs: post提交的参数
        :return: q对象
        """
        q = Q()
        q.connector = connector
        for k, v in kwargs.items():
            f = self.model._meta.get_field(k)
            if type(f).__name__ == 'ForeignKey':
                q.children.append((f.name + '_id', v))
            else:
                for row in f.choices:
                    if str(row[0]) == v:
                        q.children.append((k, v))
        return q

    def create_data(self):
        table_data = []
        for obj in self.pageObj:
            data = {}
            if self.list_display == '__all__':
                self.list_display = [i.name for i in self.model._meta.fields]
            for field in self.list_display:
                if field in self.exclude: continue
                f = obj._meta.get_field(field)
                if f.choices:
                    value = getattr(obj, 'get_%s_display' % field)()
                else:
                    field_type_name = type(f).__name__
                    value = getattr(obj, field)
                    if field_type_name == 'DateTimeField':
                        value = timezone.localtime(value).strftime('%Y-%m-%d %H:%M:%S')
                    elif field_type_name in ['ForeignKey', 'OneToOneField']:
                        value = value.__str__() if value.__str__() != 'None' else ''
                # if type(value).__name__ == 'datetime':
                #     value = timezone.localtime(value)
                # if type(value).__name__ == 'ManyRelatedManager':
                #     print(value)
                #     value = ''
                data.update({field: value})
            table_data.append(data)
        return table_data

    @classmethod
    def get_tableHeader(cls):
        cols = [{'type': 'checkbox'}, {'type': 'numbers', 'title': '序号'}]
        html = """"""
        fields_list = [_ for _ in cls.model._meta.get_fields()]
        if cls.list_display == '__all__':
            cls.list_display = [i.name for i in cls.model._meta.fields]
        for index, field in enumerate(cls.list_display):
            if field == 'id': continue
            if field in cls.exclude: continue
            for fie in fields_list:
                if fie.name == field:
                    field_type = type(cls.model._meta.get_field(fie.name)).__name__
                    if field_type == 'BooleanField':
                        script_id = ''.join([fie.name, '_', str(index)])
                        cols.append({"field": fie.name, 'title': str(fie.verbose_name),
                                     'templet': '#' + script_id, 'unresize': True})
                        html += """<script type="text/html" id="%s">""" % script_id
                        html += """{{#  if(d.%s === true){ }}""" % fie.name
                        html += """<i class="fa fa-check-circle" style="color: #009688"></i>"""
                        html += """{{#  } else { }}"""
                        html += """<i class="fa fa-times-circle" style="color: #FF5722"></i>"""
                        html += """{{#  } }}</script>"""
                    else:
                        if fie.name in cls.sort_field:
                            d = {"field": fie.name, 'title': str(fie.verbose_name), 'sort': 'true'}
                        else:
                            d = {"field": fie.name, 'title': str(fie.verbose_name)}
                        cols.append(d)

                    fields_list.remove(fie)
                    break
        cols.append({"field": 'right', 'title': '操作',
                     'toolbar': '#' + cls.model._meta.label.split('.')[1].lower() + '-toolbar', 'width': 180})
        choices_list = []
        if isinstance(cls.choices_field, bool) and cls.choices_field == True:
            for field in cls.model._meta.fields:
                if field.choices:
                    choices_list.append({field.name: field.get_choices()})
        elif isinstance(cls.choices_field, (list, tuple)):
            for field in cls.choices_field:
                field_cls = cls.model._meta.get_field(field)
                blank_choice = cls.choices_field_blank.get(field)
                if blank_choice:
                    value = field_cls.get_choices(blank_choice=[('', blank_choice)])
                else:
                    value = field_cls.get_choices(blank_choice=[('', field_cls.verbose_name)])
                if value:
                    choices_list.append({field_cls.name: value})
        return (json.dumps(cols), mark_safe(html), choices_list)

    def get_data(self, **kwargs):
        data = self.create_data()
        layui_data = {
            'status': kwargs.get('status', 200),
            'message': kwargs.get('message', ''),
            'count': self.paginator.count,
            'data': data,
        }
        return layui_data
