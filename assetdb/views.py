#!/usr/bin/env python
from django.shortcuts import render
from cmdb.models import Asset
from cmdb import models

def dashboard(request):
    total=Asset.objects.count()
    online=Asset.objects.filter(status=0).count()
    noline=Asset.objects.filter(status=1).count()
    unknown=Asset.objects.filter(status=2).count()
    breakdown=Asset.objects.filter(status=3).count()
    backup=Asset.objects.filter(status=4).count()

    on_rate = round(online / total * 100)
    no_rate = round(noline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)
    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()
    xAxis = ['在线', '下线', '故障', '备用', '未知']
    yAxis = [online, noline, breakdown, backup, unknown]
    server_xAxis=['服务器','网络设备','存储设备','安全设备','付费软件/系统']
    temp=[server_number,networkdevice_number,storagedevice_number,
                  securitydevice_number,software_number]
    server_yAxis=[]
    for i,t in enumerate(server_xAxis):
        server_yAxis.append({'value':temp[i],'name':server_xAxis[i]})
    print(server_yAxis)
    return render(request,'dashboard.html',locals())


