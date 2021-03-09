from django.urls import path

from apps.users import views_users, views_base

urlpatterns = [

    path('', views_users.UserIndexView.as_view(), name='index'),

    # Users Router
    path('user/', views_users.UsersListView.as_view(), name='user-list'),
    path('user/create/', views_users.UsersCreateView.as_view(), name='user-create'),
    path('user/detail/', views_users.UsersDetailView.as_view(), name='user-detail'),
    path('user/delete/', views_users.UsersDeleteView.as_view(), name='user-delete'),
    path('user/active/', views_users.UsersActiveView.as_view(), name='user-active'),
    path('user/reset/', views_users.UsersResetView.as_view(), name='user-reset'),
    path('user/permit/', views_users.UsersPermitView.as_view(), name='user-permit'),

    # Department Router
    path('department/', views_base.DepartmentListView.as_view(), name='department-list'),
    path('department/create/', views_base.DepartmentCreateView.as_view(), name='department-create'),
    path('department/detail/', views_base.DepartmentDetailView.as_view(), name='department-detail'),
    path('department/relation/', views_base.DepartmentRelationView.as_view(), name='department-relation'),
    path('department/delete/', views_base.DepartmentDeleteView.as_view(), name='department-delete'),

    # Location Router
    path('location/', views_base.LocationListView.as_view(), name='location-list'),
    path('location/create/', views_base.LocationCreateView.as_view(), name='location-create'),
    path('location/detail/', views_base.LocationDetailView.as_view(), name='location-detail'),
    path('location/relation/', views_base.LocationRelationView.as_view(), name='location-relation'),
    path('location/delete/', views_base.LocationDeleteView.as_view(), name='location-delete'),

    # Position Router
    path('position/', views_base.PositionListView.as_view(), name='position-list'),
    path('position/create/', views_base.PositionCreateView.as_view(), name='position-create'),
    path('position/detail/', views_base.PositionDetailView.as_view(), name='position-detail'),
    path('position/relation/', views_base.PositionRelationView.as_view(), name='position-relation'),
    path('position/delete/', views_base.PositionDeleteView.as_view(), name='position-delete'),

    # Permit Router
    path('permit/', views_users.PermitListView.as_view(), name='permit-list'),
    path('permit/create/', views_users.PermitCreateView.as_view(), name='permit-create'),
    path('permit/delete/', views_users.PermitDeleteView.as_view(), name='permit-delete'),
    path('permit/detail/', views_users.PermitDetailView.as_view(), name='permit-detail'),
    path('permit/relation/', views_users.PermitRelationView.as_view(), name='permit-relation'),

]
