from django.http import QueryDict
from django.urls import reverse

def memory_url(request,name,*args,**kwargs):
    """
    生成带搜索条件的URL
    """
    basic_url = reverse(name,args=args,kwargs=kwargs)

    #当前URL 无参数
    if not request.GET:
        return basic_url

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()  #把URL参数复制

    return '%s?%s' %(basic_url,query_dict.urlencode())


def memory_reverse(request,name,*args,**kwargs):
    url = reverse(name,args=args,kwargs=kwargs)
    orgin_params = request.GET.get('_filter')
    if orgin_params:
        url = '%s?%s' % (url, orgin_params)

    return url