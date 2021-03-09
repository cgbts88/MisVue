from datetime import date
from django.contrib.auth import get_user_model

from apps.asset.models import Stock, RecordLog, Attribute, AssetOrder
from apps.users.models import Department
from apps.worktable.models import WorkOrder, WorkOrderLog

User = get_user_model()


def build_order_num(prefix):
	today_array = date.today().strftime('%Y%m%d')
	s_num = "1"
	num = ""
	filters_num = ""
	for num in range(1, 99):
		num = prefix + '-' + today_array + s_num.zfill(2)
		if prefix == "A":
			filters_num = WorkOrder.objects.filter(num=num)
		# elif prefix == "B":
			# filters_num = StockOrder.objects.filter(num=num)
		elif prefix == "C":
			filters_num = AssetOrder.objects.filter(num=num)
		if len(filters_num):
			n_num = int(s_num)
			s_num = str(n_num + 1)
		else:
			break
	return num


def form_to_remark(**form):
	"""
	将表单的内容格式化为记录的备注
	"""
	try:
		form['model'] = form['model'].brand + ' ' + form['model'].model
	except KeyError:
		attribute = Attribute.objects.get(id=form['model_id'])
		form['model'] = attribute.brand + ' ' + attribute.model
	if form['buy_date']:
		try:
			date.strftime(form['buy_date'], '%Y-%m-%d')
			form['buy_date'] = date.strftime(form['buy_date'], '%Y-%m-%d')
		except TypeError:
			pass
	if form['warranty_date']:
		try:
			date.strftime(form['warranty_date'], '%Y-%m-%d')
			form['warranty_date'] = date.strftime(form['warranty_date'], '%Y-%m-%d')
		except TypeError:
			pass
	if form['state']:
		for stock_status in Stock.STATUS:
			if str(form['state']) == stock_status[0]:
				form['state'] = stock_status[1]
	try:
		form['department'] = form['department']
	except KeyError:
		department = Department.objects.get(id=form['department_id'])
		form['department'] = department.simple_title

	remark = dict()
	"""
	访问类的受保护成员 _meta 还是有问题
	from django.apps import apps
	model_obj = apps.get_model(apps.asset, Stock)
	fields = model_obj._meta.fields
	"""
	fields = Stock._meta.fields
	for key, value in form.items():
		for field in fields:
			if field.name == key and field.name != 'id':
				remark[field.verbose_name] = (str(value) if value else '')
	return remark


def output_to_records(record_obj_id):
	"""
	格式化输出记录日志
	"""

	records = RecordLog.objects.filter(record_obj=record_obj_id)
	previous_record = ''
	ret = []
	for i, record in enumerate(records):
		record_type = ''
		for record_log_type in RecordLog.TYPES:
			if record_log_type[0] == record.record_type:
				record_type = record_log_type[1]

		current_record = record.remark
		remark = dict()
		if i == 0:
			remark = current_record
		else:
			current = eval(current_record)
			previous = eval(previous_record)
			for key, c, p in zip(current, current.values(), previous.values()):
				if c == p:
					remark[key] = c
				else:
					remark[key] = '<font color="red">' + str(c) + '</font>'

		new_records = {
			'record_obj': record.record_obj,
			'recorder': record.recorder,
			'record_time': record.record_time,
			'record_type': record_type,
			'remark': remark,
		}

		ret.append(new_records)
		previous_record = current_record
	return ret


def order_record(recorder, num, record_type):
	"""
	工单记录
	"""
	records = {
		'record_obj': WorkOrder.objects.get(num=num),
		'recorder': recorder,
		'record_type': record_type,
	}
	WorkOrderLog.objects.create(**records)


def action_menu(form_type, current_user, order_status, proposer, leader):
	edp_user_ids = User.objects.filter(department__simple_title='EDP').values('id')
	edp_user_list = []
	for ids in edp_user_ids:
		edp_user_list.append(ids['id'])
	user_actions = []
	state = order_status

	action_cn_codes = []
	action_en_codes = []
	# icons = []
	if form_type == "A":
		action_cn_codes = ['修改', '处理', '完成', '确认']
		action_en_codes = ['Edit', 'Process', 'Finish', 'Confirm']
		# icons = ['pencil', 'spinner', 'circle-o', 'lock']

		if current_user in edp_user_list:
			user_actions.append('修改')
			if state == "wait":
				user_actions.append('处理')
			if state == "process":
				user_actions.append('完成')
			if state == "finish":
				user_actions.append('确认')

		elif current_user == proposer:
			if state == "wait":
				user_actions.append('修改')
			if state == "process":
				user_actions.append('修改')
			if state == "finish":
				user_actions.append('确认')

	elif form_type == "B" or form_type == "C":
		action_cn_codes = ['修改', '批示', '处理', '确认']
		action_en_codes = ['Edit', 'Approve', 'Process', 'Confirm']
		# icons = ['pencil', 'check', 'circle-o', 'lock']

		if current_user in edp_user_list:
			if state == "finish":
				user_actions.append('处理')

		elif current_user == proposer:
			if state == "wait":
				user_actions.append('修改')
			if state == "process":
				user_actions.append('修改')
			if state == "confirm":
				user_actions.append('确认')

		elif current_user == leader:
			if state == "process":
				user_actions.append('批示')
	else:
		pass
	actions = zip(action_cn_codes, action_en_codes)
	actions_list = []
	for cn_code, en_code in actions:
		if cn_code in user_actions:
			actions_dict = dict(cn_code=cn_code, en_code=en_code)
		else:
			actions_dict = dict(cn_code=cn_code, en_code=en_code, disabled='disabled')
		actions_list.append(actions_dict)
	actions_list.append(dict(cn_code='返回', en_code='Return'))
	return actions_list
