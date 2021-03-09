from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.users.models import Department, Location, Position
from apps.utils.custom import MisCreateView, MisUpdateView, MisDeleteView, MisRelationView, MisListView

User = get_user_model()


"""
Here is Department View：
"""


class DepartmentListView(MisListView):
    model = Department
    context_object_name = 'data_all'
    template_name = 'personnel/department/list.html'
    paginate_by = 20


class DepartmentCreateView(MisCreateView):
    model = Department
    fields = '__all__'
    template_name = 'personnel/department/create.html'

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.all().exclude(Q(username='admin') | Q())
        return super().get_context_data(**kwargs)


class DepartmentDetailView(MisUpdateView):
    model = Department
    fields = '__all__'
    template_name = 'personnel/department/detail.html'

    def get_context_data(self, **kwargs):
        kwargs['users'] = User.objects.all().exclude(Q(username='admin') |
                                                     ~Q(department__id=self.request.GET['id']))
        return super().get_context_data(**kwargs)


class DepartmentRelationView(MisRelationView):
    model = Department
    template_name = 'personnel/department/relation.html'

    def get_context_data(self, **kwargs):
        kwargs['users'] = self.object.userprofile_set.all()
        return super().get_context_data(**kwargs)


class DepartmentDeleteView(MisDeleteView):
    model = Department
    success_url = 'personnel/department'


"""
Here is Locations View：
"""


class LocationListView(MisListView):
    model = Location
    context_object_name = 'data_all'
    template_name = 'personnel/location/list.html'
    paginate_by = 20


class LocationCreateView(MisCreateView):
    model = Location
    fields = '__all__'
    template_name = 'personnel/location/create.html'


class LocationDetailView(MisUpdateView):
    model = Location
    fields = '__all__'
    template_name = 'personnel/location/detail.html'


class LocationRelationView(MisRelationView):
    model = Location
    template_name = 'personnel/location/relation.html'


class LocationDeleteView(MisDeleteView):
    model = Location
    success_url = 'personnel/location'


"""
Here is Position View：
"""


class PositionListView(MisListView):
    model = Position
    context_object_name = 'data_all'
    template_name = 'personnel/position/list.html'
    paginate_by = 20


class PositionCreateView(MisCreateView):
    model = Position
    fields = '__all__'
    template_name = 'personnel/position/create.html'


class PositionDetailView(MisUpdateView):
    model = Position
    fields = '__all__'
    template_name = 'personnel/position/detail.html'


class PositionRelationView(MisRelationView):
    model = Position
    template_name = 'personnel/position/relation.html'

    def get_context_data(self, **kwargs):
        kwargs['users'] = self.object.userprofile_set.all()
        return super().get_context_data(**kwargs)


class PositionDeleteView(MisDeleteView):
    model = Position
    success_url = 'personnel/position'
