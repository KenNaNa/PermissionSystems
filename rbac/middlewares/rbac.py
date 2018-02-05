from django.utils.deprecation import MiddlewareMixin
import re
from django.shortcuts import HttpResponse
from django.conf import settings

class RbacMiddleware(MiddlewareMixin):
    def process_request(self,request):

        # 1. 获取白名单，让白名单中的所有url和当前访问url匹配
        for reg in settings.PERMISSION_VALID_URL:
            if re.match(reg,request.path_info):
                return None

        # 2. 获取权限
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse('未获取到当前用户的权限信息，无法访问')

        """
        permission_dict={
            1：{
                'urls': ['/users/','/users/add/','/users/del/(\d+)/','/users/edit/(\d+)/'],
                'codes':['list','add','del','edit']
            },
            2：{
                'urls': ['/users/','/users/add/',],
                'codes':['list','add',]
            },
        
        }
        """
        flag = False
        # 3. 对用户请求的url进行匹配
        for value in permission_dict.values():
            urls = value['urls']
            codes = value['codes']
            for reg in urls:
                regx = "^%s$" % (reg,)
                if re.match(regx, request.path_info):
                    flag = True
                    break
            if flag:
                request.permission_codes = codes
                break

        if not flag:
            return HttpResponse('无权访问')
