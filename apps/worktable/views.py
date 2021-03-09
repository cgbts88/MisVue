import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import HttpResponse

from apps.users.models import UserProfile, Department, Location, Position
from apps.users.forms import UserCenterForm, SelfPasswordChangeForm
from apps.asset.models import NetworkDevice

from apps.utils.custom import MisUpdateView, MisListView
from apps.utils.mixin import LoginRequiredMixin
from apps.utils.util import form_invalid_msg

User = get_user_model()


class WorktableIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'


class PhoneBookView(MisListView):
    model = UserProfile
    context_object_name = 'data_all'
    template_name = 'worktable/phonebook.html'
    paginate_by = 25

    def get_queryset(self):
        fields = ['id', 'ext_num', 'email', 'department__simple_title', 'location__area']
        queryset = self.model.objects.filter().values(*fields).exclude(
            Q(ext_num=0) |
            Q(username='admin') |
            Q(is_active=False)
            )
        '''
        由于IP不在同一个查询当中
        for keyword in self.request.GET.items():
            if keyword[1]:
                queryset = queryset.filter(**{keyword[0]:keyword[1]})
        '''
        if 'department' in self.request.GET and self.request.GET['department']:
            queryset = queryset.filter(department=self.request.GET['department'])
        if 'username' in self.request.GET and self.request.GET['username']:
            queryset = queryset.filter(username__contains=self.request.GET['username'])
        if 'ext_num' in self.request.GET and self.request.GET['ext_num']:
            queryset = queryset.filter(ext_num=self.request.GET['ext_num'])
        if 'ip' in self.request.GET and self.request.GET['ip']:
            try:
                ip_obj = NetworkDevice.objects.get(ip=self.request.GET['ip'])
                queryset = queryset.filter(id=ip_obj.asset_user_id)
            except ObjectDoesNotExist:
                pass
        for qs in queryset:
            try:
                network = NetworkDevice.objects.filter(asset_user=qs['id'])
                ip = ' / '.join([item.ip for item in network])
            except TypeError:
                ip = ""
            qs.update(name=self.model.objects.get(id=qs['id']))
            qs.update(ip=ip)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['departments'] = Department.objects.all()
        return super().get_context_data(**kwargs)


class NoticeCenterView(View):
    @staticmethod
    def get(request):

        # 系统信息
        ret = {}
        return render(request, 'worktable/notice.html', ret)


class PersonCenterView(MisUpdateView):
    model = UserProfile
    form_class = UserCenterForm
    context_object_name = 'data'
    template_name = 'worktable/person.html'

    def get_object(self, queryset=None):
        return self.get_queryset().get(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        kwargs['departments'] = Department.objects.all()
        kwargs['locations'] = Location.objects.all()
        kwargs['positions'] = Position.objects.all()
        kwargs['role'] = self.object.roles.get()
        return super().get_context_data(**kwargs)


class PersonPasswordChangeView(MisUpdateView):
    model = User
    form_class = SelfPasswordChangeForm
    template_name = 'worktable/passwordchange.html'

    def post(self, request, *args, **kwargs):
        user = self.object
        form = self.form_class(request.POST)
        if form.is_valid():
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            res = {'result': 'success'}
        else:
            res = form_invalid_msg(form)
        return HttpResponse(json.dumps(res), content_type='application/json')
