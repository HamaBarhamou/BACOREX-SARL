from django.db import models

# Create your models here.
class CategoriMateriel(models.Model):
    name = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=150, default=None)

class Entrepot(models.Model):
    name = models.CharField(max_length=100, default=None)
    adresse = models.CharField(max_length=100, default=None)

class Materiels(models.Model):
    name = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=150, default=None)
    qte = models.IntegerField()
    categorie = models.ForeignKey(CategoriMateriel, on_delete=models.CASCADE)
    entrepot = models.ForeignKey(Entrepot, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='image materiel', upload_to='media', default=None)