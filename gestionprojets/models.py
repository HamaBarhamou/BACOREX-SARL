from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone
from userprofile.models import User
from gestiondesstock.models import Materiels
from django.db.models import Q



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
    
    def pourcentage_achevement(self):
        # Obtenir toutes les tâches pour ce projet
        taches = self.task_set.all()  # Assurez-vous que votre modèle de tâche est lié à votre projet avec un ForeignKey
        total_taches = taches.count()  # Compter le nombre total de tâches
        taches_terminees = taches.filter(status=3).count()  # Compter les tâches terminées

        # Calculer le pourcentage
        if total_taches > 0:
            pourcentage_achevement = (taches_terminees / total_taches) * 100
        else:
            pourcentage_achevement = 0  # Eviter la division par zéro si le projet n'a pas de tâches

        # Convertir en chaîne avec un point comme séparateur décimal
        pourcentage_achevement_str = "{:.2f}".format(pourcentage_achevement).replace(',', '.')
        
        return pourcentage_achevement_str
        return round(pourcentage_achevement, 2)  # Arrondir à deux décimales pour la précision
    
    
    @staticmethod
    def get_projects_by_user(user):
        # Les leaders peuvent voir tous les projets.
        if user.is_leader():
            return Projet.objects.all()

        # Les chefs de projet et les conducteurs de travaux peuvent voir les projets où ils sont responsables.
        projects = Projet.objects.filter(
            Q(chef_project=user) | 
            Q(conducteur_travaux=user) |
            Q(list_intervenant=user)
        )

        # Inclure les projets où l'utilisateur est affecté à une tâche.
        tasks = Task.objects.filter(attribuer_a=user)
        for task in tasks:
            projects |= Projet.objects.filter(pk=task.projet.pk)
        
        return projects.distinct()


    # Ajout de la méthode pour obtenir tous les utilisateurs impliqués dans un projet
    def get_all_users(self):
        # Commencez par ajouter les rôles principaux du projet.
        users = set([
            self.coordinateur,
            self.chef_project,
            self.conducteur_travaux
        ])

        # Ajouter tous les intervenants directement liés au projet.
        users.update(self.list_intervenant.all())

        # Ajouter tous les utilisateurs attribués à des tâches dans ce projet.
        tasks = self.task_set.all()
        for task in tasks:
            users.update(task.attribuer_a.all())
        
        # Retirer les éventuelles valeurs None (si des relations sont nulles).
        users.discard(None)

        return users

    
    def to_dict(self):
        # Convertissez l'instance Projet en dictionnaire, y compris des informations supplémentaires
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'coordinateur': self.coordinateur.get_full_name() if self.coordinateur else None,
            'chef_project': self.chef_project.get_full_name() if self.chef_project else None,
            'conducteur_travaux': self.conducteur_travaux.get_full_name() if self.conducteur_travaux else None,
            'status': self.get_status_display(),  # Affiche la représentation textuelle du statut
            'budget': self.budget,
            'pourcentage_achevement': self.pourcentage_achevement(),
        }

        # Ajoutez la logique des jours restants ici
        if date.today() < self.start_date:
            days_until_start = (self.start_date - date.today()).days
            data['days_remaining'] = f"Commence dans {days_until_start} jours"
        elif date.today() > self.end_date:
            data['days_remaining'] = "Terminé"
        else:
            days_remaining = (self.end_date - date.today()).days
            data['days_remaining'] = f"{days_remaining} jours restants"

        return data
    
    def days_remaining(self):
        if date.today() < self.start_date:
            return f"Commence dans {(self.start_date - date.today()).days} jours"
        elif date.today() > self.end_date:
            return "Terminé"
        else:
            return f"{(self.end_date - date.today()).days} jours restants"
    
    def get_user_role(self, user):
        """
        Détermine le rôle de l'utilisateur dans le projet.
        """
        if user.is_superuser:
            return 'Admin'
        elif user == self.coordinateur:
            return 'Coordinateur des Operations'
            #return 'Coordinateur'
        elif user == self.chef_project:
            return 'Chef de Projet'
        elif user == self.conducteur_travaux:
            return 'Conducteurs des Travaux'
        elif user in self.list_intervenant.all():
            return 'Intervenant'
        else:
            return 'Aucun'
    
    def get_user_by_role_name(self, role_name):
        """
        Récupère l'utilisateur ayant le rôle spécifié dans ce projet.
        Retourne None si aucun utilisateur ne correspond à ce rôle.
        """
        if role_name == 'Coordinateur des Operations':
            return self.coordinateur
        elif role_name == 'Chef de Projet':
            return self.chef_project
        elif role_name == 'Conducteurs des Travaux':
            return self.conducteur_travaux
        return None


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


class Phase(models.Model):
    name = models.CharField(max_length=100, default=None)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=None)

    def __str__(self):
        """
        Retourne une représentation textuelle de la phase.
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
        Retourne la durée de la phase en jours.
        """
        return (self.end_date - self.start_date).days
    
    def remaining_time(self):
        """
        Retourne le temps restant pour la phase en jours.
        """
        return (self.end_date - date.today()).days


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
