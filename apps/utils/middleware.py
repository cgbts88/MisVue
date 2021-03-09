import re

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import render


class MenuCollection(MiddlewareMixin):
    """
    菜单中间件
    1. get_user 请求获取 user 信息
    2. get_menu_from_role 根据 user 获取 role 所拥有的 menu 对象
        .distinct() 去除重复
    3. get_permission_url 根据 get_menu_from_role 函数整理出 permission_url_list
    4. get_permission_menu 根据 get_menu_from_role 函数整理出 permission_menu_list
    5. get_top_reveal_menu 根据 request.path_info获取当前路径，
        判断 permission_menu_list 否为当前路径，如果是则设 status:True，
        判断菜单是否还有上级菜单，如果没有则插入到最前,如果有上级菜单就加入 sub_menu 附属菜单

    """
    @staticmethod
    def get_user(request):
        return request.user

    def get_menu_from_role(self, request, user=None):
        if user is None:
            user = self.get_user(request)
        try:
            menus = user.roles.values(
                'permissions__sort_number',
                'permissions__id',
                'permissions__title',
                'permissions__url',
                'permissions__code',
                'permissions__parent',
            ).distinct()
            return [menu for menu in menus if menu['permissions__id'] is not None]
        except AttributeError:
            return None

    def get_permission_url(self, request):
        role_menus = self.get_menu_from_role(request)
        if role_menus is not None:
            permission_url_list = [menu['permissions__url'] for menu in role_menus]
            return permission_url_list

    def get_permission_menu(self, request):
        permission_menu_list = []
        role_menus = self.get_menu_from_role(request)
        if role_menus is not None:
            for item in role_menus:
                menu = {
                    'sort_number': item['permissions__sort_number'],
                    'id': item['permissions__id'],
                    'title': item['permissions__title'],
                    'url': item['permissions__url'],
                    'code': item['permissions__code'],
                    'parent': item['permissions__parent'],
                    'status': False,
                    'sub_menu': [],
                }
                permission_menu_list.append(menu)
            return permission_menu_list

    def get_top_reveal_menu(self, request):
        top_menu = []
        permission_menu_dict = {}
        request_url = request.path_info
        permission_menu_list = self.get_permission_menu(request)
        if permission_menu_list is not None:
            for menu in permission_menu_list:
                url = menu['url']
                if url and re.match(url, request_url):
                    menu['status'] = True
                if menu['parent'] is None:
                    top_menu.insert(0, menu)
                permission_menu_dict[menu['id']] = menu

            menu_data = []
            for i in permission_menu_dict:
                if permission_menu_dict[i]['parent']:
                    pid = permission_menu_dict[i]['parent']
                    parent_menu = permission_menu_dict[pid]
                    parent_menu['sub_menu'].append(permission_menu_dict[i])
                else:
                    menu_data.append(permission_menu_dict[i])
            if [menu['sub_menu'] for menu in menu_data if menu['url'] in request_url]:
                reveal_menu = [menu['sub_menu'] for menu in menu_data if menu['url'] in request_url][0]
            else:
                reveal_menu = None
            return top_menu, reveal_menu

    def process_request(self, request):
        if self.get_top_reveal_menu(request):
            request.top_menu, request.reveal_menu = self.get_top_reveal_menu(request)
            request.permission_url_list = self.get_permission_url(request)


class ActionMiddleware(MiddlewareMixin):
    """
    动作中间件
    """

    @staticmethod
    def get_user(request):
        return request.user

    def get_permission_url(self, request, user=None):
        if user is None:
            user = self.get_user(request)
        try:
            menus = user.roles.values('permissions__url',).distinct()
            permission_url_list = [menu['permissions__url'] for menu in menus]
            return permission_url_list
        except AttributeError:
            return None

    def get_action_menu(self, request):
        actions = ['create', 'instead', 'delete', 'done', 'cancel', 'detail',
                   'role2user', 'role2menu', 'permit', 'reset', 'active', 'relation']
        action_list = []
        request_url = request.path_info
        permission_menu_list = self.get_permission_url(request)
        if permission_menu_list is not None and request_url != '/':
            for menu in permission_menu_list:
                if menu and re.match(request_url, menu) and menu.split('/')[-2] in actions \
                        and request_url.split('/')[2] == menu.split('/')[2]:
                    action_list.append(menu.split('/')[-2])
            return action_list

    def process_request(self, request):
        if self.get_action_menu(request):
            request.action_list = self.get_action_menu(request)


class RbacMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if hasattr(request, 'permission_url_list'):
            request_url = request.path_info
            permission_url = request.permission_url_list
            for url in settings.SAFE_URL:
                if re.match(url, request_url):
                    return None
            if request_url in permission_url:
                return None
            else:
                return render(request, 'main/page404.html')
