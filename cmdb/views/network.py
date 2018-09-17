from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from cmdb.datatable import NetworkTable
from cmdb.models import NetworkDevice
from cmdb.forms import NetworkForm


@login_required
@permission_verify
def network(request):
    init = inittable(NetworkTable)
    kwargs={
        'kwargs':init,
        'html_title':''.join([NetworkDevice._meta.verbose_name,'管理']),
        'header_temp':'header.html',
        'add_url':reverse('cmdb:network_add'),
        'editor_url':reverse('cmdb:network_editor',args=['']),
        'data_url':reverse('cmdb:network_data'),
        'delete_url':reverse('cmdb:network_delete'),
    }
    return render(request, 'table.html', kwargs)


@login_required
@permission_verify
def network_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = NetworkForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = NetworkForm()
    kwargs = {
        'html_title': '添加网络设备',
        'cancel': reverse('cmdb:network'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'table-add.html', kwargs)


@login_required
@permission_verify
def network_editor(request, data):
    try:
        network = NetworkDevice.objects.get(id=data)
    except Exception:
        return redirect(reverse('cmdb:network_add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms =NetworkForm(data=request.POST, instance=network)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)

    else:
        forms = NetworkForm(instance=network)
    kwargs = {
        'html_title': '更新网络设备',
        'cancel': reverse('cmdb:network'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'table-editor.html', kwargs)


@login_required
@permission_verify
@csrf_exempt
def network_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = NetworkDevice.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required
@permission_verify
def network_data(request):
    table = NetworkTable(request)
    data = table.get_data()
    return JsonResponse(data)
