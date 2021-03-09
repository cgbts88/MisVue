from rest_framework import serializers
from apps.system.models import Menu


class MenuSerializer(serializers.ModelSerializer):
    """
    菜单序列化
    """

    class Meta:
        model = Menu
        fields = ('id', 'sort', 'name', 'icon', 'path', 'is_frame', 'is_show', 'component', 'pid')
        extra_kwargs = {'name': {'required': True, 'error_messages': {'required': '必须填写菜单名'}}}
