# -*- coding: UTF-8 -*-

from django.urls import path

from apps.asset import views_base, views_stock, views_info


urlpatterns = [

	path('', views_base.AssetIndexView.as_view(), name='index'),

	# TypeCode Manager
	path('typecode/', views_base.TypeCodeListView.as_view(), name="typecode-list"),
	path('typecode/create/', views_base.TypeCodeCreateView.as_view(), name="typecode-create"),
	path('typecode/detail/', views_base.TypeCodeDetailView.as_view(), name="typecode-detail"),
	path('typecode/delete/', views_base.TypeCodeDeleteView.as_view(), name="typecode-delete"),
	path('typecode/relation/', views_base.TypeCodeRelationView.as_view(), name="typecode-relation"),

	# Attribute Manager
	path('attribute/', views_base.AttributeListView.as_view(), name="attribute-list"),
	path('attribute/create/', views_base.AttributeCreateView.as_view(), name="attribute-create"),
	path('attribute/detail/', views_base.AttributeDetailView.as_view(), name="attribute-detail"),
	path('attribute/relation/', views_base.AttributeRelationView.as_view(), name="attribute-relation"),
	path('attribute/delete/', views_base.AttributeDeleteView.as_view(), name="attribute-delete"),

	# Asset Stock
	path('stock/', views_stock.StockListView.as_view(), name="stock-list"),
	path('stock/create/', views_stock.StockCreateView.as_view(), name="stock-create"),
	path('stock/detail/', views_stock.StockDetailView.as_view(), name="stock-detail"),
	path('stock/relation/', views_stock.StockRelationView.as_view(), name="stock-relation"),
	path('stock/delete/', views_stock.StockDeleteView.as_view(), name="stock-delete"),

	# Asset Scrap
	path('scrap/', views_stock.ScrapListView.as_view(), name="scrap-list"),
	path('scrap/detail/', views_stock.ScrapDetailView.as_view(), name="scrap-detail"),
	path('scrap/cancel/', views_stock.ScrapCancelView.as_view(), name="scrap-cancel"),
	path('scrap/done/', views_stock.ScrapDoneView.as_view(), name="scrap-done"),

	# Network Device
	path('networkdevice/', views_info.NetworkDeviceListView.as_view(), name="networkdevice-list"),
	path('networkdevice/create/', views_info.NetworkDeviceCreateView.as_view(), name="networkdevice-create"),
	path('networkdevice/detail/', views_info.NetworkDeviceDetailView.as_view(), name="networkdevice-detail"),
	path('networkdevice/relation/', views_info.NetworkDeviceRelationView.as_view(), name="networkdevice-relation"),
	path('networkdevice/delete/', views_info.NetworkDeviceDeleteView.as_view(), name="networkdevice-delete"),

	# Other Device
	path('otherdevice/', views_info.OtherDeviceListView.as_view(), name="otherdevice-list"),
	path('otherdevice/create/', views_info.OtherDeviceCreateView.as_view(), name="otherdevice-create"),
	path('otherdevice/detail/', views_info.OtherDeviceDetailView.as_view(), name="otherdevice-detail"),
	path('otherdevice/relation/', views_info.OtherDeviceRelationView.as_view(), name="otherdevice-relation"),
	path('otherdevice/delete/', views_info.OtherDeviceDeleteView.as_view(), name="otherdevice-delete"),

	# order
	path('order/', views_info.AssetOrderListView.as_view(), name="order-list"),
	path('order/select/', views_info.AssetOrderSelectView.as_view(), name="order-select"),
	path('order/create/', views_info.AssetOrderCreateView.as_view(), name="order-create"),
	path('order/delete/', views_info.AssetOrderDeleteView.as_view(), name="order-delete"),

]
