import logging
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

# Configuration du logger
logger = logging.getLogger(__name__)


class Configuration(models.Model):
    tva_pourcentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("19.00"),
        help_text="Taux de TVA en pourcentage (ex: 19.00 pour 19%)",
    )

    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configurations"

    def __str__(self):
        return f"Configuration (TVA: {self.tva_pourcentage}%)"

    def clean(self):
        """Valide que la TVA n'est pas négative."""
        if self.tva_pourcentage < Decimal("0.00"):
            raise ValidationError(
                {"tva_pourcentage": "La TVA ne peut pas être négative."}
            )
        super().clean()

    @classmethod
    def get_tva(cls):
        """Retourne le taux de TVA actuel"""
        config = cls.objects.first()
        if not config:
            config = cls.objects.create()
        return config.tva_pourcentage


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
    taux_dollar_fcfa = models.DecimalField(max_digits=10, decimal_places=2, default=630)
    taux_euro_fcfa = models.DecimalField(max_digits=10, decimal_places=2, default=656)

    def __str__(self):
        return "Rapport de dépouillement pour DAO {}".format(self.dao.dao_number)

    def convertir_en_fcfa(self, montant, devise):
        """Convertit un montant en FCFA en fonction de la devise (sans TVA)"""
        if devise == "USD":
            return montant * self.taux_dollar_fcfa
        elif devise == "EUR":
            return montant * self.taux_euro_fcfa
        else:
            return montant


class Soumissionnaire(models.Model):
    nom = models.CharField(max_length=200)  # Nom du soumissionnaire
    adresse = models.CharField(max_length=200, blank=True, null=True)  # Adresse
    telephone = models.CharField(max_length=20, blank=True, null=True)  # Téléphone
    email = models.EmailField(blank=True, null=True)  # Email
    # Ajoutez d'autres champs si nécessaire

    def __str__(self):
        return self.nom


# Modèle LigneRapport
class LigneRapport(models.Model):
    rapport = models.ForeignKey(
        RapportDepouillement,
        related_name="lignes",
        on_delete=models.CASCADE,
    )
    soumissionnaire = models.ForeignKey(
        Soumissionnaire,
        related_name="lignes_rapport",
        on_delete=models.CASCADE,
    )
    observations = models.TextField(blank=True, null=True)  # Observations générales

    def __str__(self):
        return (
            f"Ligne pour {self.soumissionnaire.nom}"
            if self.soumissionnaire
            else "Nouvelle ligne"
        )


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
    offre_financiere = models.DecimalField(max_digits=10, decimal_places=2)
    devise = models.CharField(
        max_length=10,
        choices=[("FCFA", "FCFA"), ("USD", "USD"), ("EUR", "EUR")],
        default="FCFA",
    )
    est_htva = models.BooleanField(
        default=True,
        verbose_name="HTVA",
        help_text="Cochez si le montant est Hors TVA (HTVA)",
    )
    offre_financiere_fcfa = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    offre_financiere_fcfa_ttc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant TTC (FCFA)",
    )

    def __str__(self):
        return "Offre pour {} par {}".format(
            self.lot.nom_lot,
            (
                self.ligne_rapport.soumissionnaire.nom
                if self.ligne_rapport.soumissionnaire
                else "Inconnu"
            ),
        )

    def get_offre_fcfa(self):
        """Retourne l'offre financière en FCFA TTC"""
        rapport = self.ligne_rapport.rapport
        montant_fcfa = rapport.convertir_en_fcfa(self.offre_financiere, self.devise)

        # Si c'est déjà TTC, on retourne simplement
        if not self.est_htva:
            return montant_fcfa

        # Sinon on ajoute la TVA
        tva = Configuration.get_tva() / Decimal("100")
        return montant_fcfa * (Decimal("1") + tva)

    def save(self, *args, **kwargs):
        try:
            rapport = self.ligne_rapport.rapport
            # Conversion en FCFA (sans TVA)
            self.offre_financiere_fcfa = rapport.convertir_en_fcfa(
                self.offre_financiere, self.devise
            )
            # Calcul du montant TTC
            # print('Configuration.get_tva()=',Configuration.get_tva())
            tva = Configuration.get_tva() / Decimal("100")
            if self.est_htva:
                self.offre_financiere_fcfa_ttc = self.offre_financiere_fcfa * (
                    Decimal("1") + tva
                )
            else:
                self.offre_financiere_fcfa_ttc = self.offre_financiere_fcfa
            # Logging
            logger.info(
                f"Conversion: {self.offre_financiere} {self.devise} -> "
                f"{self.offre_financiere_fcfa} FCFA "
                f"({'HTVA' if self.est_htva else 'TTC'}) -> "
                f"{self.offre_financiere_fcfa_ttc} FCFA TTC"
            )
        except Exception as e:
            logger.error(f"Erreur de conversion: {e}")
            raise ValidationError(f"Impossible de convertir l'offre: {e}")

        super().save(*args, **kwargs)

    @classmethod
    def mettre_a_jour_offres_fcfa(cls, rapport):
        """
        Méthode de classe pour mettre à jour toutes les offres en FCFA
        pour un rapport donné
        """
        # Récupérez toutes les offres
        offres_lots = cls.objects.filter(ligne_rapport__rapport=rapport)
        print(f"Offres à mettre à jour: {offres_lots.count()}")

        for offre in offres_lots:
            try:
                # Conversion en FCFA
                offre.offre_financiere_fcfa = rapport.convertir_en_fcfa(
                    offre.offre_financiere, offre.devise
                )

                # Calcul du montant TTC
                tva = Configuration.get_tva() / Decimal("100")
                if offre.est_htva:
                    offre.offre_financiere_fcfa_ttc = offre.offre_financiere_fcfa * (
                        Decimal("1") + tva
                    )
                else:
                    offre.offre_financiere_fcfa_ttc = offre.offre_financiere_fcfa

                offre.save(
                    update_fields=["offre_financiere_fcfa", "offre_financiere_fcfa_ttc"]
                )
                print(
                    f"Offre mise à jour: {offre.id}, {offre.offre_financiere} "
                    f"{offre.devise} -> {offre.offre_financiere_fcfa} FCFA "
                    f"({'HTVA' if offre.est_htva else 'TTC'}) -> "
                    f"{offre.offre_financiere_fcfa_ttc} FCFA TTC"
                )
            except Exception as e:
                print(f"Erreur lors de la mise à jour de l'offre {offre.id}: {e}")


