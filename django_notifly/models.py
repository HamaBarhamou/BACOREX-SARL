from django.db import models
from userprofile.models import User
from django.utils import timezone


from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("1", "Nouveau Projet"),
        ("2", "Modification de Projet"),
        ("3", "Nouvelle Tâche"),
        ("4", "Mise à jour de Tâche"),
        ("5", "Demande d'achats"),
        ("6", "Autre"),
    )

    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    extra_info = models.JSONField(null=True, blank=True)

    # Champ ManyToMany avec le modèle intermédiaire 'UserNotification'
    recipients = models.ManyToManyField(
        User, through="UserNotification", related_name="notifications"
    )

    # Nouveaux champs pour l'envoi par e-mail
    send_email = models.BooleanField(default=False)
    email_subject = models.CharField(max_length=255, null=True, blank=True)
    email_template = models.TextField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        recipient_names = ", ".join(self.recipients.values_list("username", flat=True))
        return f"Notification pour {recipient_names} - {self.get_notification_type_display()}"


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.notification} - {'Lue' if self.is_read else 'Non lue'}"
