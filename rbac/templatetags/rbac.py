from django.template import Library
from luffy_permission import settings

register = Library()

@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    """
    创建一级菜单
    """
    menu_list = request.session.get(settings.MEMU_LIST_SESSION_KEY)
    return {"menu_list": menu_list }