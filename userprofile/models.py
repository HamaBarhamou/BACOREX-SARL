from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "Assistant DAO"),
        (2, "Chef Service Etude"),
        (3, "Chef Departement Etude"),
        (4, "Directeur Energie"),
        (5, "admin"),
        (6, "Coordinateur des Operations"),
        (7, "Conducteurs des Travaux"),
        (8, "Chef de Projet"),
        (9, "DEGP"),
        (10, "Magasinier"),
        (11, "Intervenant"),
        (12, "PDG"),
        (13, "DAF"),
    )

    fonction = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)
    avatar = models.ImageField(
        verbose_name="photo de profile", upload_to="media/avatars"
    )

    def get_fonction_label(self):
        if self.fonction is not None:
            return self.get_fonction_display()
        return "Non défini"

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

    def is_Directeur_energie(self):
        return self.fonction == 4

    def is_conducteur_travaux(self):
        return self.fonction == 7

    def is_Intervenant(self):
        return self.fonction == 11

    def is_chefDeProjet_or_coordinateur_or_admin(self):
        if self.is_superuser:
            return True
        return self.fonction in [5, 6, 8]

    def is_leader(self):
        return self.is_admin_or_coordinator() or self.is_Directeur_energie()

    def is_member_workflot_achats(self):
        return self.is_superuser or self.fonction in [4, 6, 8, 12, 13]

    def is_coordinateur_or_directeur_energie(self):
        return self.fonction in [4, 6]

    def is_daf(self):
        return self.fonction == 13

    def is_pdg(self):
        return self.fonction == 12
