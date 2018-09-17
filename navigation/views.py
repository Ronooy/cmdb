from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from navigation.datatable import NavTable
from navigation.models import NavStore
from navigation.forms import NavStoreForm


@login_required
@permission_verify
def index(request):
    html_title='站点导航'
    nav=NavStore.objects.all().values('name','url','remark')
    return render(request, 'navigation/index.html', locals())


@login_required
@permission_verify
def nav_list(request):
    kwargs = inittable(NavTable)
    return render(request, 'navigation/nav-list.html', locals())


@login_required
@permission_verify
def nav_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = NavStoreForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = NavStoreForm()
    html_title = '添加站点'
    cancel = reverse('navigation:nav-list')
    return render(request, 'navigation/nav-add.html', locals())


@login_required
@permission_verify
def nav_editor(request, data):
    try:
        nav = NavStore.objects.get(pk=data)
    except Exception:
        return redirect(reverse('accounts:user-add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = NavStoreForm(data=request.POST, instance=nav)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '%s-更新成功' % forms.cleaned_data.get('name')
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = NavStoreForm(instance=nav)
    html_title = '更新站点'
    cancel = reverse('navigation:nav-list')
    return render(request, 'navigation/nav-editor.html', locals())


@login_required
@permission_verify
@csrf_exempt
def nav_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = NavStore.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required
@permission_verify
def nav_data(request):
    table = NavTable(request)
    data = table.get_data()
    return JsonResponse(data)
