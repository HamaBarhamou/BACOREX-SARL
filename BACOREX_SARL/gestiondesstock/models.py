from django.db import models

# Create your models here.
class CategoriMateriel(models.Model):
    name = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=150, default=None)

class Materiels(models.Model):
    name = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=150, default=None)
    categorie = models.ForeignKey(CategoriMateriel, on_delete=models.CASCADE)