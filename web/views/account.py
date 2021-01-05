#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse, render, redirect
from rbac import models
from rbac.service.init_permission import init_permission
from web.forms.userinfo import UserInfoModelForm


def login(request):
    # 1. 用户登录
    if request.method == 'GET':
        form = UserInfoModelForm()
        return render(request, 'login.html',{"form": form })

    user = request.POST.get('name')
    pwd = request.POST.get('password')
    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    init_permission(current_user, request)

    return redirect('/customer/list/')
