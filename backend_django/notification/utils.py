# 📄 [ notification/utils.py ] ملف

from .models import Notification

from users_accounts.models import FriendshipRequest


def create_notification(
    type_of_notification,
    created_by,
    created_for,
    friendrequest_id=None,
    extra_data=None,
):
    try:
        # تحقق إذا كان friendrequest_id غير فارغ
        if friendrequest_id:
            friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
            created_for = friendrequest.created_for
            created_by = friendrequest.created_by

        # بناء النص بناءً على نوع الإشعار
        body = ""
        # 👥 طلب صداقة جديد
        if type_of_notification == Notification.NEWFRIENDREQUEST:
            body = f"{created_by.surname} sent you a friend request!"
        # ✅ قبول طلب صداقة
        elif type_of_notification == Notification.ACCEPTEDFRIENDREQUEST:
            body = f"{created_by.surname} accepted your friend request!"
        # 💬 تعليق على منشور
        elif type_of_notification == Notification.POSTCOMMENT:
            body = f"{created_by.surname} commented on your post!"
        # 👍 إعجاب بالمنشور
        elif type_of_notification == Notification.POSTLIKE:
            body = f"{created_by.surname} liked your post!"
        # 📩 رسالة جديدة
        elif type_of_notification == Notification.MESSAGE:
            body = f"{created_by.surname} sent you a message!"
        # إنشاء الإشعار
        notification = Notification.objects.create(
            body=body,
            type_of_notification=type_of_notification,
            created_by=created_by,
            created_for=created_for,
            # friendrequest_id=friendrequest_id
            # إضافة بيانات إضافية إذا كانت موجودة
            **(extra_data or {}),
        )
        return notification
    except Exception as e:
        # في حال حدوث أي خطأ، يتم رفع استثناء مع رسالة الخطأ
        raise ValueError(f"Error creating notification: {e}")
