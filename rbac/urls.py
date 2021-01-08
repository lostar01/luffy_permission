from django.conf.urls import url
from rbac.views import role,user,menu

urlpatterns = [
    url(r'^role/list/$', role.role_list,name='role_list'),
    url(r'^role/add/$', role.role_add,name='role_add'),
    url((r'^role/edit/(?P<rid>\d+)/$'),role.role_edit,name='role_edit'),
    url(r'^role/del/(?P<rid>\d+)/$',role.role_del,name='role_del'),

    url(r'^user/list/$', user.user_list,name='user_list'),
    url(r'^user/add/$', user.user_add,name='user_add'),
    url((r'^user/edit/(?P<rid>\d+)/$'),user.user_edit,name='user_edit'),
    url(r'^user/del/(?P<rid>\d+)/$',user.user_del,name='user_del'),
    url(r'^user/resetpwd/(?P<rid>\d+)/$',user.user_resetpwd,name='user_resetpwd'),

    url(r'^menu/list/$',menu.menu_list,name='menu_list'),


]
