# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from apps.users.models import Permit

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"required": "请填写用户名"})
    password = forms.CharField(required=True, error_messages={"required": "请填写密码"})


class UserUpdateForm(forms.ModelForm):
    """
    用户创建-修改表单
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'en_name', 'cn_name', 'work_card', 'gender',
                  'ext_num', 'birthday', 'department', 'location', 'position', 'roles']
        error_messages = {
            'en_name': {'required': '英文姓名不能为空'},
            'cn_name': {'required': '中文姓名不能为空'},
            'work_card': {'required': '工卡号不能为空'},
            'ext_num': {'required': '座机不能为空'},
            'department': {'required': '部门不能为空'},
            'location': {'required': '位置不能为空'},
            }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False


    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        ext_num = cleaned_data.get("ext_num")

        # email = cleaned_data.get("email")

        # if User.objects.filter(username=username).count() and username != "":
        # 	raise forms.ValidationError('用户名：{}已存在'.format(username))

        if ext_num and not ext_num.isdigit() and ext_num != "":
            raise forms.ValidationError('请填写正确的号码')

        # if User.objects.filter(email=email).count() and email != "":
        # 	raise forms.ValidationError('邮箱：{}已存在'.format(email))

        return cleaned_data


class SelfPasswordChangeForm(forms.Form):
    """
    用户自行修改密码
    """

    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"密码不能为空"
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"确认密码不能为空"
        })

    def clean(self):
        cleaned_data = super(SelfPasswordChangeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")


class PermitForm(forms.ModelForm):
    """
    权限管理
    """
    class Meta:
        model = Permit
        fields = '__all__'


class UserCenterForm(forms.ModelForm):
    """
    用户创建-修改表单
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'cn_name', 'work_card', 'gender', 'ext_num', 'birthday',
                  'department', 'location', 'roles']
        error_messages = {
            'username': {'required': '用户名不能为空'},
            'en_name': {'required': '英文姓名不能为空'},
            'cn_name': {'required': '中文姓名不能为空'},
            'work_card': {'required': '工卡号不能为空'},
            'ext_num': {'required': '座机不能为空'},
            'department': {'required': '部门不能为空'},
            'location': {'required': '位置不能为空'},
        }

    def clean(self):
        cleaned_data = super(UserCenterForm, self).clean()
        # username = cleaned_data.get("username")
        ext_num = cleaned_data.get("ext_num")
        # email = cleaned_data.get("email")

        # if User.objects.filter(username=username).count() and username != "":
        # 	raise forms.ValidationError('用户名：{}已存在'.format(username))

        if ext_num and not ext_num.isdigit() and ext_num != "":
            raise forms.ValidationError('请填写正确的号码')

        # if User.objects.filter(email=email).count() and email != "":
        # 	raise forms.ValidationError('邮箱：{}已存在'.format(email))

        return cleaned_data
