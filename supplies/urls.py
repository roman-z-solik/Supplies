from django.contrib import admin
from django.urls import path
from supplies_app import views

urlpatterns = [
    path('admin/device/<int:device_id>/manage_consumables/', views.manage_consumables, name='manage_consumables'),
    path('admin/consumable/<int:consumable_id>/manage_devices/', views.manage_devices, name='manage_devices'),  # ← новый
    path('admin/', admin.site.urls),
]
