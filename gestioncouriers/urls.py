from django.urls import path
from . import views

app_name = 'mailmanagement'

urlpatterns = [
    # Ajouter 'projet_id' comme paramètre facultatif dans les URL
    path('<int:projet_id>/message/', views.messagerie, name="messagerie"),
    path('entrant/<int:projet_id>/', views.courier_entrant, name="entrant"),
    path('boitereception/envoye/<int:projet_id>/', views.courier_envoye, name='courier_envoye'),
    path('projet/<int:projet_id>/', views.boitemessagerie, name="inbox_projet"),
    
    # Ajouter des URL sans 'projet_id' pour les cas où le projet n'est pas spécifié
    path('', views.boitemessagerie, name="inbox"),
    path('message/<int:message_id>/', views.detail_message, name='detail_message'),
    path('reply/<int:message_id>/', views.reply_to_message, name='reply_to_message'),
    path('message/', views.messagerie, name="messagerie_general"),
    path('entrant/', views.courier_entrant, name="entrant_general"),
    path('boitereception/envoye/', views.courier_envoye, name='courier_envoye_general'),
]
