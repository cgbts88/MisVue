import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponse

from apps.asset.models import Stock, NetworkDevice, OtherDevice, AssetOrder, RecordLog
from apps.asset.forms import NetworkDeviceForm, OtherDeviceForm
from apps.users.models import Department

from apps.utils.custom import MisCreateView, MisUpdateView, MisDeleteView, MisRelationView, MisListView
from apps.utils.toolkit import build_order_num
from apps.utils.mailer import send_asset_order_message
from apps.utils.util import form_invalid_msg

User = get_user_model()


"""
Here is NetworkDevice Views
"""


class NetworkDeviceListView(MisListView):
	model = NetworkDevice
	context_object_name = 'data_all'
	template_name = 'asset/networkdevice/list.html'
	paginate_by = 20

	def get_queryset(self):
		queryset = self.model.objects.filter().exclude(Q(asset_user__username='admin') | Q())
		if 'department' in self.request.GET and self.request.GET['department']:
			queryset = queryset.filter(asset_user__department=self.request.GET['department'])
		if 'username' in self.request.GET and self.request.GET['username']:
			queryset = queryset.filter(asset_user__username__contains=self.request.GET['username'])
		if 'ip' in self.request.GET and self.request.GET['ip']:
			try:
				queryset = queryset.filter(ip=self.request.GET['ip'])
			except ObjectDoesNotExist:
				pass
		return queryset

	def get_context_data(self, *, object_list=None, **kwargs):
		kwargs['departments'] = Department.objects.all()
		return super().get_context_data(**kwargs)


class NetworkDeviceCreateView(MisCreateView):
	model = NetworkDevice
	form_class = NetworkDeviceForm
	template_name = 'asset/networkdevice/create.html'

	def get_context_data(self, **kwargs):
		kwargs['devices'] = Stock.objects.filter(
			Q(model__is_network=True) &
			Q(department_id=self.request.user.department.id) &
			~Q(id__in=NetworkDevice.objects.values('stock'))
		)
		user_roles_id_list = [roles['id'] for roles in self.request.user.roles.values('id')]
		if 1 in user_roles_id_list or 2 in user_roles_id_list:
			kwargs['users'] = User.objects.all()
		else:
			kwargs['users'] = User.objects.filter(department=self.request.user.department).exclude(username='admin')
		return super().get_context_data(**kwargs)


class NetworkDeviceDetailView(MisUpdateView):
	model = NetworkDevice
	form_class = NetworkDeviceForm
	template_name = 'asset/networkdevice/detail.html'

	def get_context_data(self, **kwargs):
		kwargs['networkdevice'] = self.object
		kwargs['devices'] = Stock.objects.filter(
			Q(model__is_network=True) &
			Q(department_id=self.request.user.department.id) &
			~Q(id__in=NetworkDevice.objects.filter(stock__isnull=False).values('stock'))
		)
		user_roles_id_list = [roles['id'] for roles in self.request.user.roles.values('id')]
		if 1 in user_roles_id_list or 2 in user_roles_id_list:
			kwargs['users'] = User.objects.all().order_by('username')
		else:
			kwargs['users'] = User.objects.filter(
				department=self.request.user.department).exclude(username='admin').order_by('username')
		return super().get_context_data(**kwargs)


class NetworkDeviceDeleteView(MisDeleteView):
	model = NetworkDevice
	success_url = 'asset/networkdevice'


class NetworkDeviceRelationView(MisRelationView):
	model = Stock
	fields = '__all__'
	template_name = 'asset/networkdevice/relation.html'

	def get_context_data(self, **kwargs):
		kwargs['users'] = self.object.userprofile_set.all()
		return super().get_context_data(**kwargs)


"""
Here is OtherDevice Views
"""


class OtherDeviceListView(MisListView):
	model = OtherDevice
	context_object_name = 'data_all'
	template_name = 'asset/otherdevice/list.html'
	paginate_by = 20


class OtherDeviceCreateView(MisCreateView):
	model = Stock
	form_class = OtherDeviceForm
	template_name = 'asset/otherdevice/create.html'

	def get_context_data(self, **kwargs):
		kwargs['devices'] = self.model.objects.filter(
			Q(model__is_network=False) &
			Q(department_id=self.request.user.department.id) &
			~Q(id__in=OtherDevice.objects.filter(stock__isnull=False).values('stock'))
		)
		kwargs['users'] = User.objects.filter(department=self.request.user.department)
		return super().get_context_data(**kwargs)


