# =====================================================================================================================
#                                       PROJET CALAL - django settings.py
#                 CONFIGURATION DU BACKEND AVEC EXPLICATIONS TECHNIQUES DÉTAILLÉES (EN ANGLAIS)
# =====================================================================================================================

# Path module from Python's standard library to manipulate filesystem paths in a platform-independent way.
from pathlib import Path

# OS module from standard library to access environment variables and filesystem paths.
import os

# Timedelta from datetime module to configure time durations (used for JWT token lifetimes).
from datetime import timedelta

# =====================================================================================================================
# 📁 BASE DIRECTORY CONFIGURATION
# =====================================================================================================================

# Path(__file__) returns the absolute path of this settings.py file.
# .resolve() resolves symlinks and normalizes the path.
# .parent gets the containing folder ('calal_backend' configuration folder).
# .parent.parent goes one level up to the root project directory ('c:\Users\mouat\Desktop\MY_PRINCESS_PROJECT\calal_backend').
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================================================================================
# 🔑 SECURITY & UTILITY SETTINGS
# =====================================================================================================================

# Defines the default primary key field type for all models that do not explicitly declare a primary key.
# BigAutoField is a 64-bit integer auto-incrementing key (supports up to 9.22 Quintillion records).
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Secret key used for cryptographic signing. Critical for signing sessions, password resets, and JWT tokens.
SECRET_KEY = 'django-insecure-calal-secret-key-2024'

# Debug mode switch. When True, Django displays detailed error pages and traceback logs on unhandled exceptions.
# WARNING: Must be set to False in production environments to avoid exposing sensitive server details.
DEBUG = True

# Security filter of host headers. Django will reject requests whose Host header doesn't match this list.
# "*" allows any hostname (useful for testing). The other strings allow local and production hostnames.
ALLOWED_HOSTS = ["*", "mouatazfarri.pythonanywhere.com", "127.0.0.1", ".onrender.com"]

# =====================================================================================================================
# 📦 INSTALLED APPLICATIONS REGISTER
# =====================================================================================================================

# Central registry of all active modules in this Django project.
INSTALLED_APPS = [
    # --- 1. Core Django Built-in Apps ---
    'django.contrib.admin',        # Admin panel: generates the automatic database administration web interface.
    'django.contrib.auth',         # Authentication system: handles user login, permissions, and groups.
    'django.contrib.contenttypes', # Contenttypes framework: tracks all database models and establishes dynamic relations.
    'django.contrib.sessions',     # Session framework: stores user login sessions across requests (used by admin panel).
    'django.contrib.messages',     # Messaging framework: allows temporary cookie-based user notifications.
    'django.contrib.staticfiles',  # Static files utility: gathers CSS, JS, and image assets for the admin interface.
    
    # --- 2. Third-Party Packages ---
    'corsheaders',                 # Cross-Origin Resource Sharing handler: permits Flutter to make remote HTTP requests.
    'rest_framework',              # Django REST Framework (DRF): transforms Django into a RESTful JSON API provider.
    'rest_framework_simplejwt',    # SimpleJWT: orchestrates JWT authentication, issuing stateless access/refresh tokens.
    
    # --- 3. Custom Project Apps (Local Business Logic) ---
    'users',                       # Users app: manages CustomUser model, biological vectors, registration and login.
    'foods',                       # Foods app: hosts the food ingredient database for user autocomplete searches.
    'nutrition',                   # Nutrition app: logs daily meals and performs macronutrient aggregation.
    'workouts',                    # Workouts app: logs gym workouts, sets, reps, and tracks training sessions.
]

# =====================================================================================================================
# ⚙️ MIDDLEWARE CHAIN
# =====================================================================================================================

# List of hooks executed sequentially during request/response cycles. Order is critical.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',           # intercept and append CORS headers to responses (must be first).
    'django.middleware.security.SecurityMiddleware',   # injects defensive HTTP security headers and handles SSL checks.
    'whitenoise.middleware.WhiteNoiseMiddleware',     # serves compressed static files directly in production.
    'django.contrib.sessions.middleware.SessionMiddleware', # reads/writes session IDs inside request cookies.
    'django.middleware.common.CommonMiddleware',       # handles basic routing tasks like appending trailing slashes.
    'django.middleware.csrf.CsrfViewMiddleware',       # prevents Cross-Site Request Forgery attacks on unsafe HTTP methods.
    'django.contrib.auth.middleware.AuthenticationMiddleware', # associates the authenticated user to request.user.
    'django.contrib.messages.middleware.MessageMiddleware',   # processes and flashes feedback messages to views.
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # blocks clickjacking by preventing iframe embedding.
]

