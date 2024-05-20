from django.db import models


# Create your models here.
class DAO(models.Model):
    dao_number = models.CharField(max_length=200)
    dao_title = models.CharField(max_length=200)
    date_publication = models.DateTimeField()
    date_soumission = models.DateTimeField()
    approbation_chef_service = models.BooleanField(default=False)
    approbation_chef_depatement = models.BooleanField(default=False)
    approbation_direction = models.BooleanField(default=False)
    document_link = models.URLField(blank=True)

    def __str__(self):
        return "{} {}".format(self.dao_number, self.dao_title)


class ExperienceSimilaire(models.Model):
    dao = models.ForeignKey(
        DAO, related_name="experiences_similaires", on_delete=models.CASCADE
    )
    reference_marche = models.CharField(max_length=200)
    objet = models.CharField(max_length=600)
    description_travaux = models.TextField()
    delai_execution_jours = models.PositiveIntegerField()
    delai_execution_mois = models.PositiveIntegerField()
    nom_client = models.CharField(max_length=200)
    financement = models.CharField(max_length=200)
    maitre_ouvrage = models.CharField(max_length=200)
    montant_contrat = models.DecimalField(max_digits=10, decimal_places=2)
    date_demarrage_travaux = models.DateTimeField()
    date_fin_travaux = models.DateTimeField()
    document = models.FileField(upload_to="documents/")

    def __str__(self):
        return self.reference_marche
