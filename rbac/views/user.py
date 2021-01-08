from django.shortcuts import render,redirect,reverse,HttpResponse
from rbac.models import UserInfo
from rbac.forms.user import UserInfoModelForm, UserInfoUpdateModelForm, UserInfoResetPwdModelForm


def user_list(request):

    data_list = UserInfo.objects.all()
    return render(request,'rbac/user_list.html',{"data_list": data_list})

def user_add(request):
    form = UserInfoModelForm()

    if request.method == 'POST':
        form = UserInfoModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse('rbac:user_list')
            return redirect(url)
    return render(request,'rbac/userchange.html',{"form": form})

def user_edit(request,rid):
    role_obj = UserInfo.objects.get(pk=rid)
    if not role_obj:
        return HttpResponse("用户不存在")
    form = UserInfoUpdateModelForm(instance=role_obj)
    if request.method == 'POST':
        form = UserInfoUpdateModelForm(data=request.POST,instance=role_obj)
        if form.is_valid():
            form.save()
            url = reverse('rbac:user_list')
            return redirect(url)
    return render(request,'rbac/userchange.html',{"form": form })


def user_del(request,rid):
    url = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request,'rbac/delete.html',{"cancel_url": url})
    try:
        UserInfo.objects.filter(pk=rid).delete()
        return redirect(url)
    except:
        return HttpResponse("删除失败")


def user_resetpwd(request,rid):
    url = reverse('rbac:user_list')
    user_obj = UserInfo.objects.get(pk=rid)
    if not user_obj:
        return HttpResponse("用户不存在")
    form = UserInfoResetPwdModelForm(instance=user_obj)
    if request.method == 'POST':
        form = UserInfoResetPwdModelForm(data=request.POST,instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect(url)
    return render(request, 'rbac/userchange.html', {"form": form})