# Modèle pour l'attribution des lots
class AttributionLot(models.Model):
    STATUT_CHOICES = [
        ("ATTRIBUE", "Attribué"),
        ("REJETE", "Rejeté"),
        ("EN_ATTENTE", "En attente de décision"),
    ]

    lot = models.ForeignKey(
        Lot,
        related_name="attributions",
        on_delete=models.CASCADE,
    )
    soumissionnaire = models.ForeignKey(
        Soumissionnaire,
        related_name="attributions",
        on_delete=models.CASCADE,
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="EN_ATTENTE"
    )
    motif_rejet = models.TextField(
        blank=True,
        null=True,
        help_text="Motif de rejet si le soumissionnaire n'est pas retenu",
    )
    document_attribution = models.FileField(
        upload_to="attributions/%Y/%m/%d/",
        blank=True,
        null=True,
        help_text="Document scanné de la lettre d'attribution",
    )
    date_attribution = models.DateField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("lot", "soumissionnaire")
        verbose_name = "Attribution de lot"
        verbose_name_plural = "Attributions de lots"

    def __str__(self):
        return (
            f"Attribution {self.lot} -"
            f" {self.soumissionnaire.nom} ({self.get_statut_display()})"
        )

    def clean(self):
        # Vérification que le soumissionnaire a bien fait une offre pour ce lot
        if not OffreLot.objects.filter(
            lot=self.lot, ligne_rapport__soumissionnaire=self.soumissionnaire
        ).exists():
            raise ValidationError(
                f"Le soumissionnaire {self.soumissionnaire.nom} n'a pas fait d'offre"
                " pour ce lot"
            )

        # Si statut est ATTRIBUE, document d'attribution obligatoire
        if self.statut == "ATTRIBUE" and not self.document_attribution:
            raise ValidationError(
                "Un document d'attribution est requis pour l'attribution du marché"
            )

    def save(self, *args, **kwargs):
        self.lot.dao.is_closed = True
        self.lot.dao.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        dao = self.lot.dao
        super().delete(*args, **kwargs)  # Suppression de l'attribution
        # Vérifier s'il reste des attributions pour ce DAO
        if not AttributionLot.objects.filter(lot__dao=dao).exists():
            dao.is_closed = False
            dao.save()


class ExperienceSimilaire(models.Model):
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
