from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from datatables.utils import inittable

from cmdb.datatable import AssetTable
from cmdb.models import Asset, Tag
from cmdb.forms import AssetForm


@login_required
@permission_verify
def asset(request):
    kwargs = inittable(AssetTable)
    header_temp = 'header.html'
    return render(request, 'cmdb/asset/asset.html', locals())


@login_required
@permission_verify
def asset_details(request, sn):
    asset = Asset.objects.get(sn=sn)
    html_title = '%s %s' % (sn, Asset._meta.verbose_name)
    header_temp = 'header.html'
    return render(request, 'cmdb/asset/asset_details.html', locals())


@login_required
@permission_verify
def asset_add(request):
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = AssetForm(data=request.POST)
        if forms.is_valid():
            instance = forms.save()
            print(forms.cleaned_data.get('label'))
            label = forms.cleaned_data.get('label', '').split(',')
            tags = []
            for t in label:
                t = t.strip()
                if t:
                    tag, flag = Tag.objects.get_or_create(name=t)
                    tags.append(tag)
            if tags:
                instance.tags.add(*tags)
            JSON_RESULT['message'] = '添加成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)
    else:
        forms = AssetForm()
    kwargs = {
        'html_title': '添加资产',
        'cancel': reverse('cmdb:asset'),
        'col_md': 'col-md-4',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'cmdb/asset/asset-add.html', kwargs)


@login_required
@permission_verify
def asset_editor(request, data):
    try:
        asset = Asset.objects.filter(sn=data).prefetch_related('tags')[0]
    except Exception:
        return redirect(reverse('cmdb:asset-add'))
    if request.method == 'POST':
        JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
        forms = AssetForm(data=request.POST, instance=asset)
        if forms.is_valid():
            instance = forms.save()
            label = forms.cleaned_data.get('label', '').split(',')
            tags = []
            for t in label:
                t = t.strip()
                if t:
                    tag, flag = Tag.objects.get_or_create(name=t)
                    tags.append(tag)
            if tags:
                instance.tags.set(tags)
            JSON_RESULT['message'] = '更新成功'
            return JsonResponse(JSON_RESULT)
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = forms.errors.as_json()
        return JsonResponse(JSON_RESULT)

    else:
        forms = AssetForm(instance=asset)
    kwargs = {
        'html_title': '更新资产',
        'cancel': reverse('cmdb:asset'),
        'col_md': 'col-md-5',
        'forms': forms,
        'header_temp': 'header.html',
    }
    return render(request, 'cmdb/asset/asset-editor.html', kwargs)


@login_required
@permission_verify
@csrf_exempt
def asset_delete(request):
    JSON_RESULT = {'status': 200, 'message': '', 'error': '', 'data': []}
    res = request.POST.getlist('sn')
    count = Asset.objects.filter(sn__in=res).delete()
    if count[0] > 0:
        JSON_RESULT['message'] = '删除成功'
    else:
        JSON_RESULT['status'] = 201
        JSON_RESULT['error'] = '删除失败'
    return JsonResponse(JSON_RESULT)


@login_required
@permission_verify
def asset_data(request):
    table = AssetTable(request)
    data = table.get_data()
    return JsonResponse(data)


def asset_collect(request):
    pass