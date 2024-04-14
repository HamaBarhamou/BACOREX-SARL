from .models import Notification, UserNotification
from django.core.exceptions import ValidationError


NEW_PROJECT = 1
UPDATE_PROJECT = 2
NEW_TASK = 3
UPDATE_YASK = 4
PURCHASE_REQUEST = 5
OTHER = 6


def send_notification(
    notification_type,
    message,
    url,
    recipients,
    extra_info=None,
    send_email=False,
    email_subject=None,
    email_template=None,
):
    # Valider le type de notification
    """if notification_type not in dict(Notification.NOTIFICATION_TYPES):
    raise ValidationError("Type de notification invalide.")"""

    try:
        notification = Notification.objects.create(
            notification_type=notification_type,
            message=message,
            url=url,
            extra_info=extra_info,
            send_email=send_email,
            email_subject=email_subject,
            email_template=email_template,
        )
        for user in recipients:
            UserNotification.objects.create(user=user, notification=notification)

            # Ajouter la logique d'envoi d'email ici si nécessaire

        return notification
    except Exception as e:
        # Loguer l'erreur ou faire un traitement spécifique
        print(f"Erreur lors de la création de la notification : {e}")
        # Vous pouvez décider de renvoyer None ou de relancer l'exception selon votre logique d'erreur.


def mark_notification_as_read(user_notification_id):
    user_notification = UserNotification.objects.get(id=user_notification_id)
    user_notification.mark_as_read()
