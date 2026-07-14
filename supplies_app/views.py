from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Device, DeviceType, Vendor, Consumable, ConsumableType, Compatibility, Color


@staff_member_required
def manage_consumables(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    vendors = Vendor.objects.all().order_by('name')
    consumable_types = ConsumableType.objects.all().order_by('name')

    vendor_id = request.GET.get('vendor')
    consumable_type_id = request.GET.get('consumable_type')

    consumables = Consumable.objects.all()
    if vendor_id:
        consumables = consumables.filter(vendor_id=vendor_id)
    if consumable_type_id:
        consumables = consumables.filter(consumable_type_id=consumable_type_id)

    existing_ids = Compatibility.objects.filter(device=device).values_list('consumable_id', flat=True)

    if request.method == 'POST':
        selected_ids = request.POST.getlist('consumables')
        Compatibility.objects.filter(device=device).delete()
        for consumable_id in selected_ids:
            Compatibility.objects.create(device=device, consumable_id=consumable_id)
        messages.success(request, f'Расходники для устройства "{device}" обновлены.')
        return redirect('admin:supplies_app_device_change', device.id)

    return render(request, 'admin/supplies_app/manage_consumables.html', {
        'device': device,
        'vendors': vendors,
        'consumable_types': consumable_types,
        'consumables': consumables,
        'existing_ids': existing_ids,
        'selected_vendor': vendor_id,
        'selected_type': consumable_type_id,
    })


@staff_member_required
def manage_devices(request, consumable_id):
    consumable = get_object_or_404(Consumable, id=consumable_id)
    vendors = Vendor.objects.all().order_by('name')
    device_types = DeviceType.objects.all().order_by('name')

    vendor_id = request.GET.get('vendor')
    device_type_id = request.GET.get('device_type')

    devices = Device.objects.all()
    if vendor_id:
        devices = devices.filter(vendor_id=vendor_id)
    if device_type_id:
        devices = devices.filter(device_type_id=device_type_id)

    existing_ids = Compatibility.objects.filter(consumable=consumable).values_list('device_id', flat=True)

    if request.method == 'POST':
        selected_ids = request.POST.getlist('devices')
        Compatibility.objects.filter(consumable=consumable).delete()
        for device_id in selected_ids:
            Compatibility.objects.create(consumable=consumable, device_id=device_id)
        messages.success(request, f'Устройства для расходника "{consumable}" обновлены.')
        return redirect('admin:supplies_app_consumable_change', consumable.id)

    return render(request, 'admin/supplies_app/manage_devices.html', {
        'consumable': consumable,
        'vendors': vendors,
        'device_types': device_types,
        'devices': devices,
        'existing_ids': existing_ids,
        'selected_vendor': vendor_id,
        'selected_type': device_type_id,
    })

def index(request):
    """Главная страница с двумя блоками поиска"""
    return render(request, 'supplies_app/index.html')


def search(request):
    """Результаты поиска по устройствам и расходникам"""
    query = request.GET.get('q', '').strip()
    device_results = []
    consumable_results = []

    if query:
        from django.db.models import Q
        device_results = Device.objects.filter(
            Q(model_name__icontains=query) | Q(vendor__name__icontains=query)
        )
        consumable_results = Consumable.objects.filter(
            Q(name__icontains=query) | Q(part_number__icontains=query)
        )

    return render(request, 'supplies_app/search.html', {
        'query': query,
        'device_results': device_results,
        'consumable_results': consumable_results,
    })

def device_detail(request, device_id):
    """Детальная страница устройства со списком совместимых расходников"""
    device = get_object_or_404(Device, id=device_id)
    consumables = Consumable.objects.filter(
        compatibilities__device=device
    ).select_related('vendor', 'consumable_type', 'color')
    return render(request, 'supplies_app/device_detail.html', {
        'device': device,
        'consumables': consumables,
    })


def consumable_detail(request, consumable_id):
    """Детальная страница расходника со списком совместимых устройств"""
    consumable = get_object_or_404(Consumable, id=consumable_id)
    devices = Device.objects.filter(
        compatibilities__consumable=consumable
    ).select_related('vendor', 'device_type')
    return render(request, 'supplies_app/consumable_detail.html', {
        'consumable': consumable,
        'devices': devices,
    })


def device_list(request):
    """Страница каталога устройств с фильтрами"""
    vendors = Vendor.objects.all().order_by('name')
    device_types = DeviceType.objects.all().order_by('name')

    vendor_id = request.GET.get('vendor')
    device_type_id = request.GET.get('device_type')

    devices = Device.objects.all().select_related('vendor', 'device_type').order_by('vendor')
    if vendor_id:
        devices = devices.filter(vendor_id=vendor_id)
    if device_type_id:
        devices = devices.filter(device_type_id=device_type_id)

    return render(request, 'supplies_app/device_list.html', {
        'devices': devices,
        'vendors': vendors,
        'device_types': device_types,
        'selected_vendor': vendor_id,
        'selected_type': device_type_id,
    })


def consumable_list(request):
    """Страница каталога расходников с фильтрами"""
    vendors = Vendor.objects.all().order_by('name')
    consumable_types = ConsumableType.objects.all().order_by('name')
    colors = Color.objects.all().order_by('name')

    vendor_id = request.GET.get('vendor')
    consumable_type_id = request.GET.get('consumable_type')
    color_id = request.GET.get('color')

    consumables = Consumable.objects.all().select_related('vendor', 'consumable_type', 'color').order_by('consumable_type', 'vendor')
    if vendor_id:
        consumables = consumables.filter(vendor_id=vendor_id)
    if consumable_type_id:
        consumables = consumables.filter(consumable_type_id=consumable_type_id)
    if color_id:
        consumables = consumables.filter(color_id=color_id)

    return render(request, 'supplies_app/consumable_list.html', {
        'consumables': consumables,
        'vendors': vendors,
        'consumable_types': consumable_types,
        'colors': colors,
        'selected_vendor': vendor_id,
        'selected_type': consumable_type_id,
        'selected_color': color_id,
    })
