# 📄 [ backend_django/urls.py ] ملف

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf import settings
from django.conf.urls.static import static
from users_accounts.views import MyTokenObtainPairView,  LogoutAPIView, GoogleLoginToJWTView, GoogleAuthInitView
from django.views.generic import RedirectView

from debug_toolbar.toolbar import debug_toolbar_urls

# 0️⃣1️⃣ Document
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Django-allauth
    path("accounts/", include("allauth.urls")),
    # path('accounts/profile/',
    #      RedirectView.as_view(url='http://localhost:5173/profile/', permanent=False)),
    # path('api/auth/google/', GoogleAuthInitView.as_view(), name='google_auth_init'),
    # path('api/auth/google/callback/', GoogleLoginToJWTView.as_view(),
    #      name='google_auth_callback'),
    # simplejwt
    path("api/login/", MyTokenObtainPairView.as_view(), name="token_obtain"),
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", LogoutAPIView.as_view(), name="logout"),
    # Djoser
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),

    # Apps
    # users_accounts
    path("api/", include("users_accounts.urls")),
    path("api/notifications/", include("notification.urls")),
    # Ma
    path('api/vendors/', include('vendor.urls')),
    path('api/products/', include('product.urls')),
    # Admin
    path('admin/', admin.site.urls),
    # 0️⃣1️⃣ Document
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
