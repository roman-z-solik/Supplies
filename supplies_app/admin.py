from django.contrib import admin
from .models import DeviceType, Vendor, Color, Device, ConsumableType, Consumable, Compatibility


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(ConsumableType)
class ConsumableTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


class DeviceCompatibilityInline(admin.TabularInline):
    model = Compatibility
    fk_name = 'consumable'
    extra = 1
    autocomplete_fields = ('device',)
    verbose_name = 'Совместимое устройство'
    verbose_name_plural = 'Совместимые устройства'


class ConsumableCompatibilityInline(admin.TabularInline):
    model = Compatibility
    fk_name = 'device'
    extra = 1
    autocomplete_fields = ('consumable',)
    verbose_name = 'Совместимый расходник'
    verbose_name_plural = 'Совместимые расходники'


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'device_type', 'model_name')
    list_filter = ('vendor', 'device_type')
    search_fields = ('model_name', 'vendor__name')
    inlines = [ConsumableCompatibilityInline]
    fieldsets = (
        (None, {
            'fields': ('vendor', 'device_type', 'model_name')
        }),
        ('Фото', {
            'fields': ('photo',),
            'description': 'Загрузите фото устройства'
        }),
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['manage_consumables_url'] = f'/admin/device/{object_id}/manage_consumables/'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'consumable_type', 'color', 'part_number')
    list_filter = ('vendor', 'consumable_type', 'color')
    search_fields = ('name', 'part_number')
    inlines = [DeviceCompatibilityInline]
    fieldsets = (
        (None, {
            'fields': ('vendor', 'consumable_type', 'color', 'part_number')
        }),
        ('Фото', {
            'fields': ('photo',),
            'description': 'Загрузите фото расходного материала'
        }),
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['manage_devices_url'] = f'/admin/consumable/{object_id}/manage_devices/'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
