from django.urls import path, include
from rest_framework import routers
from apps.system.views import index

routers = routers.SimpleRouter()

urlpatterns = [
    path(r'api/', include(routers.urls)),
    path(r'auth/login/', index.UserAuthView.as_view())
]
