import os
from django.core.validators import RegexValidator
from django.db import models

from django.db import models
from django.utils import timezone

from core.utils import get_slug, resize_and_crop_image, set_furniture_image_filename


class FurnitureType(models.Model):
    """
    Модель для хранения типов мебели (например, "диваны").
    """
    name = models.CharField(max_length=100,
                            verbose_name="Тип мебели")
    description = models.TextField(blank=True,
                                   verbose_name="Описание")
    slug = models.SlugField(unique=True,
                            blank=True,
                            verbose_name="Slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип мебели'
        verbose_name_plural = 'Типы мебели'
        ordering = ['name']


class FurnitureModel(models.Model):
    """
    Модель для хранения конкретных моделей мебели (например, угловой диван "Елена").
    """
    type = models.ForeignKey(FurnitureType,
                             related_name='models',
                             on_delete=models.CASCADE,
                             verbose_name="Тип мебели")
    name = models.CharField(max_length=100,
                            verbose_name="Модель мебели")
    colors = models.ManyToManyField('Color',
                                    related_name='furniture_models',
                                    verbose_name="цвета мебели")
    description = models.TextField(blank=True,
                                   verbose_name="Описание")
    slug = models.SlugField(unique=True,
                            blank=True,
                            verbose_name="Slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель мебели'
        verbose_name_plural = 'Модели мебели'
        ordering = ['name']


class Color(models.Model):
    """
    Модель для хранения цветов моделей.
    """
    name = models.CharField(max_length=50,
                            verbose_name="Цвет мебели")

    hex_code = models.CharField(max_length=7,
                                validators=[RegexValidator(regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                                                           message='Введите цвет в формате HEX (#RRGGBB или #RGB).')],
                                verbose_name="HEX код цвета"
                                )
    description = models.TextField(blank=True,
                                   verbose_name="Описание")
    slug = models.SlugField(unique=True,
                            blank=True,
                            verbose_name="Slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет мебели'
        verbose_name_plural = 'Цвета мебели'
        ordering = ['hex_code']


class FurnitureBase(models.Model):
    """
    Абстрактная модель, которая объединяет FurnitureModel и Color
    """
    furniture_model = models.ForeignKey(FurnitureModel,
                                        null=True,
                                        on_delete=models.CASCADE,
                                        verbose_name="Модель мебели")
    color = models.ForeignKey(Color,
                              null=True,
                              on_delete=models.CASCADE,
                              verbose_name="Цвет")

    class Meta:
        abstract = True


class Image(FurnitureBase):
    """
    Модель для хранения изображений.
    """
    image = models.ImageField(upload_to=set_furniture_image_filename,
                              verbose_name="Фото"
                              )
    max_size = (1024, 1024)
    uploaded_at = models.DateTimeField(auto_now=True,
                                       verbose_name="Дата и время обновления")

    def __str__(self):
        return f'{self.furniture_model}_{self.color}_{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_and_crop_image(self.image.path, self.max_size)
            self.image = self.image
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Определение пути к изображению
        image_path = self.image.path if self.image else None
        # Вызов суперметода для удаления объекта из базы данных
        super().delete(*args, **kwargs)
        # Удаление файла изображения, если он существует
        if image_path and os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print('Удаление файла изображения не удалось', e)

    class Meta:
        verbose_name = 'Фото мебели'
        verbose_name_plural = 'Фото мебели'
        ordering = ['-uploaded_at']
