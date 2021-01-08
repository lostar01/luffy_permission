from django.shortcuts import render,redirect,reverse
from rbac.models import Menu

def menu_list(request):
    menus = Menu.objects.all()

    menu_id = request.GET.get('mid')
    return render(request,'rbac/menu_list.html',{"menus":menus,"menu_id": menu_id})