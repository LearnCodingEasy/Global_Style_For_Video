
# 📝 [users_accounts/signals.py] صفحة

from allauth.socialaccount.signals import social_account_added, social_account_updated, pre_social_login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import User


@receiver(social_account_added)
def save_google_user_info(sender, request, sociallogin, **kwargs):

    user = sociallogin.user
    if sociallogin.account.provider == 'google':
        extra_data = sociallogin.account.extra_data

        user.name = extra_data.get('given_name', '')
        user.surname = extra_data.get('family_name', '')
        user.email = extra_data.get('email', '')
        user.avatar = extra_data.get('picture', '')

        user.save(update_fields=['name', 'surname', 'email', 'avatar'])
        print(f"✅ User data has been saved signals.py.: {user.email}")


@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    user.is_online = True
    user.save(update_fields=['is_online'])


@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    user.is_online = False
    user.save(update_fields=['is_online'])
