from django.contrib import admin

# Register your models here.

# 🛠️ استيراد أدوات الإدارة
from django.contrib import admin

# 🌐 استيراد نموذج موقع الويب
from .models import Notification


# 🖥️ تخصيص عرض النموذج في لوحة الإدارة
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    # 🌟 الحقول التي ستظهر في قائمة الإدارة
    list_display = (
        "body",
        "is_read",
        "type_of_notification",
        "created_by",
        "created_for",
    )

    # 🔍 تمكين البحث عبر الحقول
    search_fields = ("created_by", "created_for")

    # 🗂️ إضافة فلاتر حسب اللغة
    list_filter = ("is_read",)

    # 🔃 ترتيب النتائج حسب الاسم
    ordering = ("created_by",)

    # 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم
    # fields = ("name", "surname", "email", "is_online")
