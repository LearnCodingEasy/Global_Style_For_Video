# 📄 [ users_accounts/settings.py ] ملف


from decouple import config
from datetime import timedelta

import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')


DEBUG = True
# DEBUG = config('DEBUG', default=False, cast=bool)


# 1️⃣ Django_Core
WEBSITE_URL = "http://127.0.0.1:8000"
AUTH_USER_MODEL = "users_accounts.User"
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.1.5",
    "172.23.232.133",
    "localhost:5173",
    "localhost:5174",
    'https://global-style-for-video.pages.dev/'
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://192.168.1.5:5173",
    "http://192.168.1.5:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    'https://global-style-for-video.pages.dev/'
]
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

CORS_ALLOW_ALL_ORIGINS = True
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


# 2️⃣ simplejwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
}

# 3️⃣ rest_framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}
# 0️⃣1️⃣ Document
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


# 4️⃣ django-allauth
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config('GOOGLE_OAUTH_CLIENT_ID'),
            "secret": config('GOOGLE_OAUTH_CLIENT_SECRET'),
            "key": "",
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,

    },

}
"""
"none" ➝ من غير تحقق.
"optional" ➝ التحقق اختياري.
"mandatory" ➝ لازم يتحقق عشان الحساب يتفعل ✅.
"""
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_FIELDS = ["email", "name", ]
ACCOUNT_LOGIN_METHODS = {"email"}
# LOGIN_REDIRECT_URL = "/"
# LOGIN_REDIRECT_URL = 'http://localhost:5173/'
# LOGIN_REDIRECT_URL = 'http://localhost:5173/about/'
# LOGIN_REDIRECT_URL = '/accounts/google/login/callback/'
LOGIN_REDIRECT_URL = 'http://localhost:5173/auth/callback'
LOGOUT_REDIRECT_URL = "/accounts/login/"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_ADAPTER = "users_accounts.adapter.MySocialAccountAdapter"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 أيام
SESSION_SAVE_EVERY_REQUEST = True
ACCOUNT_LOGOUT_REDIRECT_URL = 'http://localhost:5173/login'
ACCOUNT_SIGNUP_REDIRECT_URL = 'http://localhost:5173'
SOCIALACCOUNT_LOGIN_REDIRECT_URL = 'http://localhost:5173/auth-callback/'
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
print(f"✅ Settings loaded Django")
print(f"✅ AUTH_USER_MODEL: {AUTH_USER_MODEL}")
print(f"✅ SOCIALACCOUNT_ADAPTER: {SOCIALACCOUNT_ADAPTER}")

# 5️⃣ Djoser
DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user_create': 'users_accounts.serializers.UserSerializer',
        'user': 'users_accounts.serializers.UserSerializer',
    }
}

# 6️⃣ corsheaders
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://192.168.1.5:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",

]
CORS_ALLOW_CREDENTIALS = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = None


# 7️⃣ Debug Toolbar settings
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False,
}

#
REST_USE_JWT = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # App
    'users_accounts',
    "notification",
    "vendor",
    "product",

    # "marketplace.vendor",



    # 📚 Libraries
    # 1️⃣ djangorestframework
    'rest_framework',
    'rest_framework.authtoken',
    # 2️⃣ djangorestframework-simplejwt
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    #
    # 'dj_rest_auth',
    # 3️⃣ django-allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 4️⃣ Djoser
    "djoser",
    # 5️⃣ corsheaders
    "corsheaders",
    # 6️⃣ debug_toolbar
    'debug_toolbar',
    # 7️⃣
    'drf_spectacular',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Libraries [ Django Cors Headers ]
    "corsheaders.middleware.CorsMiddleware",
    # Add AccountMiddleware for allauth
    "allauth.account.middleware.AccountMiddleware",
    # debug_toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # My Middleware for debug
    # 'users_accounts.middleware.LogRequestResponseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_django.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),

    }
}

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


# Access path for static files (such as CSS and JavaScript files)
STATIC_URL = "static/"
# Access path for media files (such as images and files uploaded by users)
MEDIA_URL = "media/"
# Specify a "media" folder in the project to store uploaded media files
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
