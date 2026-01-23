# backend_django\automation\serializers.py
from rest_framework import serializers
from .models import Explain
from .models import ExplainCategory

# ==================================================
# 1️⃣ Explain
# ==================================================


class ExplainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExplainCategory
        fields = "__all__"


class ExplainSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = Explain
        read_only_fields = ("created_by",)

        # fields = "__all__"
        fields = [
            # ___________________
            # حقل يتم تعبئة تلقائي
            # ___________________
            'id',
            'slug',
            'created_at',
            'updated_at',
            'created_by',
            'profile',

            # ___________________
            # حقل يتم تعبئة من المستخدام
            # ___________________
            # Text
            'name',
            'slug',
            'description',
            'email',
            'url',
            # Number
            'price',
            "count",
            "views",
            "rating",
            "actual_price",
            # Boolean
            "is_active",
            # Date Time
            'birth_date',
            'start_time',
            'created_at',
            'updated_at',
            # File
            'files',
            'image',
            # Json
            'settings',
            # ForeignKey
            'category',
            "category_name",
        ]
