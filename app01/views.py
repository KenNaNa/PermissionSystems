from django.shortcuts import render, redirect
from app01 import models
from rbac.service.init_permission import init_permission


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user = models.User.objects.filter(user_info__name=user, user_info__password=pwd).first()
        if user:
            # 权限初始化
            init_permission(user.user_info, request)  # 注意此处的用户表对象是rbac用户表对象
            return redirect('/users/')
        return render(request, 'login.html')
