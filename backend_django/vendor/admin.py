from django.contrib import admin

from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    list_display = (
        "name", 'created_at', 'created_at_formatted', 'created_by'
    )

    search_fields = ("name", )

    ordering = ("name",)

    fields = ('created_by', "name", )
