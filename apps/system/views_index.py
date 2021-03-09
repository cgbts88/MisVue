import re
import os
import json
import datetime

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View, TemplateView

from apps.system.models import FileUpload
from apps.system.forms import UploadForm
from apps.asset.models import NetworkDevice
from apps.users.models import PermitLog
from apps.users.forms import LoginForm
from apps.worktable.models import WorkOrderLog

from apps.utils.mixin import LoginRequiredMixin
from apps.utils.mailer import send_daily_job_excel

User = get_user_model()


class IndexView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        return render(request, 'main/index.html')


class SystemIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'


class LoginView(View):

    @staticmethod
    def get(request):
        user_ip = request.META.get('REMOTE_ADDR')
        redirect_to = request.GET.get('next', '/')
        try:
            network_obj = NetworkDevice.objects.get(ip=user_ip)
            user = User.objects.get(id=network_obj.asset_user_id)
            login(request, user)
            return HttpResponseRedirect(redirect_to)
        except ObjectDoesNotExist:
            pass
        if not request.user.is_authenticated:
            return render(request, 'main/login.html')
        else:
            return HttpResponseRedirect('/')

    @staticmethod
    def post(request):
        redirect_to = request.GET.get('next', '/')
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    ret['msg'] = '用户未激活！'
            else:
                ret['msg'] = '用户名或密码错误！'
        else:
            ret['msg'] = '用户和密码不能为空！'
        return render(request, 'main/login.html', ret)


class LogoutView(View):

    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class UploadView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        jump_url = ''
        jump_id = request.GET['id']
        if request.GET['previous'] == 'permit':
            jump_url = 'personnel:user-permit'
        ret = {
            'jump_url': jump_url,
            'jump_id': jump_id
        }
        return render(request, 'system/upload.html', ret)

    @staticmethod
    def post(request):
        res = dict(result='fail')
        if 'file' in request.FILES and request.FILES['file']:
            form = UploadForm(request.POST, request.FILES)
            file = str(request.FILES['file'])
            extension = os.path.splitext(file)[1]
            allow_ext = ['.pdf', '.jpg', '.gif', '.xls']
            if extension not in allow_ext:
                res['result'] = 'refuse'
            elif form.is_valid():
                form.save()
                upload = FileUpload.objects.last()
                log_record = {
                    'record_obj_id': request.POST['id'],
                    'recorder': request.user,
                    'record_type': 'upload',     # 上传
                    'remark': '<a href=' + settings.MEDIA_URL + str(upload.file) + '>附件</a>',
                }
                if request.POST['previous'] == 'permit':
                    PermitLog.objects.create(**log_record)
                res['result'] = 'success'
            else:
                pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
                form_errors = str(form.errors)
                errors = re.findall(pattern, form_errors)
                res['error'] = errors[0]
        return HttpResponse(json.dumps(res), content_type='application/json')


class ExportView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        work_order_log = WorkOrderLog.objects.filter(record_type='create').values('record_time').first()
        date_start = datetime.datetime.now()
        date_end = work_order_log['record_time']
        date_list = []
        while date_start > date_end:
            date_list.append(str(date_start.year) + '-' + str(date_start.month).zfill(2))
            date_start -= relativedelta(months=1)
        ret = {
            'date_list': date_list,
        }
        return render(request, 'system/export.html', ret)

    @staticmethod
    def post(request):
        res = dict(result=False)
        if 'date' in request.POST and request.POST['date']:
            send_daily_job_excel(request.POST['date'])
            res['result'] = True
            return HttpResponse(json.dumps(res), content_type='application/json')
