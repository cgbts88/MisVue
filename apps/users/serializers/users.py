import re

from rest_framework import serializers
from apps.users.models import UserProfile


class UserListSerializer(serializers.ModelSerializer):
    """
    用戶列表的序列化
    """
    roles = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'ext_num', 'email', 'image', 'department', 'position',
                  'is_active', 'roles']
        depth = 1

    def get_roles(self, obj):
        return obj.roles.values()


class UserModifySerializer(serializers.ModelSerializer):
    """
    用戶編輯的序列化
    """
    ext_num = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'ext_num', 'email', 'image', 'department', 'position',
                  'is_active', 'roles']

    def validate_ext_num(self, ext_num):
        REGEX_EXT = "^\\d{5}"
        if not re.match(REGEX_EXT, ext_num):
            raise serializers.ValidationError("座机号码不正确")
        return ext_num


class UserCreateSerializer(serializers.ModelSerializer):
    """
    创建用戶的序列化
    """
    username = serializers.CharField(required=True, allow_blank=False)
    ext_num = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'ext_num', 'email', 'image', 'department', 'position',
                  'is_active', 'roles']

    def validate_username(self, username):
        if UserProfile.objects.filter(username=username):
            raise serializers.ValidationError(username + ' 帐号已经存在')
        return username

    def validate_ext_num(self, ext_num):
        REGEX_EXT = "^\\d{5}"
        if not re.match(REGEX_EXT, ext_num):
            raise serializers.ValidationError("座机号码不正确")
        return ext_num


class UserForSelectSerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField(source='__str__')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'display_name')
