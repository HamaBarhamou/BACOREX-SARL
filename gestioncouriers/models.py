from django.db import models
from userprofile.models import User
from gestionprojets.models import Projet

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    objet = models.CharField(max_length=200, blank=False)
    messages = models.TextField()
    emetteur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # on_delete is now SET_NULL
        null=True,  # You need to set null=True if you use SET_NULL
        related_name='emetteur_messages'
    )
    recepteurs = models.ManyToManyField(
        User,
        related_name='recepteur_messages'
    )
    date_envoie = models.DateTimeField(auto_now_add=True)
    status_envoie = models.BooleanField(default=True)  # default is now True
    lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    notification_email_envoyee = models.BooleanField(default=False)
    fil_de_discussion = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    documents = models.ManyToManyField(Document)

    created_at = models.DateTimeField(auto_now_add=True)  # New field
    updated_at = models.DateTimeField(auto_now=True)  # New field

    # Ajoutez une relation au projet
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.objet


class MessagePredefini(models.Model):
    
    titre = models.CharField(max_length=200)
    corps = models.TextField()
    expeditaire_role = models.PositiveSmallIntegerField(
        choices=User.USER_TYPE_CHOICES,
        null=True
    )
    destinataire_role = models.PositiveSmallIntegerField(
        choices=User.USER_TYPE_CHOICES,
        null=True
    )
    def __str__(self):
        return self.titre

