from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from cmdb.datatable import ContractTable
from cmdb.models import Contract
from cmdb.forms import ContractUnitForm


@login_required
@permission_verify
def contract(request):
    init = inittable(ContractTable)
    kwargs={
        'kwargs':init,
        'html_title':''.join([Contract._meta.verbose_name,'管理']),
        'header_temp':'header.html',
        'add_url':reverse('cmdb:contract_add'),
        'editor_url':reverse('cmdb:contract_editor',args=['']),
        'data_url':reverse('cmdb:contract_data'),
        'delete_url':reverse('cmdb:contract_delete'),
    }
    return render(request, 'cmdb/contract/contract.html', kwargs)


@login_required
@permission_verify
def contract_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = ContractUnitForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = ContractUnitForm()
    kwargs = {
        'html_title': ''.join(['添加',Contract._meta.verbose_name]),
        'cancel': reverse('cmdb:contract'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'cmdb/contract/contract-add.html', kwargs)


@login_required
@permission_verify
def contract_editor(request, data):
    try:
        contract = Contract.objects.get(id=data)
    except Exception:
        return redirect(reverse('cmdb:contract_add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms =ContractUnitForm(data=request.POST, instance=contract)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)

    else:
        forms = ContractUnitForm(instance=contract)
    kwargs = {
        'html_title': ''.join(['更新',Contract._meta.verbose_name]),
        'cancel': reverse('cmdb:contract'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'cmdb/contract/contract-editor.html', kwargs)


@login_required
@permission_verify
@csrf_exempt
def contract_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = Contract.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required
@permission_verify
def contract_data(request):
    table = ContractTable(request)
    data = table.get_data()
    return JsonResponse(data)
