"""
Django settings for SDMAS_django_nextjs project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v0$4$#5yasj5wa5o=m$$3_#gy@j)*n*tpz(6g4k+q9c!+$j4bk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'SDMAS',
    # 'authen',
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]


CORS_ALLOW_ALL_ORIGINS = True  # อนุญาตให้ทุกโดเมนเรียก API (ใช้เฉพาะตอน Dev)

ROOT_URLCONF = 'SDMAS_django_nextjs.urls'

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

WSGI_APPLICATION = 'SDMAS_django_nextjs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "SDMAS",
        "USER": "postgres",
        "PASSWORD": "0930038864",
        "HOST": "localhost",
        "PORT": "8000",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

# ทำหน้าที่เป็นแบ็กเอนด์ในการส่งอีเมล โดยโปรโตคอล SMTP (Simple Mail Transfer Protocol) จะถูกใช้ในการส่งอีเมล
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# กำหนด EMAIL_HOST ให้เป็น 'smtp.gmail.com' ซึ่งเป็นเซิร์ฟเวอร์ SMTP ของ Gmail หมายความว่า Django จะใช้ Gmail เป็นตัวกลางในการส่งอีเมลออกจากระบบ
EMAIL_HOST = 'smtp.gmail.com'
# กำหนดพอร์ตของเซิร์ฟเวอร์ SMTP ที่จะใช้ในการเชื่อมต่อกับ Gmail พอร์ต 587 เป็นพอร์ตที่ใช้สำหรับการเชื่อมต่อที่เข้ารหัส TLS (Transport Layer Security) ซึ่งเป็นมาตรฐานสำหรับการส่งข้อมูลที่ปลอดภัยผ่านเครือข่าย
EMAIL_PORT = 587
# กำหนดให้เปิดใช้งาน TLS ซึ่งเป็นการเข้ารหัสข้อมูลระหว่างการส่งข้อมูลผ่าน SMTP TLS จะช่วยปกป้องข้อมูลที่ส่งผ่านเครือข่ายจากการถูกดักฟังหรือแก้ไข
EMAIL_USE_TLS = True
# กำหนดชื่อผู้ใช้ (อีเมล) สำหรับบัญชี Gmail ที่จะใช้ส่งอีเมล (สร้างเอง)
EMAIL_HOST_USER = 'sdmas.notfication.noreply@gmail.com'
# รหัสผ่านสำหรับบัญชี Gmail นี้ เพื่อยืนยันตัวตนและอนุญาตให้เซิร์ฟเวอร์ SMTP ของ Gmail ยอมรับการส่งอีเมลจากแอปพลิเคชัน
EMAIL_HOST_PASSWORD = 'bbrk sngt jyvb nyzw'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER