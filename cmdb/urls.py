"""SuperCmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from cmdb import contract
from cmdb.views import software, asset, idc, network, manufacturer, server, business

urlpatterns = [
    url(r'^asset/$', asset.asset, name='asset'),
    url(r'^asset/add/$', asset.asset_add, name='asset_add'),
    url(r'^asset/del/$', asset.asset_delete, name='asset_delete'),
    url(r'^asset/data/$', asset.asset_data, name='asset_data'),
    url(r'^collect/$', asset.asset_collect, name='asset_collect'),
    url(r'^idc/$', idc.idc, name='idc'),
    url(r'^idc/add/$', idc.idc_add, name='idc_add'),
    url(r'^idc/del/$', idc.idc_delete, name='idc_delete'),
    url(r'^idc/data/$', idc.idc_data, name='idc_data'),
    url(r'^server/$', server.server, name='server'),
    url(r'^server/add/$', server.server_add, name='server_add'),
    url(r'^server/del/$', server.server_delete, name='server_delete'),
    url(r'^server/data/$', server.server_data, name='server_data'),
    url(r'^network-device/$', network.network, name='network'),
    url(r'^network-device/add/$', network.network_add, name='network_add'),
    url(r'^network-device/del/$', network.network_delete, name='network_delete'),
    url(r'^network-device/data/$', network.network_data, name='network_data'),
    url(r'^software/$', software.software, name='software'),
    url(r'^software/add/$', software.software_add, name='software_add'),
    url(r'^software/del/$', software.software_delete, name='software_delete'),
    url(r'^software/data/$', software.software_data, name='software_data'),
    url(r'^manufacturer/$', manufacturer.manufacturer, name='manufacturer'),
    url(r'^manufacturer/add/$', manufacturer.manufacturer_add, name='manufacturer_add'),
    url(r'^manufacturer/del/$', manufacturer.manufacturer_delete, name='manufacturer_delete'),
    url(r'^manufacturer/data/$', manufacturer.manufacturer_data, name='manufacturer_data'),
    url(r'^business/$', business.business, name='business'),
    url(r'^business/add/$', business.business_add, name='business_add'),
    url(r'^business/del/$', business.business_delete, name='business_delete'),
    url(r'^business/data/$', business.business_data, name='business_data'),
    url(r'^contract/$', contract.contract, name='contract'),
    url(r'^contract/add/$', contract.contract_add, name='contract_add'),
    url(r'^contract/del/$', contract.contract_delete, name='contract_delete'),
    url(r'^contract/data/$', contract.contract_data, name='contract_data'),

    url(r'^asset/editor/(.*)$', asset.asset_editor, name='asset_editor'),
    url(r'^asset/details/(?P<sn>.*)$', asset.asset_details, name='asset_details'),
    url(r'^idc/editor/(.*)$', idc.idc_editor, name='idc_editor'),
    url(r'^server/editor/(.*)$', server.server_editor, name='server_editor'),
    url(r'^network-device/editor/(.*)$', network.network_editor, name='network_editor'),
    url(r'^software/editor/(.*)$', software.software_editor, name='software_editor'),
    url(r'^manufacturer/editor/(.*)$', manufacturer.manufacturer_editor, name='manufacturer_editor'),
    url(r'^business/editor/(.*)$', business.business_editor, name='business_editor'),
    url(r'^contract/editor/(.*)$', contract.contract_editor, name='contract_editor'),
]
