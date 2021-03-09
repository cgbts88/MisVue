import re
import json
from datetime import datetime

from django.views.generic import CreateView, UpdateView, ListView, View, DetailView
from django.shortcuts import HttpResponse
from django.http import Http404, JsonResponse
from django.db.models.query import QuerySet
from django.core.exceptions import ImproperlyConfigured

from apps.system.models import Menu
from apps.utils.mixin import LoginRequiredMixin


class BreadcrumbMixin:

    def get_context_data(self, **kwargs):
        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            kwargs.update(menu)
        return super().get_context_data(**kwargs)


class MisGetObjectMixin:

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()
        if 'id' in self.request.GET and self.request.GET['id']:
            queryset = queryset.filter(id=int(self.request.GET['id']))
        elif 'id' in self.request.POST and self.request.POST['id']:
            queryset = queryset.filter(id=int(self.request.POST['id']))
        elif 'num' in self.request.GET and self.request.GET['num']:
            queryset = queryset.filter(num=self.request.GET['num'])
        else:
            raise AttributeError("Generic detail view %s must be called with id or num." %
                                 self.__class__.__name__)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class MisMultipleObjectMixin:

    filters = {}
    fields = []
    queryset = None
    model = None

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet.Define "
                "%(cls)s.model, %(cls)s.queryset."
                "{'cls':self.__class__.__name__"
            )
        return queryset

    def get_filters(self):
        return self.filters

    def get_fields(self):
        return self.fields


class MisEditViewMixin:

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        form = self.get_form()
        if form.is_valid():
            form.save()
            res['result'] = True
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            # print(form.errors)
            form_errors = str(form.errors)
            errors = re.findall(pattern, form_errors)
            res['error'] = errors[0]
        return HttpResponse(json.dumps(res), content_type='application/json')


class MisListView(LoginRequiredMixin, MisMultipleObjectMixin, ListView):
    """
    JsonResponse some json of objects, set by 'self.model' or 'self.queryset'.
    """


class MisOrderListView(LoginRequiredMixin, MisMultipleObjectMixin, ListView):
    """
    JsonResponse some json of objects, set by 'self.model' or 'self.queryset'.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        propose_queryset = queryset.filter(record_type='create').order_by('-id')
        data_all = []

        user_roles_id_list = [roles['id'] for roles in self.request.user.roles.values('id')]
        if 1 not in user_roles_id_list and 2 not in user_roles_id_list:
            propose_queryset = propose_queryset.filter(recorder_id=self.request.user.id)

        if 'department' in self.request.GET and self.request.GET['department']:
            propose_queryset = propose_queryset.filter(recorder__department=self.request.GET['department'])
        if 'username' in self.request.GET and self.request.GET['username']:
            propose_queryset = propose_queryset.filter(recorder__username__contains=self.request.GET['username'])
        if 'date' in self.request.GET and self.request.GET['date']:
            date = datetime.strptime(self.request.GET['date'], "%Y-%m")
            propose_queryset = propose_queryset.filter(record_time__year=date.year, record_time__month=date.month)

        for item in propose_queryset:
            obj_type = ''
            obj_content = ''
            form_type = item.record_obj.num[0]
            if form_type == 'A':
                obj_content = item.record_obj.format_content
                obj_type = item.record_obj.get_type_display
            # elif form_type == 'B':
                # permits = PermitFile.objects.filter(num=item.record_obj.id).values('permit__title')
                # for i in permits:
                    # obj_content += i['permit__title'] + '　'
            data_dict = {
                'id': item.record_obj.id,
                'num': item.record_obj,
                'propose_time': item.record_time,
                'proposer': item.record_obj.proposer,
                'content': obj_content,
                'state': item.record_obj.get_state_display,
                'type': obj_type,
            }
            try:
                process_record = queryset.filter(record_obj=item.record_obj, record_type='process').last()
                data_dict['processor'] = process_record.recorder
                data_dict['process_time'] = process_record.record_time
            except AttributeError:
                pass
            data_all.append(data_dict)
        return data_all


class MisCreateView(LoginRequiredMixin, MisEditViewMixin, CreateView):
    """
    View For create an object, with a response rendered by a template.
    Returns information with Json when the data is created successfully or fails.
    """


class MisUpdateView(LoginRequiredMixin, MisEditViewMixin, MisGetObjectMixin, UpdateView):
    """
    View for updating an object, with a response rendered by a template.
    """
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class MisDeleteView(LoginRequiredMixin, MisMultipleObjectMixin, View):

    def post(self, request):
        context = dict(result=False)
        queryset = self.get_queryset()
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            queryset.filter(id__in=id_list).delete()
            context['result'] = True
        else:
            raise AttributeError('Delete View %s must be called with id.' %
                                 self.__class__.__name__)
        return JsonResponse(context)


class MisRelationView(LoginRequiredMixin, MisGetObjectMixin, DetailView):
    """
    View For Relation an object, with a response rendered by a template.
    Returns information with Json when the data successfully or fails.
    """


class MisListView(LoginRequiredMixin, ListView):
    """
    View For Relation an object, with a response rendered by a template.
    Returns information with Json when the data successfully or fails.
    """