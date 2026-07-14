from django.db import models


class DeviceType(models.Model):
    """Тип устройства (Принтер, МФУ, Копир)"""
    name = models.CharField('Название типа', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип устройства'
        verbose_name_plural = 'Типы устройств'


class Vendor(models.Model):
    """Производитель (вендор) устройства или расходника"""
    name = models.CharField('Название производителя', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Color(models.Model):
    """Цвет расходного материала"""
    name = models.CharField('Название цвета', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Device(models.Model):
    """Модель устройства (принтера, МФУ и т.д.)"""
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='devices',
        verbose_name='Производитель'
    )
    device_type = models.ForeignKey(
        DeviceType,
        on_delete=models.CASCADE,
        related_name='devices',
        verbose_name='Тип устройства'
    )
    model_name = models.CharField('Модель', max_length=200)
    photo = models.ImageField(
        'Фото устройства',
        upload_to='device_photos/',
        blank=True,
        null=True
    )

    def __str__(self):
        if self.device_type:
            return f'{self.device_type.name} {self.vendor.name} {self.model_name}'
        return f'{self.vendor.name} {self.model_name}'

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'


class ConsumableType(models.Model):
    """Тип расходного материала (картридж, фотовал, бушинг и т.д.)"""
    name = models.CharField('Название типа', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип расходника'
        verbose_name_plural = 'Типы расходников'


class Consumable(models.Model):
    """Расходный материал (картридж, тонер и т.д.)"""
    name = models.CharField(
        'Название расходного материала',
        max_length=200,
        blank=True,
        help_text='Заполняется автоматически из производителя, типа, цвета и артикула'
    )
    part_number = models.CharField(
        'Артикул производителя',
        max_length=100,
        unique=True,
        help_text='Оригинальный номер производителя'
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consumables',
        verbose_name='Производитель'
    )
    consumable_type = models.ForeignKey(
        ConsumableType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consumables',
        verbose_name='Тип расходника'
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consumables',
        verbose_name='Цвет'
    )
    photo = models.ImageField(
        'Фото расходного материала',
        upload_to='consumable_photos/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        parts = []
        if self.consumable_type:
            parts.append(self.consumable_type.name)
        if self.vendor:
            parts.append(self.vendor.name)
        if self.color:
            parts.append(self.color.name)
        if self.part_number:
            parts.append(self.part_number)
        self.name = ' '.join(parts) if parts else 'Без названия'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Расходный материал'
        verbose_name_plural = 'Расходные материалы'


class Compatibility(models.Model):
    """Связь между устройством и расходником (совместимость)"""
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='compatibilities',
        verbose_name='Устройство'
    )
    consumable = models.ForeignKey(
        Consumable,
        on_delete=models.CASCADE,
        related_name='compatibilities',
        verbose_name='Расходный материал'
    )

    def __str__(self):
        return f'{self.device} → {self.consumable}'

    class Meta:
        verbose_name = 'Совместимость'
        verbose_name_plural = 'Совместимости'
        unique_together = ('device', 'consumable')
