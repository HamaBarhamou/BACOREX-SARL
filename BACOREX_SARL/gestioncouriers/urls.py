from django.urls import path
from . import views

from . import views

urlpatterns = [
    path('message',views.messagerie, name="messagerie"),
    path('', views.boitemessagerie, name="boitereception")
]