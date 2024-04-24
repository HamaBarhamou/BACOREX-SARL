from django.db import models
from django.contrib.auth.models import AbstractUser

ASSISTANT_DAO = 1
CHEF_SERVICE_ETUDE = 2
CHEF_DEPARTEMENT_ETUDE = 3
DIRECTEUR_ENERGIE = 4
ADMIN = 5
COORDINATEUR_OPERATIONS = 6
CONDUCTEUR_TRAVAUX = 7
CHEF_PROJET = 8
DEGP = 9
MAGASINIER = 10
INTERVENANT = 11
PRESIDENT_DIRECTEUR_GENERALE = 12
DIRECTEUR_ADMINISTRATIF_FINANCIER = 13
CAISSIER = 14


# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (ASSISTANT_DAO, "Assistant DAO"),
        (CHEF_SERVICE_ETUDE, "Chef Service Etude"),
        (CHEF_DEPARTEMENT_ETUDE, "Chef Departement Etude"),
        (DIRECTEUR_ENERGIE, "Directeur Energie"),
        (ADMIN, "admin"),
        (COORDINATEUR_OPERATIONS, "Coordinateur des Operations"),
        (CONDUCTEUR_TRAVAUX, "Conducteurs des Travaux"),
        (CHEF_PROJET, "Chef de Projet"),
        (DEGP, "DEGP"),
        (MAGASINIER, "Magasinier"),
        (INTERVENANT, "Intervenant"),
        (PRESIDENT_DIRECTEUR_GENERALE, "PDG"),
        (DIRECTEUR_ADMINISTRATIF_FINANCIER, "DAF"),
        (CAISSIER, "CAISSIER"),
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

    def has_role(self, roles):
        if self.is_superuser:
            return True
        return self.fonction in roles

    def is_admin_or_coordinator(self):
        if self.is_superuser:
            return True
        return self.has_role([ADMIN, COORDINATEUR_OPERATIONS])

    def is_chefDeProjet(self):
        return self.has_role([CHEF_PROJET])

    def is_Directeur_energie(self):
        return self.has_role([DIRECTEUR_ENERGIE])

    def is_conducteur_travaux(self):
        return self.has_role([CONDUCTEUR_TRAVAUX])

    def is_Intervenant(self):
        return self.has_role([INTERVENANT])

    def is_chefDeProjet_or_coordinateur_or_admin(self):
        if self.is_superuser:
            return True
        return self.has_role([CHEF_PROJET, COORDINATEUR_OPERATIONS, ADMIN])

    def is_leader(self):
        return self.has_role(
            [
                ADMIN,
                COORDINATEUR_OPERATIONS,
                DIRECTEUR_ENERGIE,
                DIRECTEUR_ADMINISTRATIF_FINANCIER,
                PRESIDENT_DIRECTEUR_GENERALE,
            ]
        )

    def is_member_workflot_achats(self):
        return self.is_superuser or self.has_role(
            [
                DIRECTEUR_ENERGIE,
                COORDINATEUR_OPERATIONS,
                CHEF_PROJET,
                DIRECTEUR_ADMINISTRATIF_FINANCIER,
                PRESIDENT_DIRECTEUR_GENERALE,
            ]
        )

    def is_coordinateur_or_directeur_energie(self):
        return self.has_role([COORDINATEUR_OPERATIONS, DIRECTEUR_ENERGIE])

    def is_daf(self):
        return self.has_role([DIRECTEUR_ADMINISTRATIF_FINANCIER])

    def is_pdg(self):
        return self.has_role([PRESIDENT_DIRECTEUR_GENERALE])

    def is_caissier(self):
        return self.has_role([CAISSIER])

    def is_directeur_energie_or_pdg_or_daf(self):
        return self.has_role(
            [
                DIRECTEUR_ENERGIE,
                PRESIDENT_DIRECTEUR_GENERALE,
                DIRECTEUR_ADMINISTRATIF_FINANCIER,
            ]
        )

    def administraion_role(self):
        return self.has_role([ADMIN])

    def gestiondao_role(self):
        return self.has_role(
            [ASSISTANT_DAO, CHEF_SERVICE_ETUDE, CHEF_DEPARTEMENT_ETUDE]
        )

    def gestiondesstock_role(self):
        return self.has_role([MAGASINIER])

    def gestionprojet_role(self):
        return self.has_role(
            [
                CHEF_PROJET,
                CONDUCTEUR_TRAVAUX,
                INTERVENANT,
                COORDINATEUR_OPERATIONS,
                DIRECTEUR_ENERGIE,
                PRESIDENT_DIRECTEUR_GENERALE,
                DIRECTEUR_ADMINISTRATIF_FINANCIER,
            ]
        )

    def newclients_role(self):
        return self.has_role([ADMIN, COORDINATEUR_OPERATIONS])

    def newprojet_role(self):
        return self.has_role([ADMIN, COORDINATEUR_OPERATIONS])

    def taskliste_redirection(self):
        return self.has_role(
            [CHEF_PROJET, CONDUCTEUR_TRAVAUX, INTERVENANT, COORDINATEUR_OPERATIONS]
        )

    def demande_achats_all(self):
        return self.has_role(
            [
                COORDINATEUR_OPERATIONS,
                DIRECTEUR_ADMINISTRATIF_FINANCIER,
                PRESIDENT_DIRECTEUR_GENERALE,
                DIRECTEUR_ENERGIE,
            ]
        )
