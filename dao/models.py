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
