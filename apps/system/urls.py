from django.urls import path

from apps.system import views_index, views_menu, views_role

urlpatterns = [

    path('', views_index.SystemIndexView.as_view(), name='system'),
    path('upload/', views_index.UploadView.as_view(), name='upload'),
    path('export/', views_index.ExportView.as_view(), name='export'),

    # menu manager
    path('menu/', views_menu.MenuListView.as_view(), name='menu-list'),
    path('menu/create/', views_menu.MenuCreateView.as_view(), name='menu-create'),
    path('menu/detail/', views_menu.MenuDetailView.as_view(), name='menu-detail'),
    path('menu/delete/', views_menu.MenuDeleteView.as_view(), name='menu-delete'),

    # role manager
    path('role/', views_role.RoleListView.as_view(), name='role-list'),
    path('role/create/', views_role.RoleCreateView.as_view(), name='role-create'),
    path('role/detail/', views_role.RoleDetailView.as_view(), name='role-detail'),
    path('role/delete/', views_role.RoleDeleteView.as_view(), name='role-delete'),
    path('role/role2user/', views_role.Role2UserView.as_view(), name="role-role2user"),
    path('role/role2menu/', views_role.Role2MenuView.as_view(), name="role-role2menu"),

]
