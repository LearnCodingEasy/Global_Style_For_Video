from django.contrib import admin

from .models import Category

# 🖥️ تخصيص عرض النموذج في لوحة الإدارة


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 🌟 الحقول التي ستظهر في قائمة الإدارة
    list_display = (
        "name",
        "created_by",
        "ordering",
        "is_active"
    )

    # 🔍 تمكين البحث عبر الحقول
    search_fields = ("name", )

    # 🗂️ إضافة فلاتر حسب اللغة
    list_filter = ("is_active",)

    # 🔃 ترتيب النتائج حسب الاسم
    ordering = ("name",)

    # 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم
    fields = (
        "created_by",
        "name",
        "description",
        "ordering",
        "is_active",
        "image")


# 🖥️ تخصيص عرض النموذج في لوحة الإدارة
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     # 🌟 الحقول التي ستظهر في قائمة الإدارة
#     list_display = (
#         "name",
#     )

#     # 🔍 تمكين البحث عبر الحقول
#     search_fields = ("name", )

#     # 🗂️ إضافة فلاتر حسب اللغة
#     list_filter = ("name",)

#     # 🔃 ترتيب النتائج حسب الاسم
#     ordering = ("name",)

#     # 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم
#     fields = (
#         "category",
#         "vendor",
#         "name",
#         "description",
#         "price",
#         "image"
#     )
