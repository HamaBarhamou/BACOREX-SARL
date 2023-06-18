from django.db import models
from userprofile.models import User

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    objet = models.CharField(max_length=200)
    messages = models.TextField()
    emetteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emetteur_messages'
    )
    recepteurs = models.ManyToManyField(
        User,
        related_name='recepteur_messages'
    )
    date_envoie = models.DateTimeField(auto_now_add=True)
    status_envoie = models.BooleanField(default=False)
    lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    notification_email_envoyee = models.BooleanField(default=False)
    fil_de_discussion = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    documents = models.ManyToManyField(Document)

    def __str__(self):
        return self.objet
