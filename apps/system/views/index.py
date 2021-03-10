import jwt

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from operator import itemgetter

from MIS.code import *
from MIS.basic import MisResponse
from MIS.settings import SECRET_KEY

from apps.users.models import UserProfile
from apps.system.models import Menu
from apps.users.serializers.users import UserListSerializer
from apps.system.serializers.menu import MenuSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserAuthView(APIView):
    """
    用户认证获取 token
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            return MisResponse({'token': jwt.encode(payload, SECRET_KEY)}, status=OK)
        else:
            return MisResponse('用户名或密码错误！', status=BAD)


