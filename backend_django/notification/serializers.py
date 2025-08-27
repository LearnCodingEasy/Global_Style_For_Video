# 📄 [ notification/serializers.py ] ملف

from rest_framework import serializers

from users_accounts.serializers import UserSerializer

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    # تضمين تفاصيل المرسل (created_by_data)
    created_by_data = UserSerializer(source="created_by", read_only=True)
    # تضمين تفاصيل المستقبل (created_for_data)
    created_for_data = UserSerializer(source="created_for", read_only=True)

    class Meta:
        model = Notification
        fields = (
            "id",
            "body",
            "is_read",
            "type_of_notification",
            "created_at_formatted",
            # تفاصيل المرسل
            "created_by",
            "created_by_data",
            # تفاصيل المستقبل
            "created_for",
            "created_for_data",  # بيانات المنشئ التفصيلية
        )
