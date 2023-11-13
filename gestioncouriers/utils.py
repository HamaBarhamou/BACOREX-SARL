from django.core.mail import send_mail
from django.conf import settings
from django.db.models import QuerySet


def send_notification_email(receivers, objet, message_content=None):
    subject = 'Vous avez reçu un nouveau message'
    
    # Si le paramètre "receivers" est une liste ou un QuerySet
    if isinstance(receivers, (list, QuerySet)):
        for user in receivers:
            message = f'Vous avez reçu un nouveau message avec l\'objet: {objet} \n\n{message_content}\n\n Veuillez vous connecter https://gestion-des-projets-de-bacorex-sarl.onrender.com/ pour consulter'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    
    # Si le paramètre "receivers" est un seul utilisateur
    else:
        user = receivers
        message = f'Vous avez reçu un nouveau message avec l\'objet: {objet} Veuillez vous connecter https://gestion-des-projets-de-bacorex-sarl.onrender.com/ pour consulter'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
