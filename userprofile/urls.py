from django.urls import path
from . import views

app_name = "userprofile"

urlpatterns = [
    path("", views.login_page, name="login"),
    path("logout", views.deconnexion, name="logout"),
]
