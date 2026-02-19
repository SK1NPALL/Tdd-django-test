"""
Django settings for superlists project.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configuration สำหรับ Deployment ---
# เช็คว่ารันอยู่บน Production (Render) หรือไม่
IS_PRODUCTION = "DJANGO_DEBUG_FALSE" in os.environ

if IS_PRODUCTION:
    DEBUG = False
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
    # ดึงค่า Allowed Hosts จาก Environment หรือใช้ default ของ Render
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOST", ".onrender.com").split(" ")
else:
    DEBUG = True
    SECRET_KEY = "insecure-key-for-dev"
    ALLOWED_HOSTS = ['*']

# ตั้งค่า CSRF เพื่อให้ส่ง Form บน Render ได้
CSRF_TRUSTED_ORIGINS = [
    'https://kbkdev.works',
    'https://*.onrender.com',
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin", # เปิดไว้เพื่อใช้จัดการ DB แทน Adminer
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "lists",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # จัดการ Static Files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'superlists.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'superlists.wsgi.application'

# Database Setup
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# dj_database_url จะอ่านค่าจาก environment variable ชื่อ DATABASE_URL โดยอัตโนมัติ
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Logging (สำหรับดู log บนหน้า Dashboard ของ Render)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "root": {"handlers": ["console"], "level": "INFO"},
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# การตั้งค่า Storage สำหรับ WhiteNoise (Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'