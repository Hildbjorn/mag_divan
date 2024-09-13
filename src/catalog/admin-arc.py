from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import escape, format_html

from .models import Color, FurnitureModel, FurnitureType, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 5  # Количество пустых форм для добавления новых изображений
    fields = ('image', 'color', 'uploaded_at')
    # Сделаем поле "Дата загрузки" только для чтения
    readonly_fields = ('uploaded_at',)


@admin.register(FurnitureType)
class FurnitureTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FurnitureModel)
class FurnitureModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # Автоматическое заполнение slug
    inlines = [ImageInline]  # Включаем инлайн для изображений


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('hex_code_display', 'name',
                    'hex_code', 'description', 'slug')
    list_display_links = ('hex_code_display', 'name',)
    search_fields = ('name', 'hex_code')
    prepopulated_fields = {'slug': ('name',)}  # Автоматическое заполнение slug

    def hex_code_display(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border: 1px solid #000; border-radius: 50%;"></div>',
            obj.hex_code
        )
    hex_code_display.short_description = 'Цвет'  # Заголовок столбца


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'color_display', 'uploaded_at')
    list_display_links = ('image_tag',)
    fieldsets = (
        (None, {
            # Изменено на furniture_model
            'fields': (('furniture_model', 'color'),),
        }),
        (None, {
            'fields': ('image_thumbnail', 'image',),
        }),
        (None, {
            'fields': ('uploaded_at',),
        }),
    )
    readonly_fields = ('image_thumbnail', 'uploaded_at')

    def image_tag(self, obj):
        return format_html('<img src="{}" width="70" height="70" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)

    def color_display(self, obj):
        return format_html(
            '<div class="color__field">'
            '<div class="color__preview" style="background-color: {};"></div>'
            '{}: {}'
            '</div>',
            obj.color.hex_code,
            obj.color.name,
            obj.color.hex_code
        )

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img id="image_thumbnail" src="{}" width="250" height="250" style="object-fit: cover; border-radius: 5px;" />',
                               obj.image.url)
        return format_html('<img id="image_thumbnail" src="{}" width="250" height="250" style="object-fit: cover; border-radius: 5px;" />',
                           static('img/elements/no_foto.webp'))

    image_tag.short_description = 'Фото'
    color_display.short_description = 'Цвет'
    image_thumbnail.short_description = 'Предпросмотр фото'
