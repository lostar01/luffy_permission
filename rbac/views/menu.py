import datetime
from collections import OrderedDict

from django.forms import formset_factory
from django.shortcuts import render, redirect, reverse, HttpResponse
from rbac.forms.memu import MenuModelForm, SmenuModelForm, PmenuModelForm, MultiAddPermissionForm, \
    MultiEditPermissionForm
from rbac.models import Menu, Permission, UserInfo, Role
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
    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)

    post_type = request.GET.get('type')
    generate_formset = None
    update_formset = None
    if request.method == 'POST' and post_type == 'generate':
        # pass  #批量添加
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0,formset.total_form_count()):
                row_dict = post_row_list[i]
                print(row_dict)
                try:
                    new_object = Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:
                Permission.objects.bulk_create(object_list,batch_size=100)
        else:
            generate_formset = formset

    if request.method == 'POST' and post_type == 'update':
        # pass  #批量更新
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0,formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = Permission.objects.filter(id=permission_id).first()
                    for k,v in row_dict.items():
                        setattr(row_object,k,v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset

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
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = generate_formset_class(initial=[ row_dict for name,row_dict in all_url_dict.items() if name in generate_name_list])


    #3.2 计算出需要删除的name
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [ row_dict for name,row_dict in permission_dict.items() if name in delete_name_list ]

    #3.3 计算出应该更新的name
    if not update_formset:
        update_name_list = permission_name_set & router_name_set
        update_formset = update_formset_class(initial=[ row_dict for name,row_dict in permission_dict.items() if name in update_name_list])

    return render(request,'rbac/multi_permissions.html',
                  {
                      "generate_formset": generate_formset,
                      "delete_row_list": delete_row_list,
                      "update_formset": update_formset,

                  })


def multi_pmenu_del(request,pk):
    url = memory_reverse(request,"rbac:multi_pmenu")
    if request.method == 'POST':
        Permission.objects.filter(id=pk).delete()
        return redirect(url)

    return render(request,'rbac/delete.html',{"cancel_url": url})


def distribute_pmenu(request):

    all_user_list = UserInfo.objects.all()
    all_role_list = Role.objects.all()
    #所有的一级菜单
    all_menu_list = Menu.objects.all().values('id','title')
    all_menu_dict = {}

    for item in all_menu_list:
        all_menu_dict[item['id']] = item



    #所有的二级菜单
    all_second_menu_list = Permission.objects.filter(menu__isnull=False).values('id','title','menu_id')
    all_second_menu_dict = {}

    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict['id'] = row
        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    #所有的三级菜单
    all_permission_list = Permission.objects.filter(menu__isnull=True).values('id','title','pid_id')
    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)

    """
    [
        { 
           id: 1,
           title: '业务管理',
           children: [
                { id: 11,
                  title: '账单列表',
                  children: [
                {'id': 12, title: '添加账单'}
                ]
                },
                { 'id': 15, title: '客户列表'},
                
           ]
        },
    ]
    """

    return render(request,'rbac/distribute_permissions.html',{
        "user_list": all_user_list,
        "role_list": all_role_list,
        "all_menu_list": all_menu_list,
        "all_menu_dict": all_menu_dict,
    })