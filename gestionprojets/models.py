from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone
from userprofile.models import User
from gestiondesstock.models import Materiels


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=50, default=None)
    adresse = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.name


class Projet(models.Model):
    STATUS = (
        (1, 'NON DÉBUTÉ'),
        (2, 'EN COURS'),
        (3, 'TERMINER'),
        (4, 'ARCHIVER'),
    )

    name = models.CharField(max_length=100, default=None)
    description = models.TextField(default=None)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    coordinateur = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='cordinateur_projet',
                    default=None
                    )
    chef_project = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='chef_project',
                    default=None
                    )
    conducteur_travaux = models.ForeignKey(
                            User,
                            on_delete=models.CASCADE,
                            related_name='conducteur_travaux',
                            default=None
                            )
    list_intervenant = models.ManyToManyField(
                            User,
                            related_name='intervenant'
                            )
    list_materiels = models.ManyToManyField(Materiels)
    client = models.ForeignKey(
                Client,
                on_delete=models.CASCADE,
                default=None
                )
    status = models.PositiveSmallIntegerField(
                choices=STATUS,
                default=1
                )
    budget = models.IntegerField(default=0)
    pieces_jointes = models.FileField(
                        verbose_name='image',
                        upload_to='media/upload/documents',
                        null=True
                        )


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from plannig.models import Event

        event = Event.objects.filter(pk_projet = self.pk).first()
        
        if event is None:
            event = Event(
                        title=self.name,
                        description=self.description,
                        start_time=self.start_date,
                        end_time=self.end_date,
                        pk_projet = self.pk
                        )
        else:
            event.title = self.name
            event.description = self.description
            event.start_time = self.start_date
            event.end_time = self.end_date

        event.save()


    def delete(self, *args, **kwargs):
        from plannig.models import Event
        Event.objects.filter(pk_projet = self.pk).first().delete()
        super(Projet, self).delete(*args, **kwargs)


class Task(models.Model):
    STATUS = (
        (1, 'NON DÉBUTÉ'),
        (2, 'EN COURS'),
        (3, 'Terminer'),
    )
    name = models.CharField(max_length=100, default=None)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    list_materiels = models.ManyToManyField(Materiels)
    budget = models.IntegerField(default=0)
    attribuer_a = models.ManyToManyField(
                            User,
                            related_name='attribuer_a'
                            )                
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=None)
    pieces_jointes = models.FileField(
                        verbose_name='image',
                        upload_to='media/upload/documents',
                        null=True,
                        blank=True, 
                        default=None
                        )

    def __str__(self):
        """
        Retourne une représentation textuelle de la tâche.
        """
        return self.name

    def clean(self):
        """
        Vérifie que la date de fin n'est pas antérieure à la date de début.
        """
        if self.end_date < self.start_date:
            raise ValidationError("La date de fin ne peut pas être antérieure à la date de début.")

    def duration(self):
        """
        Retourne la durée de la tâche en jours.
        """
        return (self.end_date - self.start_date).days
    
    def remaining_time(self):
        """
        Retourne le temps restant pour la tâche en jours.
        """
        return (self.end_date - date.today()).days