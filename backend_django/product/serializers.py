# 📝 [Product/serializers.py] صفحة

from rest_framework import serializers
from .models import Category
# from .models import Category, Product
# from vendor.serializers import VendorSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = (
            "created_by",
            "created_at",
            "updated_at",

        )
        fields = (
            "id",
            "name",
            "description",
            "slug",
            "get_slug",
            "ordering",
            "created_by",
            "created_at",
            "updated_at",
            "created_at_formatted",
            "image",
            # "thumbnail",
        )
