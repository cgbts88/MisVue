from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.worktable import views, views_order


order_list = views_order.WorkOrderView.as_view({'get': 'get', 'post': 'multiple_delete'})
order_create = views_order.WorkOrderCreateView.as_view({'get': 'get', 'post': 'create',})
order_detail = views_order.WorkOrderDetailView.as_view({'get': 'get', 'post': 'update'})

urlpatterns = [

    path('', views.WorktableIndexView.as_view(), name='index'),
    path('phonebook/', views.PhoneBookView.as_view(), name='phonebook'),
    path('notice/', views. NoticeCenterView.as_view(), name='notice'),
    path('person/', views. PersonCenterView.as_view(), name='person'),
    path('person/passwdchange/', views. PersonPasswordChangeView.as_view(), name='passwdchange'),

    # Form_A Router
    path('order/', order_list, name='order-list'),
    path('order/create/', order_create, name='order-create'),
    re_path(r'^order/(?P<num>\w-\d{10})$', order_detail, name='order-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
