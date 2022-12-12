from django.urls import path
from . import views

urlpatterns = [
    path('message', views.messagerie, name="messagerie"),
    path('', views.boitemessagerie, name="boitereception"),
    path('entrant', views.courier_entrant, name="entrant")
]
