from rest_framework import serializers
from apps.system.models import Permission


class PermissionListSerializer(serializers.ModelSerializer):
    """
    权限列表序列化
    """
    menu_name = serializers.ReadOnlyField(source='menus.name')

    class Meta:
        model = Permission
        fields = ('id', 'name', 'method', 'menu_name', 'pid')
