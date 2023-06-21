from django.urls import path
from . import views

app_name = 'mailmanagement' 

urlpatterns = [
    path('message', views.messagerie, name="messagerie"),
    path('', views.boitemessagerie, name="inbox"),
    path('entrant', views.courier_entrant, name="entrant"),
    path('boitereception/envoye', views.courier_envoye, name='courier_envoye'),
    path('message/<int:message_id>/', views.detail_message, name='detail_message'),
    path('reply/<int:message_id>/', views.reply_to_message, name='reply_to_message'),
]
