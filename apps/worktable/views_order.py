from dateutil.relativedelta import relativedelta
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework import renderers, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from apps.utils.toolkit import build_order_num, order_record, action_menu
from apps.utils.mailer import send_work_order_message

from apps.worktable.models import WorkOrder, WorkOrderLog
from apps.users.models import Department

from apps.worktable.serializers import WorkOrderSerializer, WorkOrderListSerializer, WorkOrderLogSerializer
from apps.users.serializers import UserForSelectSerializer, DepartmentForSelectSerializer

from apps.worktable.permissions import IsOwnerOrReadOnly
from apps.worktable.filters import WorkOrderFilter

User = get_user_model()


"""
Here is WorkOrder Views
"""


class WorkOrderView(ModelViewSet):
    queryset = WorkOrder.objects.all().order_by("-id")
    serializer_class = WorkOrderListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = WorkOrderFilter

    renderer_classes = (renderers.TemplateHTMLRenderer, renderers.JSONRenderer)
    template_name = 'worktable/order/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 't' in self.request.GET and self.request.GET['t']:
            date = datetime.strptime(self.request.GET['t'], "%Y-%m")
            logs = WorkOrderLog.objects.filter(
                record_time__year=date.year,
                record_time__month=date.month
            ).values('record_obj').distinct()
            obj_id_list = [oid['record_obj'] for oid in logs]
            qs = qs.filter(id__in=obj_id_list)
        return qs

    def get(self, request, *args, **kwargs):
        work_order_log = WorkOrderLog.objects.filter(record_type='create').values('record_time').first()
        date_start = datetime.now()
        date_end = work_order_log['record_time']
        date_list = []
        while date_start > date_end:
            date_list.append(str(date_start.year) + '-' + str(date_start.month).zfill(2))
            date_start -= relativedelta(months=1)
        departments = DepartmentForSelectSerializer(Department.objects.values('id', 'simple_title'), many=True)
        results = {
            'departments': departments.data,
            'date_list': date_list,
        }

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            results['data'] = serializer.data
            return self.get_paginated_response(results)
        else:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            results['data'] = serializer.data
        return self.list(request, results)

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        delete_id = request.POST.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for i in delete_id.split(','):
            get_object_or_404(WorkOrder, pk=int(i)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkOrderCreateView(ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    renderer_classes = (renderers.TemplateHTMLRenderer, renderers.JSONRenderer)
    template_name = 'worktable/order/create.html'

    def get(self, *args, **kwargs):
        users = User.objects.all().exclude(Q(username='admin') | Q(email=''))
        users_serializer = UserForSelectSerializer(users, many=True)
        kwargs['users'] = users_serializer.data
        kwargs['types'] = WorkOrder.TYPES
        return Response(kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        form = {
            'num': build_order_num('A'),
            'proposer': User.objects.get(id=self.request.data['proposer_id']),
            'state': 'wait',
        }
        serializer.save(**form)
        order_record(recorder=form['proposer'], num=form['num'], record_type="create")
        # send_work_order_message(form['num'])


class WorkOrderDetailView(ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    lookup_field = 'num'

    renderer_classes = (renderers.TemplateHTMLRenderer, renderers.JSONRenderer)
    template_name = 'worktable/order/detail.html'

    record_type = None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logs = WorkOrderLogSerializer(WorkOrderLog.objects.filter(record_obj=instance.id).order_by('-id'), many=True)
        parameter = {
            'form_type': str(instance.num[0]),
            'current_user': self.request.user.id,
            'order_status': instance.state,
            'proposer': instance.proposer.id,
            'leader': ''
        }
        actions_list = action_menu(**parameter)

        ret = {
            'result': serializer.data,
            'types': WorkOrder.TYPES,
            'logs': logs.data,
            'actions_list': actions_list,
        }
        # print(json_dumps(serializer.data, sort_keys=True, indent=4, separators=(', ', ': ')))
        return Response(ret)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'action' in request.data:
            data = {'state': request.data['action']}
            self.record_type = request.data['action']
        else:
            data = request.data
            self.record_type = 'update'
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        # return Response(serializer.data)
        return HttpResponse(serializer.data, content_type='application/json')

    def perform_update(self, serializer):
        serializer.save()
        order_record(recorder=self.request.user, num=serializer.data['num'], record_type=self.record_type)
        # send_work_order_message(form['num'])