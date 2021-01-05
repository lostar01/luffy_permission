from django.template import Library
from luffy_permission import settings
from collections import OrderedDict
import re

register = Library()

@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    """
    创建一级菜单
    """
    menu_dict = request.session.get(settings.MEMU_LIST_SESSION_KEY)
    menu_list = []
    for v in menu_dict.values():
        for item in v['children']:
            menu_list.append(item)
    return {"menu_list": menu_list }

@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    创建一级菜单
    """
    menu_dict = request.session.get(settings.MEMU_LIST_SESSION_KEY)

    key_list = sorted(menu_dict)

    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for per in val['children']:
            regex = "^%s$" % (per['url'],)
            if re.match(regex, request.path_info):
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val
    return {
        'menu_dict': ordered_dict
    }