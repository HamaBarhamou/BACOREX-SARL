from django.db import models
from django.utils import timezone
from userprofile.models import User
from gestiondesstock.models import Materiels

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=50, default=None)
    adresse = models.CharField(max_length=100, default=None)
    start_date = models.DateField(default=timezone.now)

class Projet(models.Model):
    STATUS = (
      (1, 'NON DÉBUTÉ'),
      (2, 'EN COURS'),
      (3, 'Terminer'),
      (4, 'ARCHIVER'),
    )

    name = models.CharField(max_length=100, default=None)
    description = models.TextField(default=None)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    chef_project = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='chef_project', default=None)
    conducteur_travaux = models.ForeignKey(User, on_delete=models.CASCADE,
                                           related_name='conducteur_travaux', default=None)
    list_intervenant = models.ManyToManyField(User, related_name='intervenant')
    list_materiels = models.ManyToManyField(Materiels)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    status = models.PositiveSmallIntegerField(choices=STATUS, null=True)
    budget = models.IntegerField(default=0)
    pieces_jointes = models.FileField(default=None)

class Task(models.Model):
    STATUS = (
      (1, 'NON DÉBUTÉ'),
      (2, 'EN COURS'),
      (3, 'Terminer'),
      (4, 'ARCHIVER'),
    )
    name = models.CharField(max_length=100, default=None)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUS, null=True)
    list_intervenant = models.ManyToManyField(User, related_name='intervenant_task')
    list_materiels = models.ManyToManyField(Materiels)
    budget = models.IntegerField(default=0)
    pieces_jointes = models.FileField(default=None)
    attribuer_a = models.ForeignKey(User, on_delete=models.CASCADE,
                                           related_name='attribuer_a', default=None)
