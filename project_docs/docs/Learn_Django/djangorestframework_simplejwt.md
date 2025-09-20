## Django

### 1️⃣ Install

#### 1️⃣ Install 📚

```cmd
pip install djangorestframework-simplejwt
```

### 2️⃣ Setup 🛠️

<div dir="rtl" style="font-size:1vw">

- ACCESS_TOKEN_LIFETIME: مدة صلاحية توكن الوصول (Access token) لمدة 30 يوم.

- REFRESH_TOKEN_LIFETIME: مدة صلاحية توكن التحديث (Refresh token) لمدة 180 يوم.

- ROTATE_REFRESH_TOKENS: لو True، كل مرة تستخدم فيها refresh token يتم إبطال القديم وإصدار جديد، هنا معطّل.

</div>

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
}
```

```python
# Django REST Framework settings for identity and permissions verification
# Use JWT for identity verification
# Allow only authenticated users
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
```

```python
INSTALLED_APPS = [
  # Libraries
  "rest_framework_simplejwt",
]
```

### 3️⃣ used

<div dir="rtl" style="font-size:1.5vw">
  تحديث حالة المستخدم فى 
  
  تسجيل الدخول
  
  تسجيل الخروج
</div>

```python
# users_accounts/views.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.shortcuts import get_object_or_404

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # تحديث is_online عند تسجيل الدخول
        user = self.user
        user.is_online = True
        user.save(update_fields=['is_online'])

        return data

# ✅ تسجيل الدخول
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ✅ تسجيل الخروج
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Blacklist refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # تحديث حالة المستخدم
            user = request.user
            if user and user.is_authenticated:
                user.is_online = False
                user.save(update_fields=["is_online"])

            return Response({"message": "تم تسجيل الخروج بنجاح"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

```

```python
# 📄 [ backend_django/urls.py ] ملف
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from users_accounts.views import MyTokenObtainPairView,  LogoutAPIView

urlpatterns = [
    # simplejwt
    path("api/login/", MyTokenObtainPairView.as_view(), name="token_obtain"),
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", LogoutAPIView.as_view(), name="logout"),
    # Admin
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

```python

# 📝 [users_accounts/signals.py] صفحة

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import User


@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    user.is_online = True
    user.save(update_fields=['is_online'])


@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    user.is_online = False
    user.save(update_fields=['is_online'])

```
