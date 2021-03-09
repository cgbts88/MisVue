from rest_framework import serializers
from apps.system.models import Role


class RoleListSerializer(serializers.ModelSerializer):
    """
    角色序列化
    """
    class Meta:
        model = Role
        fields = '__all__'
        # depth = 1
