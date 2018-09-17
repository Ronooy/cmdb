#!/usr/bin/env python
from django.conf.urls import url
from accounts import user,role,permission

urlpatterns = [
    url('^login/$', user.login, name='login'),
    url('^logout/$', user.logout, name='logout'),
    url('^user/list/$', user.user_list, name='user-list'),
    url('^user/data/$', user.user_data, name='user-data'),
    url('^user/add/$',user.user_add,name='user-add'),
    url('^user/delete/$', user.user_delete, name='user-delete'),
    url('^user/editor/(\d*)', user.user_editor, name='user-editor'),
    url('^change/password/$', user.change_password, name='change-password'),

    url(r'^role/list/$', view=role.role_list, name='role-list'),
    url(r'^role/add/$', view=role.role_add, name='role-add'),
    url(r'^role/delete/$', view=role.role_delete, name='role-delete'),
    url(r'^role/editor/(\d*)$', view=role.role_editor, name='role-editor'),
    url(r'^role/data/$', view=role.role_data, name='role-data'),

    url(r'^permission/list/$', view=permission.permission_list, name='permission-list'),
    url(r'^permission/add/$', view=permission.permission_add, name='permission-add'),
    url(r'^permission/delete/$', view=permission.permission_delete, name='permission-delete'),
    url(r'^permission/editor/(\d*)$', view=permission.permission_editor, name='permission-editor'),
    url(r'^permission/data/$', view=permission.permission_data, name='permission-data'),
    url(r'^permission/deny/$',view=permission.permission_deny,name='permission-deny'),
]
