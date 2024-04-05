from django.urls import path
from . import views

app_name = "djnagonotifly"

urlpatterns = [
    path("", views.all_notifications, name="all_notifications"),
]
