# 📄 [ users_accounts/settings.py ] ملف


from decouple import config
from datetime import timedelta

import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')


# DEBUG = True
DEBUG = config('DEBUG', default=False, cast=bool)


# 1️⃣ Django_Core
# WEBSITE_URL = "http://127.0.0.1:8000"
WEBSITE_URL = config(
    "WEBSITE_URL",
    default="http://127.0.0.1:8000",
)

FRONTEND_URL = config(
    "FRONTEND_URL",
    default="http://localhost:5173",
)
AUTH_USER_MODEL = "users_accounts.User"
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.1.5",
    "172.23.232.133",
    "localhost:5173",
    "localhost:5174",
    "global-style-for-video.pages.dev"
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://192.168.1.5:5173",
    "http://192.168.1.5:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    'https://global-style-for-video.pages.dev'
]
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

CORS_ALLOW_ALL_ORIGINS = False
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
    #
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    # # Pagination
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": 10,

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
    "https://global-style-for-video.pages.dev",
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

# 8️⃣
ASGI_APPLICATION = "backend_django.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# 9️⃣ Celery
# MCP Configuration (اختياري — الـ defaults كويسة)
# requests per session per minute
MCP_RATE_LIMIT_PER_MINUTE = 60
REDIS_HOST = config(
    "REDIS_HOST",
    default="127.0.0.1",
)

REDIS_PORT = config(
    "REDIS_PORT",
    default="6379",
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://127.0.0.1:6379/1",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}


# CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = config(
    "CELERY_BROKER_URL",
    default="redis://127.0.0.1:6379/0",
)

# CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = config(
    "CELERY_RESULT_BACKEND",
    default="redis://127.0.0.1:6379/0",
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"


INSTALLED_APPS = [
    # 8️⃣
    "daphne",
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 8️⃣
    "channels",
    # Apps
    'users_accounts',
    "notification",
    # Ecommerce [ Marketplace ]
    "vendor",
    "product",
    #
    "client",
    # "marketplace.vendor",
    "automation",
    "explain",
    "mcp_server.apps.McpServerConfig",
    "ai_app",

    # 📚 Libraries
    # 1️⃣ djangorestframework [DRF]
    'rest_framework',
    'rest_framework.authtoken',
    # 2️⃣ djangorestframework-simplejwt [Auth]
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    #
    # 'dj_rest_auth',
    # 3️⃣ django-allauth [Allauth]
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

    # 9️⃣ Celery
    "django_celery_results",
    "django_celery_beat",

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
        # 'HOST': config('DB_HOST', default='localhost'),
        "HOST": config("DB_HOST"),
        'PORT': config('DB_PORT', default='5432'),
    }
}

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


#
# settings.py
AI_CONFIG = {
    "OLLAMA_URL": "http://localhost:11434",
    "OLLAMA_MODEL": "gemma2:2b",  # موديل خفيف وسريع
    "OPENROUTER_API_KEY": "YOUR_KEY_HERE",
    "DEFAULT_PROVIDER": "ollama",  # القيمة الافتراضية
}

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


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


"""

تصرف كـ AI Architect + Senior Backend Engineer + Mentor تقني.

هدفك:
مساعدتي في بناء مشروع Django باسم ai_app باستخدام:
- Ollama (Local LLMs)
- MCP (Model Context Protocol)
- OpenRouter (API routing for models)

⏱️ القيود:
أريد خلال 10 ساعات فقط:
1. أفهم الفكرة العامة للمشروع
2. أتعرف على هيكل الملفات (Architecture)
3. أعرف وظيفة كل ملف بالتفصيل
4. أفهم كيف الأكواد تخدم Logic المشروع
5. أقدر أطور وأعدل بنفسي بعد ذلك

---

🧠 أسلوب الشرح المطلوب:

اتبع هذا الأسلوب في كل جزء:
1. ابدأ بتوضيح الفكرة ببساطة (ليه بنعمل كده؟)
2. تشبيه بسيط من الواقع
3. شرح الهيكل
4. مثال عملي
5. أخطاء شائعة
6. ربط كل جزء بالمشروع ككل

---

📦 المطلوب تنفيذه:

## 1. إنشاء المشروع
ابدأ من:
python manage.py startapp ai_app

ثم:
- إعداد Django project
- ربط app
- إعداد settings

---

## 2. Architecture (مهم جدًا)
اعرض:
- هيكل المشروع بالكامل (Tree Structure)
- تقسيم Layers:
  - views
  - services
  - ai layer
  - integrations (ollama / openrouter / mcp)

وشرح:
- كل ملف بيعمل ايه
- ليه موجود
- ازاي بيخدم المشروع

---

## 3. AI Integration

### Ollama:
- تشغيل موديل (phi أو gemma)
- إرسال prompt
- استقبال response

### OpenRouter:
- استخدام API
- مقارنة مع Ollama

### MCP:
- شرح الفكرة
- ازاي نستخدمه في orchestration

---

## 4. Logic المشروع

ابني مشروع عملي مثل:
"AI Assistant for Automation"

يعمل:
- تنفيذ أوامر (فتح برامج / نسخ ملفات)
- تحليل طلب المستخدم
- اختيار الأداة المناسبة
- تنفيذ Task

اشرح:
- flow من user → AI → execution
- decision making

---

## 5. Code Implementation

لكل جزء:
- اكتب الكود
- اشرح كل سطر مهم
- اربط بين الملفات

---

## 6. Workflow (مهم جدًا)
ارسم flow:
User Input → AI → Tool Selection → Execution → Result

---

## 7. ai.md Documentation

أنشئ ملف ai.md يحتوي على:
- شرح كامل من البداية للنهاية
- كيف تستخدم AI في المشاريع
- أفضل الممارسات
- أخطاء يجب تجنبها
- طرق تطوير المشروع

---

## 8. Learning System (Meta Learning)

ساعدني أفهم:
- كيف أفكر عند استخدام AI
- كيف أبني systems مش مجرد calls
- كيف أطور المشروع لاحقًا

---

## 9. Output Format

قسم الإجابة إلى مراحل:

Stage 1: الفكرة  
Stage 2: الهيكل  
Stage 3: AI Integration  
Stage 4: التنفيذ  
Stage 5: التطوير  

---

🎯 الهدف النهائي:
مش مجرد تنفيذ…  
عايز أفهم:
- Architecture
- Thinking Process
- AI System Design

وخلال 10 ساعات أكون قادر:
- أبني المشروع
- أعدّل عليه
- أطور أفكار مشابهة

ابدأ خطوة خطوة بدون قفز

التركيذ فى البداية الترتيب
Ollama
MCP
OpenRouter

"""


"""
للـ cache
pip install django-redis
للـ AI schema
pip install pydantic
إذا تستخدم ASGI
pip install uvicorn
للـ AI agent
pip install openai
pip install celery
pip install redis
pip install django-celery-beat
pip install django-celery-results
pip install langchain langchain-openai langchain-community ollama
"""
