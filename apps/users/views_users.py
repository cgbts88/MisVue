import json

from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponse, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib.auth.hashers import make_password
from django.views.generic import View
from apps.users.models import Department, Location, Position, Permit, PermitLog
from apps.users.forms import UserUpdateForm, PermitForm
from apps.system.models import Role

from apps.utils.custom import MisCreateView, MisUpdateView, MisDeleteView, MisListView, MisRelationView
from apps.utils.util import format_user_name, form_invalid_msg
from apps.utils.mixin import LoginRequiredMixin

User = get_user_model()


class UserIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'


class UsersListView(MisListView):
    model = User
    context_object_name = 'data_all'
    template_name = 'personnel/user/list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = self.model.objects.filter().exclude(username='admin').order_by('-id')
        if 'department' in self.request.GET and self.request.GET['department']:
            queryset = queryset.filter(department=self.request.GET['department'])
        if 'username' in self.request.GET and self.request.GET['username']:
            queryset = queryset.filter(username__contains=self.request.GET['username'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['departments'] = Department.objects.all()
        return super().get_context_data(**kwargs)


class UsersCreateView(MisCreateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'personnel/user/create.html'

    def get_context_data(self, **kwargs):
        kwargs['departments'] = Department.objects.values()
        kwargs['locations'] = Location.objects.values()
        kwargs['positions'] = Position.objects.values()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            rewrite_form = form.save(commit=False)
            rewrite_form.username, rewrite_form.en_name = format_user_name(form.cleaned_data['en_name'])
            rewrite_form.password = make_password("123456")
            rewrite_form.is_staff = 1
            rewrite_form.save()
            role = Role.objects.get(id=3)
            rewrite_form.roles.add(role)
            ret = {'result': 'success'}
        else:
            ret = form_invalid_msg(form)
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UsersDetailView(MisUpdateView):
    model = User
    context_object_name = 'data'
    form_class = UserUpdateForm
    template_name = 'personnel/user/detail.html'

    def get_context_data(self, **kwargs):
        kwargs['departments'] = Department.objects.values()
        kwargs['locations'] = Location.objects.values()
        kwargs['positions'] = Position.objects.values()
        kwargs['role'] = self.object.roles.get()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if 'id' in request.POST and request.POST['id']:
            form = self.form_class(request.POST, instance=User.objects.get(id=request.POST['id']))
            if form.is_valid():
                rewrite_form = form.save(commit=False)
                rewrite_form.username, rewrite_form.en_name = format_user_name(form.cleaned_data['en_name'])
                rewrite_form.save()
                ret = {'result': 'success'}
            else:
                ret = form_invalid_msg(form)
            return HttpResponse(json.dumps(ret), content_type='application/json')


class UsersDeleteView(MisDeleteView):
    model = User
    success_url = 'personnel/user'


class UsersActiveView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            queryset = get_object_or_404(User, pk=request.POST['id'])
            if queryset.is_active:
                User.objects.filter(id=request.POST['id']).update(is_active=False)
            else:
                User.objects.filter(id=request.POST['id']).update(is_active=True)
            res['result'] = True
            return HttpResponse(json.dumps(res), content_type='application/json')


class UsersResetView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            User.objects.filter(id=request.POST['id']).update(password=make_password('123456'))
            res['result'] = True
            return HttpResponse(json.dumps(res), content_type='application/json')


class UsersPermitView(MisUpdateView):
    model = User
    template_name = 'personnel/user/permit.html'

    def get_context_data(self, **kwargs):
        fields = ['id', 'title']
        user_permits = self.object.permits.values(*fields)
        kwargs['user_permits'] = user_permits
        kwargs['permits_checked'] = [permit['id'] for permit in user_permits]
        kwargs['records'] = PermitLog.objects.filter(record_obj_id=self.request.GET['id'])
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        user = self.object
        permits_checked_list = map(int, request.POST.getlist('permit_list', []))
        user.permits.clear()
        for permit in permits_checked_list:
            permit_checked = get_object_or_404(Permit, pk=permit)
            user.permits.add(permit_checked)
        log_record = {
            'record_obj_id': request.POST['id'],
            'recorder': request.user,
            'record_type': 'update',  # 修改
            'remark': '',
        }
        PermitLog.objects.create(**log_record)
        res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


"""
Here is Permit Views
"""


class PermitListView(MisListView):
    model = Permit
    context_object_name = 'data_all'
    template_name = 'personnel/permit/list.html'
    paginate_by = 10


class PermitCreateView(MisCreateView):
    model = Permit
    fields = '__all__'
    template_name = 'personnel/permit/create.html'


class PermitDeleteView(MisDeleteView):
    model = Permit
    success_url = 'personnel/permit'


class PermitDetailView(MisUpdateView):
    model = Permit
    form_class = PermitForm
    template_name = 'personnel/permit/detail.html'


class PermitRelationView(MisRelationView):
    model = Permit
    template_name = 'personnel/permit/relation.html'
