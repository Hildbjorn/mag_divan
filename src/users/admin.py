from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.templatetags.static import static
from django.utils.html import format_html
from .forms import ProfileCreationForm, ProfileChangeForm
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    model = Profile

    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 5px;" />', obj.avatar.url)
        else:
            default_avatar_url = static('img/elements/no_photo.webp')
            return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 5px;" />', default_avatar_url)

    avatar_tag.short_description = 'Аватар'

    list_display = ('avatar_tag', '__str__', 'position', 'company', 'phone', 'subscription',
                    'is_staff', 'is_active', 'is_superuser',)
    list_display_links = ('__str__', 'avatar_tag',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('Учетная запись', {'fields': ('email', 'password',)}),
        ('Персональные данные', {
         'fields': ('last_name', 'first_name', 'middle_name', 'phone', 'avatar',)}),
        ('Место работы', {'fields': ('company', 'position',)}),
        ('Согласие на обработку персональных данных',
         {'fields': ('agreement', 'subscription',)}),
        ('Активность', {'fields': ('date_joined', 'last_login',)}),
        ('Группы', {'fields': ('groups',)}),
        ('Разрешения', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('last_name', 'first_name',
                     'middle_name', 'email', 'company',)
    ordering = ('last_name', 'first_name', 'middle_name', 'email',)


admin.site.site_title = 'Электронный каталог мебели | Админ-панель'
admin.site.site_header = 'Электронный каталог мебели | Админ-панель'
