## Django

### 1️⃣ Install

#### 1️⃣ Install 📚

```cmd
pip install django-allauth
```

### 2️⃣ Setup 🛠️

```python
# 4️⃣ django-allauth
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "300012533519-3buflbtimhmardd7t1ou7tc9qs6p6tks.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        }
    }
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
LOGIN_REDIRECT_URL = "http://127.0.0.1:8000"
LOGOUT_REDIRECT_URL = "/accounts/login/"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_ADAPTER = "users_accounts.adapter.MySocialAccountAdapter"
```

```python
INSTALLED_APPS = [
  # Libraries
  'django.contrib.sites',
  'allauth',
  'allauth.account',
  'allauth.socialaccount',
  'allauth.socialaccount.providers.google',
]
```

```python
MIDDLEWARE = [
  # Add AccountMiddleware for allauth
  "allauth.account.middleware.AccountMiddleware",
]
```

```python
# 📄 [ backend_django/urls.py ] ملف
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path("accounts/", include("allauth.urls")),
]

```

```python

```
