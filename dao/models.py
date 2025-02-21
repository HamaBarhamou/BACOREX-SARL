from django.db import models
from django.core.exceptions import ValidationError


# Modèle DAO
class DAO(models.Model):
    dao_number = models.CharField(max_length=200, unique=True)  # Numéro unique du DAO
    dao_title = models.CharField(max_length=200)  # Titre du DAO
    date_publication = models.DateTimeField()  # Date de publication
    date_soumission = models.DateTimeField()  # Date de soumission
    fichier = models.FileField(
        upload_to="dao_documents/%Y/%m/%d/", blank=True, null=True
    )
    is_closed = models.BooleanField(default=False)  # Indique si le DAO est clôturé

    def __str__(self):
        return "{} {}".format(self.dao_number, self.dao_title)


# Modèle Lot
class Lot(models.Model):
    dao = models.ForeignKey(
        DAO,
        related_name="lots",
        on_delete=models.CASCADE,
    )
    nom_lot = models.CharField(
        max_length=200
    )  # Nom du lot (ex: "Lot 1", "Lot 2", etc.)
    description = models.TextField(
        blank=True, null=True
    )  # Description du lot (optionnel)

    def __str__(self):
        return "{} - {}".format(self.dao.dao_number, self.nom_lot)


# Modèle ReponseDAO
class ReponseDAO(models.Model):
    dao = models.ForeignKey(
        DAO,
        related_name="reponses",
        on_delete=models.CASCADE,
    )
    TYPE_REPONSE_CHOICES = [
        ("SCAN", "Document scanné"),
        ("ZIP", "Dossier/Fichier compressé"),
        ("URL", "Lien URL"),
    ]
    type_reponse = models.CharField(
        max_length=10, choices=TYPE_REPONSE_CHOICES
    )  # Type de réponse
    fichier = models.FileField(
        upload_to="reponses/dao_%Y/%m/%d/", blank=True, null=True
    )  # Fichier (scan ou ZIP)
    url = models.URLField(blank=True, null=True)  # URL (si la réponse est un lien)
    date_soumission = models.DateTimeField(auto_now_add=True)  # Date de soumission

    def __str__(self):
        return "Réponse pour DAO {} (Type: {})".format(
            self.dao.dao_number, self.type_reponse
        )

    def clean(self):
        if self.type_reponse in ["SCAN", "ZIP"] and not self.fichier:
            raise ValidationError("Un fichier est requis pour ce type de réponse.")
        if self.type_reponse == "URL" and not self.url:
            raise ValidationError("Une URL est requise pour ce type de réponse.")


# Modèle RapportDepouillement
class RapportDepouillement(models.Model):
    dao = models.OneToOneField(
        DAO,
        related_name="rapport_depouillement",
        on_delete=models.CASCADE,
    )
    date_creation = models.DateTimeField(
        auto_now_add=True
    )  # Date de création du rapport

    def __str__(self):
        return "Rapport de dépouillement pour DAO {}".format(self.dao.dao_number)


# Modèle LigneRapport
class LigneRapport(models.Model):
    rapport = models.ForeignKey(
        RapportDepouillement,
        related_name="lignes",
        on_delete=models.CASCADE,
    )
    nom_soumissionnaire = models.CharField(max_length=200)  # Nom du soumissionnaire
    observations = models.TextField(blank=True, null=True)  # Observations générales

    def __str__(self):
        return "Ligne pour {}".format(self.nom_soumissionnaire)


# Modèle OffreLot
class OffreLot(models.Model):
    ligne_rapport = models.ForeignKey(
        LigneRapport,
        related_name="offres_lots",
        on_delete=models.CASCADE,
    )
    lot = models.ForeignKey(
        Lot,
        related_name="offres",
        on_delete=models.CASCADE,
    )
    offre_financiere = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Offre financière pour ce lot

    def __str__(self):
        return "Offre pour {} par {}".format(
            self.lot.nom_lot, self.ligne_rapport.nom_soumissionnaire
        )


class ExperienceSimilaire(models.Model):
    dao = models.ForeignKey(
        DAO,
        related_name="experiences_similaires",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reference_marche = models.CharField(max_length=200)
    objet = models.CharField(max_length=600)
    description_travaux = models.TextField()
    delai_execution_jours = models.PositiveIntegerField()
    nom_client = models.CharField(max_length=200)
    financement = models.CharField(max_length=200)
    maitre_ouvrage = models.CharField(max_length=200)
    montant_contrat = models.DecimalField(max_digits=10, decimal_places=2)
    date_demarrage_travaux = models.DateTimeField()
    date_fin_travaux = models.DateTimeField()
    document = models.FileField(upload_to="documents/")

    def __str__(self):
        return self.reference_marche
