from collections import OrderedDict

from django.forms import formset_factory
from django.shortcuts import render, redirect, reverse, HttpResponse
from rbac.forms.memu import MenuModelForm, SmenuModelForm, PmenuModelForm,MultiAddPermissionForm,MultiEditPermissionForm
from rbac.models import Menu, Permission
from rbac.service.route import get_all_url_dict
from rbac.service.urls import memory_reverse
from django.http import QueryDict


def menu_list(request):
    menus = Menu.objects.all()
    second_menus = []
    permission_menus = []
    menu_id = request.GET.get('mid')
    smenu_id = request.GET.get('smid')
    pmenu_id = request.GET.get('pmid')
    if menu_id:
        mobj = Menu.objects.filter(pk=menu_id)
        second_menus = Permission.objects.filter(menu_id=menu_id)
        if not mobj:
            menu_id = None

    if smenu_id:
        sobj = Permission.objects.filter(pk=smenu_id)
        permission_menus = Permission.objects.filter(pid_id=smenu_id)
        if not sobj:
            smenu_id = None

    if pmenu_id:
        pobj = Permission.objects.get(pk=pmenu_id)

    return render(request, 'rbac/menu_list.html',
                  {"menus": menus, "menu_id": menu_id, "second_menus": second_menus, "smenu_id": smenu_id,
                   "permission_menus": permission_menus, "pmenu_id": pmenu_id})


def menu_add(request):
    form = MenuModelForm()

    if request.method == 'POST':
        form = MenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')

            return redirect(url)
    return render(request, 'rbac/change_menu.html', {"form": form})


def menu_edit(request, mid):
    mobj = Menu.objects.get(pk=mid)
    if not mobj:
        return HttpResponse("菜单不存在")
    form = MenuModelForm(instance=mobj)
    if request.method == 'POST':
        form = MenuModelForm(request.POST, instance=mobj)
        if form.is_valid():
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')
            return redirect(url)
    return render(request, 'rbac/change_menu.html', {"form": form})


def menu_del(request, mid):
    url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'POST':
        try:
            Menu.objects.filter(pk=mid).delete()
            return redirect(url)
        except:
            return HttpResponse("删除失败")

    return render(request, 'rbac/delete.html', {"cancel_url": url})


def smenu_add(request):
    orgin_params = request.GET.get('_filter')
    params_dict = QueryDict(orgin_params)

    mobj = Menu.objects.get(pk=params_dict['mid'])
    form = SmenuModelForm()

    if request.method == 'POST':
        form = SmenuModelForm(data=request.POST)
        if form.is_valid():
            form.instance.menu = mobj
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')

            return redirect(url)
    return render(request, 'rbac/change_menu.html', {"form": form})


def smenu_edit(request, pid):
    pobj = Permission.objects.get(pk=pid)
    if not pobj:
        return HttpResponse("菜单不存在")
    form = SmenuModelForm(instance=pobj)
    if request.method == 'POST':
        form = SmenuModelForm(data=request.POST,instance=pobj)
        if form.is_valid():
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')
            return redirect(url)
    return render(request, 'rbac/change_menu.html', {"form": form})


def smenu_del(request, pid):
    url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'POST':
        try:
            Permission.objects.filter(pk=pid).delete()
            return redirect(url)
        except:
            return HttpResponse("删除失败")

    return render(request, 'rbac/delete.html', {"cancel_url": url})

#权限管理
def pmenu_add(request):
    orgin_params = request.GET.get('_filter')
    params_dict = QueryDict(orgin_params)

    pobj = Permission.objects.get(pk=params_dict['smid'])
    if not pobj:
        return HttpResponse("权限不存在")
    form = PmenuModelForm()
    if request.method == 'POST':
        form = PmenuModelForm(data=request.POST)
        if form.is_valid():
            form.instance.pid = pobj
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')

            return redirect(url)
    return render(request, 'rbac/change_menu.html', {"form": form})


def pmenu_edit(request, pid):
    pobj = Permission.objects.get(pk=pid)
    if not pobj:
        return HttpResponse("菜单不存在")
    form = PmenuModelForm(instance=pobj)
    if request.method == 'POST':
        form = PmenuModelForm(data=request.POST,instance=pobj)
        if form.is_valid():
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')
            return redirect(url)
    return render(request, 'rbac/change_menu.html', {"form": form})


def pmenu_del(request, pid):
    url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'POST':
        try:
            Permission.objects.filter(pk=pid).delete()
            return redirect(url)
        except:
            return HttpResponse("删除失败")

    return render(request, 'rbac/delete.html', {"cancel_url": url})


def multi_pmenu(request):
    """
    批量操作权限
    """
    #1.获取项目中所有的URL
    all_url_dict = get_all_url_dict()

    router_name_set = set(all_url_dict.keys())

    #2.获取数据库中所有的URL
    permissions = Permission.objects.all().values('id','title','url_name','url','menu_id','pid_id')
    permission_dict = OrderedDict()
    permission_name_set = set()

    for row in permissions:
        permission_dict[row['url_name']] = row
        permission_name_set.add(row['url_name'])


    #3. 应该添加，删除，修改的权限有哪些

    for name,value in permission_dict.items():
        route_row_dict = all_url_dict.get(name)
        if not route_row_dict:
            continue
        if value['url'] != route_row_dict['url']:
            value['url'] = '路由和数据库中不一致'

    #3.1计算出应该增加的name
    generate_name_list = router_name_set - permission_name_set
    generate_formset_class = formset_factory(MultiAddPermissionForm,extra=0)
    generate_formset = generate_formset_class(initial=[ row_dict for name,row_dict in all_url_dict.items() if name in generate_name_list])

    #3.2 计算出需要删除的name
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [ row_dict for name,row_dict in permission_dict.items() if name in delete_name_list ]

    #3.3 计算出应该更新的name
    update_name_list = permission_name_set & router_name_set
    update_formset_class = formset_factory(MultiEditPermissionForm,extra=0)
    update_formset = update_formset_class(initial=[ row_dict for name,row_dict in permission_dict.items() if name in update_name_list])

    return render(request,'rbac/multi_permissions.html',
                  {
                      "generate_formset": generate_formset,

                  })