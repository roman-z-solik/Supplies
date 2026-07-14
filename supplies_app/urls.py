from django.urls import path
from . import views

app_name = 'supplies_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('admin/device/<int:device_id>/manage_consumables/', views.manage_consumables, name='manage_consumables'),
    path('admin/consumable/<int:consumable_id>/manage_devices/', views.manage_devices, name='manage_devices'),
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),
    path('consumable/<int:consumable_id>/', views.consumable_detail, name='consumable_detail'),
    path('devices/', views.device_list, name='device_list'),
    path('consumables/', views.consumable_list, name='consumable_list'),
]
