#!/usr/bin/env python
from django import template
from django.utils.safestring import mark_safe
register=template.Library()


@register.simple_tag
def table_header(choices,search=None):
    """
    :param choices: [{'status': [('', '---------'), (0, '在线'), (1, '下线')]}]
    :return: mark_safe
    """
    html=""
    for choice in choices:
        html+="<div class='form-group'>"
        for key,value in choice.items():
            html+="<select class='form-control' name='%s' id='%s' data-type='SelectData'>"%(key,'id_'+str(key))
            for va in value:
                html+="<option value='%s'>%s</option>"%(va[0],va[1])
        html+="</select></div>"
    if search:
        html+="<div class='form-group'>"
        html+="<input placeholder='%s' name='q' class='form-control' title='%s'>"%(search,search)
        html+="<a class='btn btn-primary tables-search' data-type='SearchData'>搜索</a>"
    return mark_safe(html)

@register.simple_tag
def table_choices_js():
    return mark_safe('alert(11)')


