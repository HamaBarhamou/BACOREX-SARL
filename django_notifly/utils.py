from .models import Notification, UserNotification


def send_notification(notification_type, message, url, recipients, extra_info=None, send_email=False, email_subject=None, email_template=None):
    notification = Notification.objects.create(
        notification_type=notification_type,
        message=message,
        url=url,
        extra_info=extra_info,
        send_email=send_email,
        email_subject=email_subject,
        email_template=email_template
    )
    for user in recipients:
        UserNotification.objects.create(user=user, notification=notification)

        # Ici, vous pouvez ajouter la logique d'envoi d'email si send_email=True

    return notification


def mark_notification_as_read(user_notification_id):
    user_notification = UserNotification.objects.get(id=user_notification_id)
    user_notification.mark_as_read()

