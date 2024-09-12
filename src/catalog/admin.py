from django.contrib import admin

from .models import Color, FurnitureModel, FurnitureSubType, FurnitureType, Image


@admin.register(FurnitureType)
class FurnitureTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FurnitureSubType)
class FurnitureSubTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description', 'slug')
    search_fields = ('name', 'description')
    list_filter = ('type',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FurnitureModel)
class FurnitureModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtype', 'description', 'slug')
    search_fields = ('name', 'description')
    list_filter = ('subtype',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'hex_code', 'description', 'slug')
    search_fields = ('name', 'hex_code', 'description')
    list_filter = ('model',)
    prepopulated_fields = {'slug': ('name',)}
    # Позволяет удобно выбирать изображения из списка
    filter_horizontal = ('images',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('images')  # Оптимизация запросов


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'uploaded_at', 'description')
    search_fields = ('description',)
    ordering = ('-uploaded_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()  # Оптимизация запросов, если нужно

    def delete_model(self, request, obj):
        # Переопределение метода удаления для корректного удаления файла
        obj.delete()  # Вызываем метод удаления, который уже реализован в модели
