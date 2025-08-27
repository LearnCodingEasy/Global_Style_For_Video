# users_accounts/views.py
import requests
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount
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

            return Response({"message": "You have successfully logged out."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginToJWTView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        refresh = RefreshToken.for_user(user)

        user.is_online = True
        user.save(update_fields=['is_online'])

        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

        frontend_url = f"http://localhost:5173/profile/{user.id}"
        redirect_url = f"{frontend_url}?access={tokens['access']}&refresh={tokens['refresh']}"

        return redirect(redirect_url)


class GoogleAuthInitView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return redirect('/accounts/google/login/')

    def post(self, request):

        code = request.data.get('code')
        if not code:
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)


class GoogleTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
