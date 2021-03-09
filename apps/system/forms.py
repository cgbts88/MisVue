# -*- coding:utf-8 -*-

from django import forms
from apps.system.models import Menu, EmailSetup, FileUpload


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'


class EmailSetupForm(forms.ModelForm):
    class Meta:
        model = EmailSetup
        fields = '__all__'


class UploadForm(forms.ModelForm):
    """
    上传
    """
    class Meta:
        model = FileUpload
        fields = ('file',)
        error_messages = {
            'file': {'required': '文件不能为空'},
        }
