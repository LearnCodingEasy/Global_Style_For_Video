# 📄 ملف [ account/account_django/notification/api.py ]

from django.http import JsonResponse

from rest_framework.decorators import (
    api_view,  # 🧑‍💻 تعريف الدالة كـ API View
    authentication_classes,  # 🔐 تخصيص طبقات المصادقة
    permission_classes,  # 🔓 تخصيص صلاحيات الوصول
)


# 📜 استيراد نموذج الإشعار
from .models import Notification

# 📦 استيراد المُسلسل الخاص بالإشعار
from .serializers import NotificationSerializer


# 👤 استيراد نموذج المستخدم
from users_accounts.models import User

# 📦 استيراد مُسلسل المستخدم
from users_accounts.serializers import UserSerializer


# 📥 دالة لجلب الإشعارات الغير مقروءة
@api_view(["GET"])  # 🔄 نوع الطلب GET لجلب البيانات
def notifications(request):
    # print(f"✅ Notifications request.user  {request.user}")
    # استعراض جميع الإشعارات الغير مقروءة للمستخدم الحالي
    # 🔕 الفلترة لتحديد الإشعارات الغير مقروءة
    notifications = request.user.received_notifications.filter(is_read=False)
    # ✔️ طباعة الإشعارات التي تم فلترتها
    # print(f"✅ Notifications Filter  {notifications}")
    # 📦 تحويل الإشعارات إلى صيغة JSON باستخدام المُسلسل
    serializer = NotificationSerializer(notifications, many=True)
    # print(f"✅ Notifications serializer  {serializer}")
    # 📨 إرجاع الإشعارات في استجابة JSON
    return JsonResponse(serializer.data, safe=False)


# 📘 دالة لعلامة الإشعار كـ "مقروء"
# 🔄 نوع الطلب POST لتعديل البيانات
@api_view(["POST"])
def read_notification(request, pk):
    # 🔍 البحث عن الإشعار باستخدام ID
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    # ✅ تحديث حالة الإشعار إلى مقروء
    notification.is_read = True
    # 💾 حفظ التحديث في قاعدة البيانات
    notification.save()
    # 📩 إرجاع رسالة تأكيد أن الإشعار تم قراءته
    return JsonResponse({"message": "notification read"})


# 🧹 دالة لجعل جميع الإشعارات الغير مقروءة مقروءة
# 🔄 نوع الطلب POST لتعديل البيانات
@api_view(["POST"])
def mark_all_notifications_as_read(request):
    # 🔕 فلترة وتحديث جميع الإشعارات الغير مقروءة
    request.user.received_notifications.filter(is_read=False).update(is_read=True)
    # 📩 إرجاع رسالة تأكيد أن جميع الإشعارات تم جعلها مقروءة
    return JsonResponse({"message": "All notifications marked as read"})
