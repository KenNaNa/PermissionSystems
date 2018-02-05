import re
from django.template import Library
from django.conf import settings

register = Library()

@register.simple_tag
def func(a1,a2):
    """
    函数返回什么，页面就能填充什么
    :param a1:
    :param a2:
    :return:
    """
    return a1 + a2

@register.inclusion_tag('rbac/rbac_menu.html')
def menu(request):
    current_url = request.path_info

    menu_list = request.session[settings.MENU_SESSION_KEY]

    menu_dict = {}
    for item in menu_list:
        pid = item['pid']
        if not pid:
            item['active'] = False
            menu_dict[item['id']] = item

    for item in menu_list:
        pid = item['pid']
        url = "^%s$" % item['url']
        if re.match(url, current_url):
            if pid:
                menu_dict[pid]['active'] = True
            else:
                item['active'] = True

    menu_result = {}
    for item in menu_dict.values():
        menu_id = item['menu_id']
        if menu_id in menu_result:
            temp = {'title': item['title'], 'url': item['url'], 'active': item['active']}
            menu_result[menu_id]['children'].append(temp)
            if item['active']:
                menu_result[menu_id]['active'] = True
        else:
            menu_result[menu_id] = {
                'title': item['menu_title'],
                'active': item['active'],
                'children': [
                    {'title': item['title'], 'url': item['url'], 'active': item['active']}
                ]
            }


    return {'menu_result':menu_result}





