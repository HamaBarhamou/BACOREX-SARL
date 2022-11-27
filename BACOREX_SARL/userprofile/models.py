from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'Assistant DAO'),
      (2, 'Chef Service Etude'),
      (3, 'Chef Departement Etude'),
      (4, 'Directeur Generale'),
      (5, 'admin'),
      (6, 'Coordinateur des Operations'),
      (7, 'Conducteurs des Travaux'),
      (8, 'Chef de Projet'),
      (9, 'DEGP')
    )

    fonction = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    avatar = models.ImageField(verbose_name='photo de profile')

    """ ASSISTANT_DAO = 'ASSISTANT_DAO'
    CHEF_SERVICE_ETUDE = 'CHEF_SERVICE_ETUDE'
    CHEF_DEPARTEMENT_ETUDE = 'CHEF_DEPARTEMENT_ETUDE'
    DG = 'DG'

    ROLE_CHOICES = (
        (ASSISTANT_DAO, 'Assistant_dao'),
        (CHEF_SERVICE_ETUDE, 'Chef_service_etude'),
        (CHEF_DEPARTEMENT_ETUDE, 'Chef_departement_etude'),
        (DG, 'Dg')
    )

    avatar = models.ImageField(verbose_name='photo de profile')
    fonction = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name = 'Fonction') """