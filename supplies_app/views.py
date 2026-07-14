from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Device, DeviceType, Vendor, Consumable, ConsumableType, Compatibility


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
