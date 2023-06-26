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
      (9, 'DEGP'),
      (10, 'Magasinier'),
      (11, 'Intervenant'),
      )

    fonction = models.PositiveSmallIntegerField(
                  choices=USER_TYPE_CHOICES,
                  null=True
                  )
    avatar = models.ImageField(
                verbose_name='photo de profile',
                upload_to='media/avatars'
                )

    def __str__(self):
        fonction = "Admin"
        for loop in self.USER_TYPE_CHOICES:
            if loop[0] == self.fonction:
                fonction = loop[1]
                break
        return "{} : {}".format(self.username, fonction)

    def is_admin_or_coordinator(self):
        if self.is_superuser:
          return True
        return self.fonction in [5, 6]
      
    def is_chefDeProjet(self):
      return self.fonction == 8
    
    def is_chefDeProjet_or_coordinateur_or_admin(self):
      if self.is_superuser:
          return True
      return self.fonction in [5,6,8]