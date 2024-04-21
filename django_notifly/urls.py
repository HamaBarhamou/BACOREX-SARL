# django_Notifly/urls.py
from django.urls import path
from .views import unread_count, all_notifications_view, read_notification

app_name = "notifly"

urlpatterns = [
    path("unread-count/", unread_count, name="unread_count"),
    path("all-notifications/", all_notifications_view, name="all_notifications"),
    path(
        "read_notification/<int:user_notification_id>/",
        read_notification,
        name="read_notification",
    ),
]
