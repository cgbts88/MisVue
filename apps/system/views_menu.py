from django.views.generic import ListView

from apps.system.models import Menu
from apps.utils.custom import MisCreateView, MisUpdateView, MisDeleteView
from apps.utils.mixin import LoginRequiredMixin


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = 'data_all'
    template_name = 'system/menu/list.html'
    paginate_by = 20


class MenuCreateView(MisCreateView):
    model = Menu
    fields = '__all__'
    template_name = 'system/menu/create.html'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)


class MenuDetailView(MisUpdateView):
    model = Menu
    fields = '__all__'
    template_name = 'system/menu/detail.html'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)


class MenuDeleteView(MisDeleteView):
    model = Menu
    success_url = 'system/menu'
