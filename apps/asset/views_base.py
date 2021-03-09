from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, ListView

from apps.utils.custom import BreadcrumbMixin, MisCreateView, MisUpdateView, MisDeleteView, MisRelationView
from apps.utils.mixin import LoginRequiredMixin
from apps.asset.models import TypeCode, Attribute

User = get_user_model()


class AssetIndexView(LoginRequiredMixin, TemplateView):
	template_name = 'main/index.html'


"""
Here is TypeCode Views
"""


class TypeCodeListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
	model = TypeCode
	context_object_name = 'data_all'
	template_name = 'asset/typecode/list.html'
	paginate_by = 20


class TypeCodeCreateView(MisCreateView):
	model = TypeCode
	fields = '__all__'
	template_name = 'asset/typecode/create.html'


class TypeCodeDetailView(MisUpdateView):
	model = TypeCode
	fields = '__all__'
	template_name = 'asset/typecode/detail.html'


class TypeCodeRelationView(MisRelationView):
	model = TypeCode
	template_name = 'asset/typecode/relation.html'

	def get_context_data(self, **kwargs):
		kwargs['attributes'] = self.object.attribute_set.all()
		return super().get_context_data(**kwargs)


class TypeCodeDeleteView(MisDeleteView):
	model = TypeCode
	success_url = 'asset/typecode'


"""
Here is Attribute Views
"""


class AttributeListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
	model = Attribute
	context_object_name = 'data_all'
	template_name = 'asset/attribute/list.html'
	paginate_by = 20


class AttributeCreateView(MisCreateView):
	model = Attribute
	fields = '__all__'
	template_name = 'asset/attribute/create.html'

	def get_context_data(self, **kwargs):
		kwargs['typecodes'] = TypeCode.objects.values()
		return super().get_context_data(**kwargs)


class AttributeDetailView(MisUpdateView):
	model = Attribute
	fields = '__all__'
	template_name = 'asset/attribute/detail.html'

	def get_context_data(self, **kwargs):
		kwargs['typecodes'] = TypeCode.objects.values()
		return super().get_context_data(**kwargs)


class AttributeRelationView(MisRelationView):
	model = Attribute
	template_name = 'asset/attribute/relation.html'

	def get_context_data(self, **kwargs):
		kwargs['stocks'] = self.object.stock_set.all()
		return super().get_context_data(**kwargs)


class AttributeDeleteView(MisDeleteView):
	model = Attribute
	success_url = 'asset/attribute'
