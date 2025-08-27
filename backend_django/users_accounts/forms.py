# 📄 [users_accounts/forms.py] ملف
#
# 🔄 هذا الملف يحتوي على نماذج Django Forms التي تُستخدم لإنشاء النماذج التي يتفاعل معها المستخدمون.
# 🌟 هذه النماذج تعمل كوسيط بين واجهة المستخدم وقاعدة البيانات.

# 🌟 1️⃣ استيراد النماذج الأساسية
# - يتم استيراد نموذج إنشاء المستخدم `UserCreationForm` من مكتبة `django.contrib.auth.forms`.
# - استيراد `forms` من مكتبة Django لإنشاء النماذج.
from django.contrib.auth.forms import UserCreationForm
from django import forms

# 🌟 2️⃣ استيراد نموذج البيانات
# - يتم استيراد نموذج `User` المعرَّف مسبقًا في ملف `models.py`.
from .models import User


# 📝 3️⃣ **SignupForm**
# - نموذج تسجيل المستخدمين الجدد.
# - يرث من `UserCreationForm` لتوفير الحقول اللازمة لإنشاء مستخدم جديد مع الحقول المخصصة.
class SignupForm(UserCreationForm):
    # 🔧 إعدادات النموذج: يتم تحديد النموذج المرتبط والحقول التي سيتم عرضها.
    class Meta:
        model = User  # 🌟 النموذج المرتبط هو `User`.
        fields = (
            # 🧑 الاسم الأول
            "name",
            # 🧑 اللقب
            "surname",
            # 📧 البريد الإلكتروني
            "email",
            # 📅 تاريخ الميلاد
            "date_of_birth",
            # ⚧ الجنس
            "gender",
            # 🔑 كلمة المرور
            "password1",
            # 🔑 تأكيد كلمة المرور
            "password2",
        )


# 🖋️ 4️⃣ **ProfileForm**
# - نموذج تعديل بيانات المستخدم الشخصية.
# - يرث من `forms.ModelForm` لتوفير واجهة سهلة لتعديل البيانات.
class ProfileForm(forms.ModelForm):
    # 🔧 إعدادات النموذج: يتم تحديد النموذج المرتبط والحقول التي يمكن تعديلها.
    class Meta:
        model = User  # 🌟 النموذج المرتبط هو `User`.
        fields = (
            # 🧑 الاسم الأول
            "name",
            # 🧑 اللقب
            "surname",
            # 📧 البريد الإلكتروني
            "email",
            # 📅 تاريخ الميلاد
            "date_of_birth",
            # ⚧ الجنس
            "gender",
            # 🖼️ صورة الملف الشخصي
            "avatar",
            # 🖼️ صورة الغلاف
            "cover",
            "skills",
            "is_online",
        )
