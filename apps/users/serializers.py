from django.contrib.auth import get_user_model

from rest_framework import serializers
from apps.users.models import UserProfile, Department

User = get_user_model()


class UserForSelectSerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField(source='__str__')

    class Meta:
        model = User
        fields = ('id', 'username', 'display_name')


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id',)


class DepartmentForSelectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'simple_title']
