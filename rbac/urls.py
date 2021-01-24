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
    url(r'^menu/add/$',menu.menu_add,name='menu_add'),
    url(r'^menu/edit/(?P<mid>\d+)/$',menu.menu_edit,name='menu_edit'),
    url(r'^menu/del/(?P<mid>\d+)/$',menu.menu_del,name='menu_del'),

    url(r'^smenu/add/$',menu.smenu_add,name='smenu_add'),
    url(r'^smenu/edit/(?P<pid>\d+)/$',menu.smenu_edit,name='smenu_edit'),
    url(r'^smenu/del/(?P<pid>\d+)/$',menu.smenu_del,name='smenu_del'),

    url(r'^pmenu/add/$',menu.pmenu_add,name='pmenu_add'),
    url(r'^pmenu/edit/(?P<pid>\d+)/$',menu.pmenu_edit,name='pmenu_edit'),
    url(r'^pmenu/del/(?P<pid>\d+)/$',menu.pmenu_del,name='pmenu_del'),

    url(r'^multi/pmenu/$',menu.multi_pmenu,name='multi_pmenu'),


]
