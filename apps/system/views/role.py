import json

from django.contrib.auth import get_user_model
from django.views.generic import View, ListView
from django.shortcuts import HttpResponse, get_object_or_404, render

from apps.system.models import Role, Menu
from apps.users.models import Department
from apps.utils.custom import BreadcrumbMixin, MisCreateView, MisUpdateView, MisDeleteView
from apps.utils.mixin import LoginRequiredMixin

User = get_user_model()


class RoleListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
    model = Role
    context_object_name = 'data_all'
    template_name = 'system/role/list.html'
    paginate_by = 20


class RoleCreateView(MisCreateView):
    model = Role
    fields = '__all__'
    template_name = 'system/role/create.html'


class RoleDetailView(MisUpdateView):
    model = Role
    fields = '__all__'
    template_name = 'system/role/detail.html'


class RoleDeleteView(MisDeleteView):
    model = Role
    success_url = 'system/role'


class Role2MenuView(LoginRequiredMixin, View):
    """
    角色绑定菜单
    """
    def get(self, request):
        fields = ['id', 'title', 'parent']
        if 'id' in request.GET and request.GET['id']:
            role = get_object_or_404(Role, pk=request.GET['id'])
            role_menus = role.permissions.values(*fields)
            menus = Menu.objects.all()
            parent_menu = Menu.objects.filter(parent=None).values(*fields)
            ret = {
                'role': role,
                'role_menus': role_menus,
                'menus': menus,
                'parent_menu': parent_menu,
            }
            return render(request, 'system/role/role2menu.html', ret)

    def post(self, request):
        res = dict(result=False)
        role = get_object_or_404(Role, pk=request.POST['id'])
        menu_checked_list = map(int, request.POST.getlist('menu_list', []))
        role.permissions.clear()
        for menu in menu_checked_list:
            menu_checked = get_object_or_404(Menu, pk=menu)
            role.permissions.add(menu_checked)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class Role2UserView(LoginRequiredMixin, View):
    """
    角色关联用户
    """

    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            role = get_object_or_404(Role, pk=request.GET['id'])
            role_users = role.userprofile_set.all()
            users = User.objects.all()
            departments = Department.objects.all()
            ret = {
                'role': role,
                'role_users': role_users,
                'users': users,
                'departments': departments,
            }
            return render(request, 'system/role/role2user.html', ret)

    def post(self, request):
        res = dict(result=False)
        role = get_object_or_404(Role, pk=request.POST['id'])
        user_checked_list = map(int, request.POST.getlist('user_list', []))
        role.userprofile_set.clear()
        for user in user_checked_list:
            user_checked = get_object_or_404(User, pk=user)
            role.userprofile_set.add(user_checked)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')