class OtherDeviceDetailView(MisUpdateView):
	model = OtherDevice
	fields = '__all__'
	template_name = 'asset/otherdevice/detail.html'

	def get_context_data(self, **kwargs):
		kwargs['otherdevice'] = self.object
		kwargs['devices'] = Stock.objects.filter(
			Q(model__is_network=False) &
			Q(department_id=self.request.user.department.id) &
			~Q(id__in=OtherDevice.objects.filter(stock__isnull=False).values('stock'))
		)
		kwargs['users'] = User.objects.all()
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		stock = Stock.objects.get(id=form['stock']).update(state=1)
		last_record_log = RecordLog.objects.filter(record_obj=stock).last()
		last_desc = eval(last_record_log.desc)
		last_desc['资产状态'] = '在用'
		records = {
			'record_obj': stock,
			'recorder': self.request.user,
			'record_type': "1",
			'desc': last_desc,
		}
		RecordLog.objects.create(**records)
		return super().form_valid(form)


class OtherDeviceRelationView(MisRelationView):
	model = Stock
	fields = '__all__'
	template_name = 'asset/otherdevice/relation.html'

	def get_context_data(self, **kwargs):
		kwargs['users'] = self.object.userprofile_set.all()
		return super().get_context_data(**kwargs)


class OtherDeviceDeleteView(MisDeleteView):
	model = OtherDevice
	success_url = 'asset/otherdevice'


"""
Here is Order Views
"""


class AssetOrderListView(MisListView):
	model = AssetOrder
	context_object_name = 'data_all'
	template_name = 'asset/order/list.html'
	paginate_by = 20


class AssetOrderSelectView(MisListView):
	model = Department
	context_object_name = 'data_all'
	template_name = 'asset/order/select.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.exclude(id=4)


class AssetOrderCreateView(MisCreateView):
	model = AssetOrder
	fields = '__all__'
	template_name = 'asset/order/create.html'

	def get_context_data(self, **kwargs):
		target_department = self.request.GET['department']
		kwargs['edp_devices'] = Stock.objects.filter(department__simple_title='EDP').order_by('id')
		kwargs['target_department'] = target_department
		kwargs['target_devices'] = Stock.objects.filter(department__simple_title=target_department).order_by('id')
		return super().get_context_data(**kwargs)

	def post(self, request, *args, **kwargs):
		res = dict(result=False)
		form = self.get_form()
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.num = build_order_num('C')
			try:
				edp_asset = Stock.objects.filter(id__in=request.POST.getlist('edp_asset', []))
				edp_asset.update(department=request.POST['target_department'])
				for obj in edp_asset:
					last_record_log = RecordLog.objects.filter(record_obj=obj).last()
					last_remark = eval(last_record_log.remark)
					last_remark['库存部门'] = request.POST['target_department']
					records = {
						'record_obj': obj,
						'recorder': request.user,
						'record_type': "transfer",
						'remark': last_remark,
					}
					RecordLog.objects.create(**records)
				new_form.edp_asset = ','.join(item.edp_num for item in edp_asset)
			except ObjectDoesNotExist:
				pass
			try:
				target_asset = Stock.objects.filter(id__in=request.POST.getlist('target_asset', []))
				target_asset.update(department='EDP')
				for obj in target_asset:
					last_record_log = RecordLog.objects.filter(record_obj=obj).last()
					last_remark = eval(last_record_log.remark)
					last_remark['库存部门'] = 'EDP'
					records = {
						'record_obj': obj,
						'recorder': request.user,
						'record_type': "transfer",
						'remark': last_remark,
					}
					RecordLog.objects.create(**records)
				new_form.target_asset = ','.join(item.edp_num for item in target_asset)
			except ObjectDoesNotExist:
				pass
			new_form.save()
			send_asset_order_message(new_form.num)
			res['result'] = True
		else:
			res = form_invalid_msg(form)
		return HttpResponse(json.dumps(res), content_type='application/json')


class AssetOrderDeleteView(MisDeleteView):
	model = AssetOrder
	success_url = 'asset/order'
