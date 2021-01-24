#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入时候出发执行
        :param request:
        :return:
        """

        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """
        current_url = request.path_info
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse('未获取到用户权限信息，请登录！')

        nav_bar_record = [{'title': '首页', 'url': '#'}]
        flag = False

        for url in permission_dict.values():
            reg = "^%s$" % url['permissions__url']

            if re.match(reg, current_url):

                flag = True
                request.current_selected_permission = url['pid'] or url['permissions__id']
                print(request.current_selected_permission,'====')
                if not url['pid']:
                    nav_bar_record.extend(
                        [{'title': url['permissions__title'], 'url': url['permissions__url'], "class": "active"}])
                else:
                    nav_bar_record.extend([
                        {'title': url['p_title'], 'url': url['p_url']},
                        {'title': url['permissions__title'], 'url': url['permissions__url'], "class": "active"}
                    ])
                request.nav_bar_record = nav_bar_record

                break

        if not flag:
            return HttpResponse('无权访问')