# =====================================================================================================================
# 🛣️ URLS & TEMPLATES CONFIGURATION
# =====================================================================================================================

# The Python import path to the root URL router config file of the project.
ROOT_URLCONF = 'calal_backend.urls'

# Configuration settings for rendering HTML files (mainly used for the Admin console).
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # Template engine driver (Django templates).
        'DIRS': [BASE_DIR / 'templates'],                            # Custom folders to search for HTML files.
        'APP_DIRS': True,                                           # Tells Django to check inside app directories.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',          # passes debug variables into templates.
                'django.template.context_processors.request',        # passes the active HTTP request object.
                'django.contrib.auth.context_processors.auth',       # passes the active user session (request.user).
                'django.contrib.messages.context_processors.messages', # passes flash notifications.
            ],
        },
    },
]

# WSGI (Web Server Gateway Interface) entrypoint. Used by production web servers to run the app.
WSGI_APPLICATION = 'calal_backend.wsgi.application'

# =====================================================================================================================
# 🗄️ DATABASE persistence LAYER
# =====================================================================================================================

# Database settings. Currently configured to SQLite for portability and compatibility with free hosting plans.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Database engine: SQLite.
        'NAME': BASE_DIR / 'db.sqlite3',       # Path to the database file on disk.
    }
}

# =====================================================================================================================
# 👤 USER AUTHENTICATION OVERRIDE
# =====================================================================================================================

# Overrides Django's default User model with our custom biometric model.
AUTH_USER_MODEL = 'users.CustomUser'

# =====================================================================================================================
# 🌐 DJANGO REST FRAMEWORK (DRF) SETTINGS
# =====================================================================================================================

# Global configuration dictionary for Django REST Framework APIs.
REST_FRAMEWORK = {
    # JWT authentication filter:
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication', # validates simplejwt tokens from incoming requests.
    ],
    # Default endpoint permissions:
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Allows public registration/login endpoints.
    ],
    # Renderer configuration:
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer', # Forces DRF to serialize and return responses in JSON.
    ]
}

# =====================================================================================================================
# 🔓 CROSS-ORIGIN RESOURCE SHARING (CORS) SETTINGS
# =====================================================================================================================

# Allows frontend clients hosted on different origins (like Flutter) to fetch data from this server.
CORS_ALLOW_ALL_ORIGINS = True   # Enables connections from any origin.
CORS_ALLOW_CREDENTIALS = True  # Allows authorization headers and cookies during cross-origin calls.

# HTTP methods authorized during cross-origin requests:
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Request headers authorized during cross-origin requests:
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization", # Required for sending "Bearer <JWT_TOKEN>" in HTTP headers.
    "content-type",  # Required for sending JSON data in the HTTP body.
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# =====================================================================================================================
# 📁 MEDIA & STATIC FILES MANAGEMENT
# =====================================================================================================================

# --- Media files (User uploads like biometric progress pictures) ---
MEDIA_URL = '/media/'                            # URL prefix used in the browser to query media files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    # Directory path in the filesystem where uploaded media is written.

# --- Static files (Developer assets like CSS stylesheets, JS, Admin icons) ---
STATIC_URL = '/static/'                          # URL prefix used to serve static assets.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Target folder for collectstatic. Used by PythonAnywhere to serve assets.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Folders containing active development static assets.

# =====================================================================================================================
# 🔑 JSON WEB TOKEN (JWT) SECURITY SCHEME
# =====================================================================================================================

# Configuration for SimpleJWT library.
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Access token lifespan (invalidated after 1 hour for security).
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Refresh token lifespan (used to request new access tokens for 1 day).
}

# =====================================================================================================================
# 🌐 TIMEZONE & LOCALIZATION SETTINGS
# =====================================================================================================================
TIME_ZONE = 'Europe/Paris'
USE_TZ = True

# =====================================================================================================================
# END OF SETTINGS CONFIGURATION
# =====================================================================================================================