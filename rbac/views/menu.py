from django.shortcuts import render, redirect, reverse, HttpResponse

from rbac.forms.memu import MenuModelForm
from rbac.models import Menu, Permission
from rbac.service.urls import memory_reverse


def menu_list(request):
    menus = Menu.objects.all()
    second_menus = []
    permission_menus = []
    menu_id = request.GET.get('mid')
    smenu_id = request.GET.get('smid')
    pmenu_id = request.GET.get('pmid')
    if menu_id:
        second_menus = Permission.objects.filter(menu_id=menu_id)

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
