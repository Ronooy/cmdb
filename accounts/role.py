#!/usr/bin/env python
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from accounts.datatable import RoleTable
from accounts.models import RoleList
from accounts.forms import RoleAddForm, RoleEditForm


@login_required()
@permission_verify
def role_list(request):
    kwargs = inittable(RoleTable)
    return render(request, 'accounts/role_list.html', locals())


@login_required()
@permission_verify
def role_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = RoleAddForm(data=request.POST)
        print(request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = RoleAddForm()
    kwargs = {
        'html_title': '添加角色',
        'cancel': reverse('accounts:role-list'),
        'col_md': 'col-md-8',
        'forms': forms
    }
    return render(request, 'accounts/role-add.html', kwargs)


@login_required()
@permission_verify
def role_editor(request, data):
    try:
        role = RoleList.objects.get(pk=data)
    except Exception:
        return redirect(reverse('accounts:role-add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = RoleEditForm(data=request.POST, instance=role)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = RoleEditForm(instance=role)
    kwargs = {
        'html_title': '添加用户',
        'cancel': reverse('accounts:user-list'),
        'col_md': 'col-md-8',
        'forms': forms
    }
    return render(request, 'accounts/role-editor.html', kwargs)


@csrf_exempt
@login_required()
@permission_verify
def role_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = RoleList.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required()
@permission_verify
def role_data(request):
    table = RoleTable(request)
    data = table.get_data()
    return JsonResponse(data)
