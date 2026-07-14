from django.urls import path
from . import views

app_name = 'supplies_app'

urlpatterns = [
    path('admin/device/<int:device_id>/manage_consumables/', views.manage_consumables, name='manage_consumables'),
]
