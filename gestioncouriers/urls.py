from django.urls import path
from . import views

app_name = 'mailmanagement' 

urlpatterns = [
    path('message', views.messagerie, name="messagerie"),
    path('', views.boitemessagerie, name="inbox"),
    path('entrant', views.courier_entrant, name="entrant"),
    path('boitereception/envoye', views.courier_envoye, name='courier_envoye'),
]
