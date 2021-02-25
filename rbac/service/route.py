import re
from collections import OrderedDict
from django.conf import settings
from django.urls import URLPattern, URLResolver
from django.utils.module_loading import import_string

def check_url_exclude(url):
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex,url):
            return True


def recursion_urls(pre_namespace,pre_url,urlpatterns,url_order_dict):
    """
    通过递归获取URL
    """
    for item in urlpatterns:
        if isinstance(item,URLPattern):   #非路由转发，将路由添加到url_ordered_dict
            if not item.name:
                continue

            if pre_namespace:
                name = "%s:%s" %(pre_namespace,item.name)
            else:
                name = item.name

            url = pre_url + str(item.pattern)

            url = url.replace('^','').replace('$','')
            if check_url_exclude(url):
                continue
            url_order_dict[name] = {'url_name':name,'url':url}

        elif isinstance(item,URLResolver): #路由转发 , 递归操作
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" %(pre_namespace,item.namespace)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + str(item.pattern), item.url_patterns, url_order_dict)
    return url_order_dict


def get_all_url_dict():
    # 获取项目中所有的URL
    url_order_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)  # from luffy... import urls
    # print(md.urlpatterns)
    return recursion_urls(None,'/',md.urlpatterns,url_order_dict)
