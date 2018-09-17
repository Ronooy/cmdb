from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from cmdb.datatable import IDCTable
from cmdb.models import IDC
from cmdb.forms import IDCForm


@login_required
@permission_verify
def idc(request):
    init = inittable(IDCTable)
    kwargs={
        'kwargs':init,
        'html_title':''.join([IDC._meta.verbose_name,'管理']),
        'header_temp':'header.html',
        'add_url':reverse('cmdb:idc_add'),
        'editor_url':reverse('cmdb:idc_editor',args=['']),
        'data_url':reverse('cmdb:idc_data'),
        'delete_url':reverse('cmdb:idc_delete'),
    }
    return render(request, 'table.html', kwargs)


@login_required
@permission_verify
def idc_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = IDCForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = IDCForm()
    kwargs = {
        'html_title': '添加机房',
        'cancel': reverse('cmdb:contract'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp':'header.html',
    }
    return render(request, 'table-add.html', kwargs)


@login_required
@permission_verify
def idc_editor(request, data):
    try:
        idc = IDC.objects.get(id=data)
    except Exception:
        return redirect(reverse('cmdb:idc_add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = IDCForm(data=request.POST, instance=idc)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)

    else:
        forms = IDCForm(instance=idc)
    kwargs = {
        'html_title': '更新机房',
        'cancel': reverse('cmdb:contract'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp':'header.html',
    }
    return render(request, 'table-editor.html', kwargs)


@login_required
@permission_verify
@csrf_exempt
def idc_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = IDC.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required
@permission_verify
def idc_data(request):
    table = IDCTable(request)
    data = table.get_data()
    return JsonResponse(data)
