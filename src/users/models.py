import os
import shutil
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.utils import resize_and_crop_image, set_correct_avatar_filename

from .managers import ProfileManager


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('E-mail'), unique=True)

    avatar = models.ImageField(upload_to=set_correct_avatar_filename,
                               null=True,
                               blank=True,
                               verbose_name='Аватар')
    max_size = (300, 300)

    first_name = models.CharField(max_length=100,
                                  verbose_name='Имя',
                                  null=True,
                                  blank=True)

    middle_name = models.CharField(max_length=100,
                                   verbose_name='Отчество',
                                   null=True,
                                   blank=True)

    last_name = models.CharField(max_length=100,
                                 verbose_name='Фамилия',
                                 null=True,
                                 blank=True)

    phone = models.CharField(max_length=20,
                             unique=False,
                             null=True,
                             blank=True,
                             verbose_name='Телефон',
                             db_index=True)

    company = models.CharField(max_length=255,
                               verbose_name='Компания',
                               null=True,
                               blank=True)

    position = models.CharField(max_length=255,
                                verbose_name='Должность',
                                null=True,
                                blank=True)

    agreement = models.BooleanField(default=True,
                                    verbose_name='Согласие на обработку персональных данных')

    subscription = models.BooleanField(default=False,
                                       verbose_name='Подписка на рассылку')

    is_staff = models.BooleanField(default=False,
                                   verbose_name='В команде')

    is_active = models.BooleanField(default=True,
                                    verbose_name='Активный')

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ProfileManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            resize_and_crop_image(self.avatar.path, self.max_size)
            self.avatar = self.avatar
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Определение пути к аватару
        avatar_path = self.avatar.path if self.avatar else None
        # Определение пути к папке пользователя
        user_folder_path = os.path.join('media', 'user_files', self.email)
        # Вызов суперметода для удаления объекта из базы данных
        super().delete(*args, **kwargs)
        # Удаление файла аватара, если он существует
        if avatar_path and os.path.isfile(avatar_path):
            try:
                os.remove(avatar_path)
            except Exception as e:
                print('Удаление файла аватара не удалось', e)
        # Удаление папки пользователя, если она существует
        if os.path.isdir(user_folder_path):
            try:
                shutil.rmtree(user_folder_path)
            except Exception as e:
                print('Удаление папки пользователя не удалось', e)

    def __str__(self):
        if not self.first_name or not self.last_name:
            fio = str(self.email)
        elif not self.middle_name:
            fio = str(self.last_name) + " " + str(self.first_name)
        else:
            fio = str(self.last_name) + " " + \
                str(self.first_name) + " " + str(self.middle_name)
        return fio

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['last_name', 'first_name', 'middle_name']
