from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from cmdb.datatable import ServerTable
from cmdb.models import Server
from cmdb.forms import ServerForm


@login_required
@permission_verify
def server(request):
    init = inittable(ServerTable)
    kwargs={
        'kwargs':init,
        'html_title':''.join([Server._meta.verbose_name,'管理']),
        'header_temp':'header.html',
        'add_url':reverse('cmdb:server_add'),
        'editor_url':reverse('cmdb:server_editor',args=['']),
        'data_url':reverse('cmdb:server_data'),
        'delete_url':reverse('cmdb:server_delete'),
    }
    return render(request, 'table.html', kwargs)


@login_required
@permission_verify
def server_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = ServerForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = ServerForm()
    kwargs = {
        'html_title': '添加服务器',
        'cancel': reverse('cmdb:server'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'table-add.html', kwargs)


@login_required
@permission_verify
def server_editor(request, data):
    try:
        server = Server.objects.get(id=data)
    except Exception:
        return redirect(reverse('cmdb:server_add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = ServerForm(data=request.POST, instance=server)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)

    else:
        forms = ServerForm(instance=server)
    kwargs = {
        'html_title': '更新服务器',
        'cancel': reverse('cmdb:server'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'table-editor.html', kwargs)


@login_required
@permission_verify
@csrf_exempt
def server_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = Server.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required
@permission_verify
def server_data(request):
    table = ServerTable(request)
    data = table.get_data()
    return JsonResponse(data)
