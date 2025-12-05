from django.db import models
import uuid
from django.utils.timesince import timesince

from io import BytesIO
from PIL import Image
from django.core.files import File

from django.utils.text import slugify


# App User & Vendor
from vendor.models import Vendor
from users_accounts.models import User


class Category(models.Model):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="categories", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ordering = models.IntegerField(default=0)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='categories/', blank=True, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name

    def created_at_formatted(self):
        return timesince(self.created_at)

    # Auto Save Slug

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Product(models.Model):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        Vendor, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    # Auto Save Slug
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
