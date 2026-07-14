from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from supplies_app import views

urlpatterns = [
    path('', include('supplies_app.urls', namespace='supplies_app')),
    path('admin/device/<int:device_id>/manage_consumables/', views.manage_consumables, name='manage_consumables'),
    path('admin/consumable/<int:consumable_id>/manage_devices/', views.manage_devices, name='manage_devices'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
