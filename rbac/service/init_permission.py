from django.conf import settings


def init_permission(user,request):
    """
    获取当前用户权限信息，并放入到session中。
    :param user: rbac用户表的对象
    :param request:
    :return:
    """
    permission_list = user.roles.filter(permissions__title__isnull=False).values('permissions__id', # 权限ID
                                                                                 'permissions__title',  # 权限标题
                                                                                 'permissions__group_id', # 权限所在的组ID
                                                                                 'permissions__code', # 权限代号
                                                                                 'permissions__parent_id', # 组内菜单id
                                                                                 'permissions__group__menu_id', # 菜单id
                                                                                 'permissions__group__menu__title', # 菜单标题
                                                                                 'permissions__url').distinct()
    # 获取想要的数据，放入session，专门用于生成菜单
    menu_list = []
    for row in permission_list:
        temp = {
            'id':row['permissions__id'],
            'title':row['permissions__title'],
            'pid':row['permissions__parent_id'],
            'url':row['permissions__url'],
            'menu_id':row['permissions__group__menu_id'],
            'menu_title':row['permissions__group__menu__title'],
        }
        menu_list.append(temp)
    request.session[settings.MENU_SESSION_KEY] = menu_list



    # 用于做权限的验证
    permission_dict = {}
    for item in permission_list:
        group_id = item['permissions__group_id']
        if group_id in permission_dict:
            permission_dict[group_id]['urls'].append(item['permissions__url'])
            permission_dict[group_id]['codes'].append(item['permissions__code'])
        else:
            permission_dict[group_id] = {
                'urls': [item['permissions__url'], ],
                'codes': [item['permissions__code'], ]
            }

    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict