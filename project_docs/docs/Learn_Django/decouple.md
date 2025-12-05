# Decouple

<div class="" dir="rtl">
  
  المكتبة دي مفيدة جدًا عشان تفصل المعلومات الحساسة (زي الـ SECRET_KEY، بيانات قواعد البيانات، API keys، …) عن كود المشروع نفسه.
  
</div>

## Website

[Decouple](https://pypi.org/project/python-decouple/)

## Install

<div class="" dir="rtl">
1️⃣ ثابت المكتبة
</div>

```
pip install python-decouple
```

## Create

<div class="" dir="rtl">
2️⃣ أنشئ ملف .env في جذر المشروع

في نفس مسار manage.py، أنشئ ملف جديد اسمه:

</div>

```
.env
```

```python
SECRET_KEY=django-insecure-sgt+4e#-f%qpz%3p8jd9z4%)2b^8@+v40m!ws^j^t(l%m-io7x
DEBUG=True
DB_NAME=myprojectdb
DB_USER=myprojectuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432
GOOGLE_OAUTH_CLIENT_ID=300012533519-3buflbtimhmardd7t1ou7tc9qs6p6tks.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=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
```

## Edit

<div class="" dir="rtl">
3️⃣ عدّل settings.py

استورد المكتبة في بداية الملف:

</div>

```python
from decouple import config

```

<div class="" dir="rtl">
وبدل القيم الثابتة بالمتغيرات:
</div>

```python
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

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

```

<div class="" dir="rtl">
4️⃣ تجاهل ملف .env

عشان تحميه من الصعود للـ git, أضف .env إلى .gitignore:

</div>

```
.env
*.env
.env.local
.env.production

```
