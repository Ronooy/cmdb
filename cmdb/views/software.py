from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from cmdb.datatable import SoftwareTable
from cmdb.models import Software
from cmdb.forms import SoftwareForm


@login_required
@permission_verify
def software(request):
    init = inittable(SoftwareTable)
    kwargs={
        'kwargs':init,
        'html_title':''.join([Software._meta.verbose_name,'管理']),
        'header_temp':'header.html',
        'add_url':reverse('cmdb:software_add'),
        'editor_url':reverse('cmdb:software_editor',args=['']),
        'data_url':reverse('cmdb:software_data'),
        'delete_url':reverse('cmdb:software_delete'),
    }
    return render(request, 'table.html', kwargs)


@login_required
@permission_verify
def software_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = SoftwareForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = SoftwareForm()
    kwargs = {
        'html_title': ''.join(['添加',Software._meta.verbose_name]),
        'cancel': reverse('cmdb:software'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'table-add.html', kwargs)


@login_required
@permission_verify
def software_editor(request, data):
    try:
        software = Software.objects.get(id=data)
    except Exception:
        return redirect(reverse('cmdb:software_add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms =SoftwareForm(data=request.POST, instance=software)
        if forms.is_valid():
            forms.save()
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)

    else:
        forms = SoftwareForm(instance=software)
    kwargs = {
        'html_title': ''.join(['更新',Software._meta.verbose_name]),
        'cancel': reverse('cmdb:software'),
        'col_md': 'col-md-3',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'table-editor.html', kwargs)


@login_required
@permission_verify
@csrf_exempt
def software_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('id')
    count = Software.objects.filter(id__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required
@permission_verify
def software_data(request):
    table = SoftwareTable(request)
    data = table.get_data()
    return JsonResponse(data)
