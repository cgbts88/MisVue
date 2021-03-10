from rest_framework import serializers
from apps.users.models import Department


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id',)


class DepartmentForSelectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'simple_title']
