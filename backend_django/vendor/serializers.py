# 📝 [vendor/serializers.py] صفحة


from rest_framework import serializers
from .models import Vendor
from users_accounts.serializers import UserSerializer
from users_accounts.models import User


class UserVendorSerializer(serializers.ModelSerializer):
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
            "is_vendor",
            "skills",
        )


class VendorSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source="created_by.username", read_only=True)
    # email = serializers.EmailField(source="created_by.email", read_only=True)
    # user = UserSerializer(read_only=True)
    # user = UserVendorSerializer(many=True)

    # user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Vendor
        read_only_fields = (
            "created_by",
            "created_at",
            "updated_at",
        )
        fields = (
            # "__all__",
            "id",
            # "user",
            # "user_id",
            "name",
            "created_at",
            "updated_at",
            "created_at_formatted",
        )

        # def create(self, validated_data):
        #     user_id = validated_data.pop("user_id")
        #     from users_accounts.models import User
        #     try:
        #         user = User.objects.get(pk=user_id)
        #         # user = User.objects.get(id=user_id)
        #         if user.is_vendor:
        #             user.is_vendor = True
        #             user.save()
        #         vendor = User.objects.create(user=user, **validated_data)
        #         return vendor

        #     except User.DoesNotExist:
        #         raise serializers.ValidationError("User.Does Not Exist:")


class VendorDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vendor
        read_only_fields = (
            "created_at",
            "updated_at",
        )
        fields = (
            "__all__",
        )
