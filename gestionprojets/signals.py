from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Phase
from gestioncouriers.utils import send_notification_email


@receiver(post_save, sender=Phase)
def create_notifications(sender, instance, created, **kwargs):
    # Vérifiez si la phase a été créée (et non simplement mise à jour)
    """if created:
    # L'objet du mail
    objet = 'Nouvelle Phase ajoutée'

    # Le contenu du mail
    message_content = 'La phase {} du projet {} débutera le {}'.format(instance.name, instance.project.name, instance.start_date)

    # Appel à la fonction send_notification_email avec les paramètres appropriés
    send_notification_email(instance.project.list_intervenant.all(), objet, message_content)
    """
    pass
