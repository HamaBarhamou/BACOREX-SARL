from django.db import models
from userprofile.models import User
from django.utils import timezone


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("1", "Nouveau Projet"),
        ("2", "Modification de Projet"),
        ("3", "Nouvelle Tâche"),
        ("4", "Mise à jour de Tâche"),
        ("5", "Autre"),
    )

    # Utilisation de ManyToManyField pour les destinataires multiples
    recipients = models.ManyToManyField(User, related_name="notifications")

    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    extra_info = models.JSONField(null=True, blank=True)

    # Nouveaux champs pour l'envoi par e-mail
    send_email = models.BooleanField(default=False)
    email_subject = models.CharField(max_length=255, null=True, blank=True)
    email_template = models.TextField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification pour {', '.join(user.username for user in self.recipients.all())} - {self.get_notification_type_display()}"
