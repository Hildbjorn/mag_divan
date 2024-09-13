from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
# Импортируйте необходимые модели
from .models import FurnitureType, Image, FurnitureModel, Color


class ColorCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):

        print(f"Value passed to render: {value}")

        output = []
        # Преобразуем value в множество для более быстрой проверки
        value_set = set(map(str, value)) if value else set()

        for i, (option_value, option_label) in enumerate(self.choices):
            # Получение hex_code (предполагаем, что это уже реализовано)
            if isinstance(option_label, str):
                color_obj = Color.objects.get(name=option_label)
                hex_code = color_obj.hex_code
            else:
                hex_code = option_label.hex_code

            checked = 'checked' if str(option_value) in value_set else ''
            checkbox_html = f'<input type="checkbox" name="{name}" value="{
                option_value}" {checked} id="id_{name}_{i}">'

            # Добавляем кружок перед спаном
            circle_html = f'<span class="check_colors_sample" style="background-color: {
                hex_code};"></span>'
            span_html = f'<span>{option_label} ({hex_code})</span>'
            label_html = f'<label for="id_{name}_{i}">{
                checkbox_html} {circle_html} {span_html}</label>'
            output.append(label_html)

        return mark_safe('\n'.join(output))

    def value_from_datadict(self, data, files, name):
        return super().value_from_datadict(data, files, name)


@admin.register(FurnitureType)
class FurnitureTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FurnitureModel)
class FurnitureModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_colors', 'type', 'description', 'slug',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = FurnitureModel

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'colors':
            kwargs['widget'] = ColorCheckboxSelectMultiple()
            kwargs['queryset'] = Color.objects.all()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def display_colors(self, obj):
        colors_html = "".join(
            f"""<div class="display_colors_item">
            <div class="display_colors_sample" style="background-color: {color.hex_code};"></div>
            <span>{color.name} ({color.hex_code})</span>
        </div>"""
            for color in obj.colors.all()
        )
        return mark_safe(f'<div>{colors_html}</div>')
    display_colors.short_description = 'Цвета'


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
    hex_code_display.short_description = 'Цвет'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'furniture_model',
                    'color_display', 'uploaded_at')
    list_display_links = ('image_tag', 'furniture_model',)
    fieldsets = (
        (None, {
            'fields': ('furniture_model', 'color', 'image'),
        }),
        (None, {
            'fields': ('uploaded_at',),
        }),
    )
    readonly_fields = ('uploaded_at',)

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

    image_tag.short_description = 'Фото'
    color_display.short_description = 'Цвет'
