#!/usr/bin/env python
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from datatables.utils import inittable

from accounts.models import PermissionList, RoleList, UserInfo
from accounts.datatable import PermissionTable
from accounts.forms import PermissionAddForm


def permission_verify(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        user = UserInfo.objects.get(username=request.user)
        if not user.is_superuser:
            if not user.role:
                return redirect(reverse('accounts:permission-deny'))
            role_permissions = RoleList.objects.get(name=user.role)
            permission_list = role_permissions.permissions.all()
            per = []
            for p in permission_list:
                if request.path == p.url or request.path.rstrip('/') == p.url:
                    per.append(p)
                elif request.path.startswith(p.url):
                    per.append(p)
                else:
                    pass
            if len(per) == 0:
                return redirect(reverse('accounts:permission-deny'))
        return view_func(request, *args, **kwargs)

    return _wrapper


@login_required()
@permission_verify
def permission_list(request):
    kwargs = inittable(PermissionTable)
    return render(request, 'accounts/permission-list.html', locals())


@login_required()
@permission_verify
def permission_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = PermissionAddForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = PermissionAddForm()
    kwargs = {
        'html_title': '添加权限',
        'cancel': reverse('accounts:permission-list'),
        'col_md': '',
        'forms': forms
    }
    return render(request, 'accounts/permission-add.html', kwargs)


@login_required()
@permission_verify
def permission_editor(request, data):
    try:
        permission = PermissionList.objects.get(pk=data)
    except Exception:
        return redirect(reverse('accounts:permission_add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = PermissionAddForm(data=request.POST, instance=permission)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)

    else:
        forms = PermissionAddForm(instance=permission)
    kwargs = {
        'html_title': '更新权限',
        'cancel': reverse('accounts:permission-list'),
        'col_md': '',
        'forms': forms
    }
    return render(request, 'accounts/permission-editor.html', kwargs)


@csrf_exempt
@login_required()
@permission_verify
def permission_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = PermissionList.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required()
def permission_deny(request):
    return render(request, 'accounts/permission-deny.html', status=403)


@login_required()
@permission_verify
def permission_data(request):
    table = PermissionTable(request)
    data = table.get_data()
    return JsonResponse(data)
