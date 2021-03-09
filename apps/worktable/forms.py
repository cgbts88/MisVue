# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth import get_user_model

from apps.worktable.models import WorkOrder

User = get_user_model()


class OrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ('type', 'content',)
        error_messages = {
            "content": {"required": "请输入工单内容"},
        }


class InsteadForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ('proposer', 'content', 'type',)
        error_messages = {
            "proposer": {"required": "请选择用户"},
            "content": {"required": "请输入工单内容"},
        }
