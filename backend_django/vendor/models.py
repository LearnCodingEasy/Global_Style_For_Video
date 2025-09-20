from django.db import models
from users_accounts.models import User
import uuid

from django.utils import timezone
from django.utils.timesince import timesince


class Vendor(models.Model):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user = models.OneToOneField(
    #     User, related_name='vendor_profile', on_delete=models.CASCADE)
    created_by = models.OneToOneField(
        User, related_name='vendor_profile', on_delete=models.CASCADE)
    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def created_at_formatted(self):
        return timesince(self.created_at)
