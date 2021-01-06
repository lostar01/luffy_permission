from django.conf.urls import url
from rbac.views import role
urlpatterns = [
    url(r'^role/list/$', role.role_list,name='role_list'),

]
