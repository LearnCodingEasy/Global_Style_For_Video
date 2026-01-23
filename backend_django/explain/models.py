"""
models.py
==========
الملف ده هو عقل الداتابيز كله
لازم يعدي من هنا الأول
"""

from django.db import models
from django.conf import settings
import uuid
from django.utils.text import slugify
# App User
from users_accounts.models import User


# ==================================================
# 1️⃣ Explain
# ==================================================


class ExplainCategory(models.Model):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________

    # Text
    name = models.CharField(max_length=100)


class Explain(models.Model):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    # ====================== 🆔 IDs ======================
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        max_length=255, editable=False, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="explains_created")
    profile = models.OneToOneField( User, on_delete=models.CASCADE,related_name="explain_profile")

    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________

    # ====================== ℹ️ Basic Info ======================
    # Text
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    url = models.URLField(max_length=255, blank=True, null=True, default="",)

    # Number
    price = models.IntegerField(default=0)
    count = models.PositiveIntegerField(default=0)
    views = models.BigIntegerField(default=0)
    rating = models.FloatField(default=0)
    actual_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Boolean
    is_active = models.BooleanField(default=True)

    # Date Time
    birth_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()

    # File
    files = models.FileField(upload_to="files/")
    image = models.ImageField(upload_to="images/")

    # Json
    settings = models.JSONField(default=dict, blank=True)

    # 🔗 Foreign Key
    category = models.ForeignKey(
        ExplainCategory,
        on_delete=models.CASCADE,
        related_name="explains"
    )

    # Slug Auto Save

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Explain.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
