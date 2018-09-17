from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from cmdb.datatable import ManufacturerTable
from cmdb.models import Manufacturer
from cmdb.forms import ManufacturerForm


@login_required
@permission_verify
def manufacturer(request):
    init = inittable(ManufacturerTable)
    kwargs={
        'kwargs':init,
        'html_title':''.join([Manufacturer._meta.verbose_name,'管理']),
        'header_temp':'header.html',
        'add_url':reverse('cmdb:manufacturer_add'),
        'editor_url':reverse('cmdb:manufacturer_editor',args=['']),
        'data_url':reverse('cmdb:manufacturer_data'),
        'delete_url':reverse('cmdb:manufacturer_delete'),
    }
    return render(request, 'table.html', kwargs)


@login_required
@permission_verify
def manufacturer_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = ManufacturerForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = ManufacturerForm()
    kwargs = {
        'html_title': ''.join(['添加',Manufacturer._meta.verbose_name]),
        'cancel': reverse('cmdb:manufacturer'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'table-add.html', kwargs)


@login_required
@permission_verify
def manufacturer_editor(request, data):
    try:
        manufacturer = Manufacturer.objects.get(id=data)
    except Exception:
        return redirect(reverse('cmdb:manufacturer_add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms =ManufacturerForm(data=request.POST, instance=Manufacturer)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)

    else:
        forms = ManufacturerForm(instance=manufacturer)
    kwargs = {
        'html_title': ''.join(['更新',Manufacturer._meta.verbose_name]),
        'cancel': reverse('cmdb:manufacturer'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'table-editor.html', kwargs)


@login_required
@permission_verify
@csrf_exempt
def manufacturer_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = Manufacturer.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required
@permission_verify
def manufacturer_data(request):
    table = ManufacturerTable(request)
    data = table.get_data()
    return JsonResponse(data)
