from django_filters import rest_framework as filters

from apps.worktable.models import WorkOrder, WorkOrderLog


class WorkOrderFilter(filters.FilterSet):
    u = filters.CharFilter(field_name='proposer__username', lookup_expr='icontains')
    d = filters.CharFilter(field_name='proposer__department__simple_title')

    class Meta:
        model = WorkOrder
        fields = ['u', 'd']
