from django.urls import path

from . import api


urlpatterns = [
    path("", api.notifications, name="notifications"),
    path("read/<uuid:pk>/", api.read_notification, name="read_notification"),
    path(
        "mark_all_notifications_as_read/",
        api.mark_all_notifications_as_read,
        name="mark_all_notifications_as_read",
    ),
]
