from django.urls import path
from . import views

app_name = "history"

urlpatterns = [
    path("history/", views.history_list, name="history_list"),
]
