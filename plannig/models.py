from django.db import models
from gestionprojets.models import Projet


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    pk_projet = models.IntegerField(default=None)

    def __str__(self):
        return self.title
