"""
██████╗     ███████╗     ██████╗     Django Starter Generator -
██╔══██╗    ██╔════╝    ██╔════╝     приложение для автоматизации
██║  ██║    ███████╗    ██║  ███╗    создания, настройки и первого
██║  ██║    ╚════██║    ██║   ██║    запуска проектов на Django.
██████╔╝    ███████║    ╚██████╔╝
╚═════╝     ╚══════╝     ╚═════╝     Copyright (c) 2024 Artem Fomin
Настройки Django для проекта core
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Построение пути внутри проекта следующим образом: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Построение пути к файлу .env
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Быстрые настройки для разработки - не подходят для производства.
# Подробнее: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', '').lower() in ['true', '1', 'yes']

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# Определение приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'sass_processor',
    'widget_tweaks',
    'users',
    'catalog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES_BASE_DIR = os.path.join(BASE_DIR, 'templates')
# Шаблоны Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_BASE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Путь к настройкам wsgi
WSGI_APPLICATION = 'core.wsgi.application'

# База данных
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.environ.get('DATABASE_NAME'),
    }
}

# Проверка пароля
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Использование класса Profile
AUTH_USER_MODEL = 'users.Profile'

# Перенаправление на домашний URL после входа (по умолчанию перенаправляет на /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

# Интернационализация
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Статические файлы (CSS, JavaScript, Img, Fonts)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

STATICFILES_DIRS = [
    BASE_DIR / "static",  # Убедитесь, что путь указан правильно
]

STATIC_ROOT = BASE_DIR.joinpath('staticfiles')

STATIC_URL = '/static/'

# Папка итогового хранения css и js
SASS_PROCESSOR_ROOT = STATIC_ROOT

# Настройки Django-Bootstrap
BOOTSTRAP5 = {
    "javascript_url": {
        "url": "/static/bootstrap/js/bootstrap.bundle.min.js",
    },
}

# Насипройки иконок Bootstrap в Django/
DJANGO_ICONS = {
    "DEFAULT": {
        "renderer": "django_icons_bootstrap_icons.BootstrapIconRenderer"
    }
}

# Медиафайлы (фото, презентации и т.д.)
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR.joinpath('media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки электронной почты Stratman.pro
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '').lower() in [
    'true', '1', 'yes']
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', '').lower() in [
    'true', '1', 'yes']

# Настройки Telegtam Stratman.pro
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Мои настройки Telegram
ADMIN_TELEGRAM_ID = os.getenv('ADMIN_TELEGRAM_ID')
if ADMIN_TELEGRAM_ID:
    ADMIN_TELEGRAM_ID = [int(id) for id in ADMIN_TELEGRAM_ID.split(',')]
else:
    ADMIN_TELEGRAM_ID = []
