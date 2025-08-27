# 📄 [users_accounts/admin.py] صفحة

# 🛠️ استيراد أدوات الإدارة
from django.contrib import admin

# 🌐 استيراد نموذج موقع الويب
from .models import User, FriendshipRequest

# admin.site.register(FriendshipRequest)


# 🖥️ تخصيص عرض النموذج في لوحة الإدارة
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 🌟 الحقول التي ستظهر في قائمة الإدارة
    list_display = (
        "name",
        "surname",
        "is_online",
        "email",
    )

    # 🔍 تمكين البحث عبر الحقول
    search_fields = ("name", "surname")

    # 🗂️ إضافة فلاتر حسب اللغة
    list_filter = ("is_online",)

    # 🔃 ترتيب النتائج حسب الاسم
    ordering = ("name",)

    # 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم
    # fields = ("name", "surname", "email", "is_online")


# 🖥️ تخصيص عرض النموذج في لوحة الإدارة
@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    # 🌟 الحقول التي ستظهر في قائمة الإدارة
    list_display = (
        "created_for",
        "created_by",
        "status",
    )

    # 🔍 تمكين البحث عبر الحقول
    search_fields = ("created_for", "created_by", "status")

    # 🗂️ إضافة فلاتر حسب اللغة
    list_filter = ("status",)

    # 🔃 ترتيب النتائج حسب الاسم
    ordering = ("status",)

    # 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم
    fields = ("created_at", "created_for", "created_by", "status")
