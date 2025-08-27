# 📝 [users_accounts/serializers.py] صفحة
from rest_framework import serializers


from .models import User, FriendshipRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "surname",
            "email",
            "date_of_birth",
            "gender",
            "get_avatar",
            "get_cover",
            "friends_count",
            "task_count",
            "date_joined",
            "date_joined_formatted",
            "last_login",
            "last_login_formatted",
            "is_online",
            "skills",
        )


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = (
            "id",
            "created_by",
            "status",
        )
