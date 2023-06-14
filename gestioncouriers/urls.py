from django.urls import path
from . import views

app_name = 'mailmanagement' 

urlpatterns = [
    path('message', views.messagerie, name="messagerie"),
    path('', views.boitemessagerie, name="inbox"),
    path('entrant', views.courier_entrant, name="entrant")
]
