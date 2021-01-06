#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf import settings


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user: 当前用户对象
    :param request: 请求相关所有数据
    :return:
    """
    # 2. 权限信息初始化
    # 根据当前用户信息获取此用户所拥有的所有权限，并放入session。
    # 当前用户所有权限
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__title",
                                                                                      "permissions__icon",
                                                                                      "permissions__url",
                                                                                      "permissions__url_name",
                                                                                      "permissions__pid_id",
                                                                                      "permissions__pid__title",
                                                                                      "permissions__pid__url",
                                                                                      "permissions__menu_id",
                                                                                      "permissions__menu__title",
                                                                                      "permissions__menu__icon"
                                                                                      ).distinct()
    # menu_obj = Menu.objects.all()
    # 获取权限中所有的URL
    # permission_list = []
    # for item in permission_queryset:
    #     permission_list.append(item['permissions__url'])

    # permission_list = [item['permissions__url'] for item in permission_queryset]

    # 获取权限中的菜单
    menu_dict = {}
    permission_dict = {}
    # for menu in menu_obj:
    #     temp_menu_dict = {
    #         'title': menu.title,
    #         'icon': menu.icon,
    #     }
    #     child_list = []
    #     for item in permission_queryset:
    #
    #         permission_list.append(item['permissions__url'])
    #         if item['permissions__menu']:
    #             if menu.id == item['permissions__menu']:
    #                 tmp_child_dict = {
    #                     'title': item['permissions__title'],
    #                     'url': item['permissions__url']
    #                 }
    #                 child_list.append(tmp_child_dict)
    #
    #     temp_menu_dict['children'] = child_list
    #
    #     menu_dict[menu.id] = temp_menu_dict

    for item in permission_queryset:
        permission_dict[item['permissions__url_name']] = {'permissions__id': item['permissions__id'],
                                                          'permissions__title': item['permissions__title'],
                                                          'permissions__url': item['permissions__url'],
                                                          'pid': item['permissions__pid_id'],
                                                          'p_title': item['permissions__pid__title'],
                                                          'p_url': item['permissions__pid__url']
                                                          }

        memu_id = item['permissions__menu_id']
        if not memu_id:
            continue
        node = {'title': item['permissions__title'], 'url': item['permissions__url'], 'icon': item['permissions__icon'],
                'id': item['permissions__id']}
        if memu_id in menu_dict:
            menu_dict[memu_id]['children'].append(node)
        else:
            menu_dict[memu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node, ]
            }
    print(menu_dict)

    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MEMU_LIST_SESSION_KEY] = menu_dict
