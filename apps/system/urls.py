from django.urls import path, include
from rest_framework import routers
from apps.system.views import menu, role

router = routers.SimpleRouter()
router.register(r'menus', menu.MenuViewSet, basename='menus')

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/menu/tree/', menu.MenuTreeView.as_view(), name='menu_tree')
]
