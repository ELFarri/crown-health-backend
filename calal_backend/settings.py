# ============================================
# CALAL SETTINGS - الملف الرئيسي للإعدادات
# ============================================

from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# 👈 إضافة هذه السطر المهم
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECRET_KEY = 'django-insecure-calal-secret-key-2024'
DEBUG = True
ALLOWED_HOSTS = ["*", "127.0.0.1", ".onrender.com"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    
    # Calal Apps 
    'users',      
    'foods',      
    'nutrition',  
    'workouts',   
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'calal_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'calal_backend.wsgi.application'

# 🔥 DATABASE CONFIGURATION (SQLite for Cloud Stability)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 👤 Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# 🌐 REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # 👈 List مش tuple
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# 🔓 CORS للـ Flutter
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# أضف هذا في settings.py بعد CORS_ALLOW_ALL_ORIGINS = True

# 🔥 CORS للـ Flutter (مهم جداً)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",  # Flutter Web
    "http://10.0.2.2:8000",   # Flutter Android Emulator
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://172.20.10.3:8000",
]

CORS_ALLOW_ALL_ORIGINS = True  # مؤقت للاختبار
CORS_ALLOW_CREDENTIALS = True

# 🔥 Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 📁 Static Files ✅
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# JWT Token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# 👈 نهاية الإعدادات