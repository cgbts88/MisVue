# -*- coding: UTF-8 -*-

from django import forms
from apps.asset.models import TypeCode, Attribute, Stock, NetworkDevice, OtherDevice


class TypeCodeForm(forms.ModelForm):
	"""
	分类编码表单
	"""

	class Meta:
		model = TypeCode
		fields = '__all__'
		error_messages = {
			"simple_code": {"required": "分类简写不能为空"},
			"en_code": {"required": "英文分类不能为空"},
			"cn_code": {"required": "中文分类不能为空"},
		}


class AttributeForm(forms.ModelForm):
	"""
	属性信息表单
	"""

	class Meta:
		model = Attribute
		fields = '__all__'
		error_messages = {
			"type": {"required": "请选择分类"},
			"brand": {"required": "品牌不能为空"},
			"model": {"required": "型号不能为空"},
		}


class StockForm(forms.ModelForm):
	"""
	库存信息表单
	"""

	class Meta:
		model = Stock
		fields = '__all__'
		error_message = {
			"edp_num": {'required': "请输入EDP编号"},
			"sn": {'required': "序列号不能为空"},
			"model": {'required': "请选择型号"},
		}


class NetworkDeviceForm(forms.ModelForm):
	class Meta:
		model = NetworkDevice
		fields = '__all__'
		error_messages = {
			"stock": {"required": "请选择资产编号"},
			"device_name": {"required": "请填写设备编号"},
			"asset_user": {"required": "请选择资产使用人"},
			"asset_owner": {"required": "请选择资产责任人"},
		}


class OtherDeviceForm(forms.ModelForm):
	class Meta:
		model = OtherDevice
		fields = '__all__'
		error_messages = {
			"stock_num": {"required": "请选择资产编号"},
			"asset_user": {"required": "请选择资产使用人"},
			"asset_owner": {"required": "请选择资产责任人"},
		}
