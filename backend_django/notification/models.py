# 📄 [ notification/models.py ] ملف

import uuid

from django.db import models

from users_accounts.models import User


from django.utils.timesince import timesince


class Notification(models.Model):
    # أنواع الإشعارات
    # 🆕👫 طلب صداقة جديد
    NEWFRIENDREQUEST = "new_friendrequest"
    # ✅👫 تم قبول طلب الصداقة
    ACCEPTEDFRIENDREQUEST = "accepted_friendrequest"
    # ❌👫 تم رفض طلب الصداقة
    REJECTEDFRIENDREQUEST = "rejected_friendrequest"
    # 🆕👥 متابع جديد
    NEWFOLLOW = "new_follow"
    # ❌👥 إلغاء المتابعة
    CANCELFOLLOW = "cancel_follow"
    # 💬📝 تعليق على المنشور
    POSTCOMMENT = "post_comment"
    # 👍📷 إعجاب بالمنشور
    POSTLIKE = "post_like"
    # 💌✉️ رسالة جديدة
    MESSAGE = "message"

    # قائمة أنواع الإشعارات المُعرفة (اختيارات من قائمة الإشعارات)
    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, "New friendrequest"),
        (ACCEPTEDFRIENDREQUEST, "Accepted friendrequest"),
        (REJECTEDFRIENDREQUEST, "Rejected friendrequest"),
        (NEWFOLLOW, "New follow"),
        (CANCELFOLLOW, "Cancel follow"),
        (POSTCOMMENT, "Post comment"),
        (POSTLIKE, "Post like"),
        (MESSAGE, "Message"),
    )

    # id: مُفتاح أساسي يُستخدم كمُعرّف فريد للإشعار باستخدام uuid
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # body: حقل نصي يحتوي على محتوى الإشعار
    body = models.TextField()
    # is_read: حقل بياني يشير إذا كان الإشعار قد تم قراءته أم لا
    is_read = models.BooleanField(default=False)
    # type_of_notification: حقل نصي قصير يُحدد نوع الإشعار باستخدام القيم المعرفة سابقًا
    type_of_notification = models.CharField(
        max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION
    )
    # created_by: مفتاح خارجي يربط الإشعار بالمستخدم الذي أنشأه
    created_by = models.ForeignKey(
        User, related_name="created_notifications", on_delete=models.CASCADE
    )
    # created_for: مفتاح خارجي يربط الإشعار بالمستخدم الذي تم إرسال الإشعار إليه
    created_for = models.ForeignKey(
        User, related_name="received_notifications", on_delete=models.CASCADE
    )
    # created_at: حقل يحفظ تاريخ ووقت إنشاء الإشعار
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ترتيب الإشعارات حسب تاريخ الإنشاء من الأحدث إلى الأقدم
        ordering = ("-created_at",)

    def created_at_formatted(self):
        # إرجاع الوقت المنقضي منذ إنشاء الإشعار
        return timesince(self.created_at)
