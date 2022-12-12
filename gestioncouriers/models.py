from django.db import models
from userprofile.models import User


# Create your models here.
class Message(models.Model):
    objet = models.CharField(max_length=200, default=None)
    messages = models.TextField()
    emetteur = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='emetteur_set'
                    )
    recepteur = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='recepteur_set'
                    )
    date_envoie = models.DateTimeField()
    status_envoie = models.BooleanField(default=False)
