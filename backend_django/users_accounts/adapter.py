# 📝 [users_accounts/adapter.py] صفحة

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.shortcuts import redirect
from users_accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urlencode


class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):

        email_address = user_email(sociallogin.user)
        if not email_address:
            return

        try:
            user = User.objects.get(email=email_address)
            sociallogin.connect(request, user)
            print(
                f"✅ Google account linked to an existing account: {email_address}")

        except User.DoesNotExist:
            pass

    def save_user(self, request, sociallogin, form=None):

        user = super().save_user(request, sociallogin, form)
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            user.name = extra_data.get('given_name', '')
            user.surname = extra_data.get('family_name', '')
            user.email = extra_data.get('email', '')
            user.avatar = extra_data.get('picture', '')
            user.save()
            print(f"✅ User data has been saved adapter.py.: {user.email}")

        return user

    def get_login_redirect_url(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        user.is_online = True
        user.save(update_fields=['is_online'])

        params = urlencode({
            "access": access_token,
            "refresh": refresh_token,
            "user_id": str(user.id),
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "avatar": user.avatar or ""
        })
        return f"http://localhost:5173/auth-callback?{params}"
