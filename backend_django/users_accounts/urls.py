# 📄 [ users_accounts/urls.py ] ملف

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import api


urlpatterns = [
    path("me/", api.me, name="me"),
    path("signup/", api.signup, name="signup"),
    # ___________________________
    # ___________________________
    # ___________________________
    # ** إدارة الملف الشخصي للمستخدم **
    path("profile/<uuid:id>/", api.profile, name="profile"),
    path("editprofile/", api.editprofile, name="editprofile"),
    path("editpassword/", api.editpassword, name="editpassword"),
    # ___________________________
    # ___________________________
    # ___________________________
    # ** إدارة الأصدقاء **
    path("friends/<uuid:pk>/", api.friends, name="friends"),
    path("friends/suggested/", api.my_friendship_suggestions,
         name="my_friendship_suggestions",),
    path("friends/<uuid:pk>/request/",
         api.send_friendship_request,
         name="send_friendship_request",),
    path(
        "friends/<uuid:pk>/<str:status>/", api.handle_request, name="handle_request"
    ),
]
