import json

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.shortcuts import HttpResponse, get_object_or_404
from django.urls import reverse_lazy

from apps.asset.models import Attribute, Stock, RecordLog
from apps.asset.forms import StockForm
from apps.users.models import Department

from apps.utils.custom import MisCreateView, MisUpdateView, MisDeleteView, MisListView, MisRelationView
from apps.utils.mixin import LoginRequiredMixin
from apps.utils.toolkit import form_to_remark, output_to_records
from apps.utils.util import form_invalid_msg

User = get_user_model()


"""
Here is Stock Views
"""


class StockListView(MisListView):
	model = Stock
	context_object_name = 'data_all'
	template_name = 'asset/stock/list.html'
	paginate_by = 20

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter().exclude(Q(state=2) | Q(state=3))


class StockCreateView(MisCreateView):
	model = Stock
	form_class = StockForm
	template_name = 'asset/stock/create.html'

	def get_context_data(self, **kwargs):
		kwargs['departments'] = Department.objects.values()
		kwargs['attributes'] = Attribute.objects.values()
		kwargs['stock_status'] = Stock.STATUS
		return super().get_context_data(**kwargs)

	def post(self, request, *args, **kwargs):
		res = dict(result=False)
		form = self.get_form()
		if form.is_valid():
			stock = Stock.objects.create(**form.cleaned_data)
			records = {
				'record_obj': stock,
				'recorder': request.user,
				'record_type': "create",
				'remark': form_to_remark(**form.cleaned_data),
			}
			RecordLog.objects.create(**records)
			res['result'] = True
		else:
			res = form_invalid_msg(form)
		return HttpResponse(json.dumps(res), content_type='application/json')


class StockDetailView(MisUpdateView):
	model = Stock
	fields = '__all__'
	template_name = 'asset/stock/detail.html'

	def get_context_data(self, **kwargs):
		kwargs['departments'] = Department.objects.values()
		kwargs['attributes'] = Attribute.objects.values()
		kwargs['stock_status'] = Stock.STATUS
		kwargs['records'] = output_to_records(self.object.id)
		return super().get_context_data(**kwargs)

	def post(self, request, *args, **kwargs):
		res = dict(result=False)
		form = self.get_form()
		if form.is_valid():
			Stock.objects.filter(id=request.POST['id']).update(**form.cleaned_data)
			records = {
				'record_obj': Stock.objects.get(id=request.POST['id']),
				'recorder': request.user,
				'record_type': "update",
				'remark': form_to_remark(**form.cleaned_data),
			}
			RecordLog.objects.create(**records)
			res['result'] = True
		else:
			res = form_invalid_msg(form)
		return HttpResponse(json.dumps(res), content_type='application/json')


class StockRelationView(MisRelationView):
	model = Stock
	fields = '__all__'
	template_name = 'asset/stock/relation.html'

	def get_context_data(self, **kwargs):
		kwargs['users'] = self.object.userprofile_set.all()
		return super().get_context_data(**kwargs)


class StockDeleteView(MisDeleteView):
	model = Stock
	success_url = reverse_lazy('asset:stock-list')


"""
Here is Scrap Views
"""


class ScrapListView(MisListView):
	model = Stock
	context_object_name = 'data_all'
	template_name = 'asset/scrap/list.html'
	paginate_by = 20

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(Q(state='disuse') | Q(state='scrap'))


class ScrapDetailView(MisUpdateView):
	model = Stock
	fields = '__all__'
	template_name = 'asset/scrap/detail.html'

	def get_context_data(self, **kwargs):
		kwargs['departments'] = Department.objects.values()
		kwargs['attributes'] = Attribute.objects.values()
		kwargs['stock_status'] = Stock.STATUS
		kwargs['records'] = output_to_records(self.object.id)
		return super().get_context_data(**kwargs)


class ScrapCancelView(LoginRequiredMixin, View):

	@staticmethod
	def post(request):
		res = dict(result=False)
		checked_list = map(int, request.POST.get('id').split(','))
		for item in checked_list:
			stock = get_object_or_404(Stock, pk=item)
			stock.state = 'free'    # 闲置
			stock.save()
			last_record_log = RecordLog.objects.filter(record_obj=stock).last()
			last_remark = eval(last_record_log.remark)
			last_remark['资产状态'] = '闲置'
			records = {
				'record_obj': stock,
				'recorder': request.user,
				'record_type': "update",
				'remark': last_remark,
			}
			RecordLog.objects.create(**records)
		res['result'] = True
		return HttpResponse(json.dumps(res), content_type='application/json')


class ScrapDoneView(LoginRequiredMixin, View):

	@staticmethod
	def post(request):
		res = dict(result=False)
		checked_list = map(int, request.POST.get('id').split(','))
		for item in checked_list:
			stock = get_object_or_404(Stock, pk=item)
			stock.state = 'scrap'    # 已报废
			stock.save()
			last_record_log = RecordLog.objects.filter(record_obj=stock).last()
			last_remark = eval(last_record_log.desc)
			last_remark['资产状态'] = '已报废'
			records = {
				'record_obj': stock,
				'recorder': request.user,
				'record_type': "scrap",
				'remark': last_remark,
			}
			RecordLog.objects.create(**records)
		res['result'] = True
		return HttpResponse(json.dumps(res), content_type='application/json')
