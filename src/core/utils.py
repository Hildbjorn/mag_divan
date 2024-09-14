import datetime
import os
import re

from uuid import uuid4
from django.core.mail import send_mail
import telepot
import pytils as pytils
from PIL import Image
from slugify import slugify

from django.conf import settings

# Диапазон лет плюс-минус 100 лет от текущего года
YEARS = [(r, r) for r in range(datetime.date.today().year -
                               100, datetime.date.today().year + 101)]

# Диапазон чисел от 1 до 20
PERIOD = [(r, r) for r in range(1, 21)]


def pluralize_russian(n, singular, dual, plural):
    """
    Склоненяет слова в зависимости от числительного в русском языке.
    """
    if n % 10 == 1 and n % 100 != 11:
        return (n, singular)
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        return (n, dual)
    else:
        return (n, plural)


def upload_to(instance, filename):
    """
    Функция для генерации пути загрузки файла, используя slugify для имени файла.
    """
    base_path = getattr(instance, 'upload_path', 'uploads/')
    name, ext = os.path.splitext(filename)
    slugified_name = slugify(name)
    return os.path.join(base_path, f'{slugified_name}{ext}').lower()


def get_slug(instance, slug_field_name='slug'):
    """
    Создает уникальный slug для объекта модели.
    """
    model_name = slugify(instance.__class__.__name__)
    slug = f'{model_name}-{uuid4().hex}'
    # Проверяем уникальность slug в модели
    while instance.__class__.objects.filter(**{slug_field_name: slug}).exists():
        slug = f'{model_name}-{uuid4().hex}'
    return slug


def set_correct_avatar_filename(instance, filename):
    """Создает путь к файлу пользователя, используя его email и каталог изображений. Имя файла транслитерируется."""
    value = pytils.translit.translify(u"%s" % filename)
    name, ext = os.path.splitext(value)
    name = re.sub(r"[\W]", "_", name.strip())
    file_name = '{0}{1}'.format(name, ext).lower()

    path = 'user_files/{0}/{1}/'.format(instance.email, 'avatar')
    file_path = path + file_name
    return file_path


def set_furniture_image_filename(instance, filename):
    """Создает путь к изображению мебели, используя тип, подтип, модель и цвет."""
    # Получаем необходимые атрибуты из экземпляра
    furniture_type = instance.furniture_model.type.name  # Тип мебели
    model_name = instance.furniture_model.name  # Модель мебели
    color_name = instance.color.name  # Цвет

    # Транслитерация названий
    furniture_type = pytils.translit.translify(furniture_type)
    model_name = pytils.translit.translify(model_name)
    color_name = pytils.translit.translify(color_name)

    # Формирование имени файла
    value = pytils.translit.translify(u"%s" % filename)
    name, ext = os.path.splitext(value)
    name = re.sub(r"[\W]", "_", name.strip())
    file_name = '{0}{1}'.format(name, ext).lower()

    # Формирование пути
    path = f'furniture_images/{furniture_type}/{model_name}/{color_name}/'
    file_path = os.path.join(path, file_name)

    return file_path


def resize_and_crop_image(image_path, max_size):
    img = Image.open(image_path)
    width, height = img.size

    # Определите, какая сторона изображения меньше
    if width < height:
        # Установите ширину в max_size[0], сохраняя пропорции
        new_width = max_size[0]
        new_height = int((new_width / width) * height)
    else:
        # Установите высоту в max_size[1], сохраняя пропорции
        new_height = max_size[1]
        new_width = int((new_height / height) * width)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Обрезка изображения
    left = (new_width - max_size[0]) / 2
    right = (new_width + max_size[0]) / 2
    top = (new_height - max_size[1]) / 2
    bottom = (new_height + max_size[1]) / 2
    img = img.crop((left, top, right, bottom))

    img.save(image_path)


class Communications:
    """Класс коммуникаций"""

    def __init__(self, subject=None, html_message=None, html_message_to_team=None, email=None, t_massage=None):
        self.subject = subject
        self.html_message = html_message
        self.html_message_to_team = html_message_to_team
        self.email = email
        self.default_from_email = settings.DEFAULT_FROM_EMAIL

        self.message = t_massage
        self.admin_telegram_id = settings.ADMIN_TELEGRAM_ID
        self.telegram_token = settings.TELEGRAM_TOKEN
        self.telegramBot = telepot.Bot(self.telegram_token)

    def email_settings_ready(self):
        """Проверяет, заданы ли необходимые настройки для отправки email."""
        return all([
            settings.EMAIL_HOST,
            settings.EMAIL_PORT,
            settings.EMAIL_HOST_USER,
            settings.EMAIL_HOST_PASSWORD,
            settings.DEFAULT_FROM_EMAIL
        ])

    def telegram_to_team(self):
        """Отправка сообщения в Телеграм сотрудникам."""
        # Проверка наличия настроек
        if not self.telegram_token or not self.admin_telegram_id:
            print("\nTelegram команде (настройки не заданы)")
            print("————")
            print(self.message)
            return
        # Отправка сообщений, если настройки заданы
        for user_id in self.admin_telegram_id:
            self.telegramBot.sendMessage(
                user_id, self.message, parse_mode='html'
            )

    def email_to_customer(self):
        """ Отправка письма пользователю или вывод в консоль, если настройки не указаны """
        if self.email_settings_ready():
            # Отправляем письмо, если настройки указаны
            send_mail(
                self.subject,
                self.html_message,
                self.default_from_email,
                [self.email],
                html_message=self.html_message
            )
        else:
            # Выводим сообщение в консоль, если настройки не указаны
            print("\nПисьмо клиенту (настройки не заданы):")
            print("————")
            print(f"Subject: {self.subject}")
            print(f"To: {self.email}")
            print(f"Message: {self.html_message}")

    def email_to_team(self):
        """Отправка письма всем суперпользователям и пользователям со статусом staff."""
        # Получаем всех пользователей, которые являются суперпользователями и имеют статус is_staff
        users = 'users.Profile'.objects.filter(
            is_superuser=True, is_staff=True)

        # Извлекаем адреса электронной почты этих пользователей
        recipients = [user.email for user in users if user.email]

        if recipients:
            if self.email_settings_ready():
                # Отправляем письмо, если настройки указаны
                send_mail(
                    self.subject,
                    self.html_message_to_team,
                    self.default_from_email,
                    recipients,
                    html_message=self.html_message_to_team
                )
            else:
                # Выводим сообщение в консоль, если настройки не указаны
                print("\nПисьмо команде (настройки не заданы):")
                print("————")
                print(f"Subject: {self.subject}")
                print(f"To: {', '.join(recipients)}")
                print(f"Message: {self.html_message_to_team}")
        else:
            print("Не найдены суперпользователи или пользователи со статусом staff с указанными адресами электронной почты.")
