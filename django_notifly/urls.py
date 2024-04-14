# django_Notifly/urls.py
from django.urls import path
from .views import unread_count, all_notifications_view

app_name = "notifly"

urlpatterns = [
    path("unread-count/", unread_count, name="unread_count"),
    path("all-notifications/", all_notifications_view, name="all_notifications"),
]
