from django.shortcuts import render,redirect,reverse,HttpResponse
from rbac.models import Role
from rbac.forms.role import RoleModelForm

def role_list(request):

    data_list = Role.objects.all()
    return render(request,'rbac/role_list.html',{"data_list": data_list})

def role_add(request):
    form = RoleModelForm()

    if request.method == 'POST':
        form = RoleModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse('rbac:role_list')
            return redirect(url)
    return render(request,'rbac/change.html',{"form": form})

def role_edit(request,rid):
    role_obj = Role.objects.get(pk=rid)
    form = RoleModelForm(instance=role_obj)
    if request.method == 'POST':
        form = RoleModelForm(data=request.POST,instance=role_obj)
        if form.is_valid():
            form.save()
            url = reverse('rbac:role_list')
            return redirect(url)
    return render(request,'rbac/change.html',{"form": form })


def role_del(request,rid):
    url = reverse('rbac:role_list')
    if request.method == 'GET':
        return render(request,'rbac/delete.html',{"cancel_url": url})
    try:
        Role.objects.filter(pk=rid).delete()
        return redirect(url)
    except:
        return HttpResponse("删除失败")