#!/usr/bin/env python
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from datatables.utils import inittable
from accounts.models import UserInfo
from accounts.forms import LoginUserForm, UserAddForm,UserEditForm,ChangePasswordForm
from accounts.permission import permission_verify
from accounts.datatable import UserTable



def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('url', '/')
            user = auth.login(request, form.get_user())
            return JsonResponse({'URL': url})
        return JsonResponse(form.errors.as_json(), safe=False)
    else:
        form = LoginUserForm(initial={'url': request.GET.get('next', '/')})
    return render(request, 'accounts/login.html', locals())


def logout(request):
    auth.logout(request)
    return redirect(reverse('accounts:login'))


@login_required
@permission_verify
def user_list(request):
    kwargs = inittable(UserTable)
    header_temp='header.html'
    return render(request, 'accounts/user_list.html', locals())



@login_required
@permission_verify
def user_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = UserAddForm(request, data=request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.set_password(forms.cleaned_data['password'])
            user.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = UserAddForm(request)
    kwargs = {
        'html_title': '添加用户',
        'cancel': reverse('accounts:user-list'),
        'col_md': 'col-md-3',
        'forms': forms
    }
    return render(request, 'accounts/user-editor.html', kwargs)

@login_required
@permission_verify
def user_editor(request,data):
    try:
        user = UserInfo.objects.get(pk=data)
        if not request.user.is_superuser and (request.user.pk != user.pk):
            return redirect(reverse('accounts:permission-deny'))
    except Exception:
        return redirect(reverse('accounts:user-add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = UserEditForm(request,data=request.POST, instance=user)
        print(request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message']='%s-更新成功'%forms.cleaned_data.get('username')
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status']=201
        JSON_RESULT['error']=forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = UserEditForm(request,instance=user)
    kwargs = {
        'html_title': '更新用户',
        'cancel': reverse('accounts:user-list'),
        'col_md': 'col-md-2',
        'forms': forms
    }
    return render(request, 'accounts/user-add.html', kwargs)



@login_required
@permission_verify
@csrf_exempt
def user_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    if str(request.user.pk) in res:
        JSON_RESULT['status']=201
        JSON_RESULT['error']='不能删除自己'
        return JsonResponse(JSON_RESULT)
    count=UserInfo.objects.filter(id__in=res).delete()
    if count[0] >0:
        JSON_RESULT['message']='删除成功'
    else:
        JSON_RESULT['status']=201
        JSON_RESULT['error']='删除失败'
    return JsonResponse(JSON_RESULT)

@login_required
@permission_verify
def change_password(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms=ChangePasswordForm(request,data=request.POST)
        if forms.is_valid():
            forms.save()
            auth.update_session_auth_hash(request,request.user)
            JSON_RESULT['message']='修改成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status']=201
        JSON_RESULT['error']=forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms=ChangePasswordForm(request)
    html_title='修改密码'
    cancel=reverse('accounts:user-list')
    return render(request,'accounts/change_password.html',locals())

@login_required
@permission_verify
def user_data(request):
    table = UserTable(request)
    data = table.get_data()
    return JsonResponse(data)