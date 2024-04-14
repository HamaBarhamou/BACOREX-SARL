from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone
from userprofile.models import User
from gestiondesstock.models import Materiels
from django.db.models import Q
from django_notifly.utils import send_notification, PURCHASE_REQUEST
from django.urls import reverse


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=50, default=None)
    adresse = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.name


class Projet(models.Model):
    STATUS = (
        (1, "NON DÉBUTÉ"),
        (2, "EN COURS"),
        (3, "TERMINER"),
        (4, "ARCHIVER"),
    )

    name = models.CharField(max_length=100, default=None)
    description = models.TextField(default=None)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    coordinateur = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cordinateur_projet", default=None
    )
    chef_project = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chef_project", default=None
    )
    conducteur_travaux = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="conducteur_travaux", default=None
    )
    directeur_energie = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="directeur_energie",
        default=None,
        null=True,
    )
    daf = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="daf", default=None, null=True
    )
    pdg = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pdg", default=None, null=True
    )
    list_intervenant = models.ManyToManyField(User, related_name="intervenant")
    list_materiels = models.ManyToManyField(Materiels)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    budget = models.IntegerField(default=0)
    pieces_jointes = models.FileField(
        verbose_name="image", upload_to="media/upload/documents", null=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from plannig.models import Event

        event = Event.objects.filter(pk_projet=self.pk).first()
        if event is None:
            event = Event(
                title=self.name,
                description=self.description,
                start_time=self.start_date,
                end_time=self.end_date,
                pk_projet=self.pk,
            )
        else:
            event.title = self.name
            event.description = self.description
            event.start_time = self.start_date
            event.end_time = self.end_date
        event.save()

    def delete(self, *args, **kwargs):
        from plannig.models import Event

        Event.objects.filter(pk_projet=self.pk).first().delete()
        super(Projet, self).delete(*args, **kwargs)

    def pourcentage_achevement(self):
        taches = self.task_set.all()
        total_taches = taches.count()
        taches_terminees = taches.filter(status=3).count()
        if total_taches > 0:
            pourcentage_achevement = (taches_terminees / total_taches) * 100
        else:
            pourcentage_achevement = 0
        pourcentage_achevement_str = "{:.2f}".format(pourcentage_achevement).replace(
            ",", "."
        )
        return pourcentage_achevement_str

    @staticmethod
    def get_projects_by_user(user):
        if user.is_leader():
            return Projet.objects.all()
        projects = Projet.objects.filter(
            Q(chef_project=user) | Q(conducteur_travaux=user) | Q(list_intervenant=user)
        )
        tasks = Task.objects.filter(attribuer_a=user)
        for task in tasks:
            projects |= Projet.objects.filter(pk=task.projet.pk)
        return projects.distinct()

    # Retourner tous les utilisateurs impliqués dans un projet
    def get_all_users(self):
        users = set(
            [
                self.coordinateur,
                self.chef_project,
                self.conducteur_travaux,
                self.directeur_energie,
                self.daf,
                self.pdg,
            ]
        )
        users.update(self.list_intervenant.all())
        tasks = self.task_set.all()
        for task in tasks:
            users.update(task.attribuer_a.all())
        users.discard(None)
        return users

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "coordinateur": self.coordinateur.get_full_name()
            if self.coordinateur
            else None,
            "chef_project": self.chef_project.get_full_name()
            if self.chef_project
            else None,
            "conducteur_travaux": self.conducteur_travaux.get_full_name()
            if self.conducteur_travaux
            else None,
            "status": self.get_status_display(),
            "budget": self.budget,
            "pourcentage_achevement": self.pourcentage_achevement(),
        }
        if date.today() < self.start_date:
            days_until_start = (self.start_date - date.today()).days
            data["days_remaining"] = f"Commence dans {days_until_start} jours"
        elif date.today() > self.end_date:
            data["days_remaining"] = "Terminé"
        else:
            days_remaining = (self.end_date - date.today()).days
            data["days_remaining"] = f"{days_remaining} jours restants"
        return data

    def days_remaining(self):
        if date.today() < self.start_date:
            return f"Commence dans {(self.start_date - date.today()).days} jours"
        elif date.today() > self.end_date:
            return "Terminé"
        else:
            return f"{(self.end_date - date.today()).days} jours restants"

    def jours_restant(self):
        return (self.end_date - date.today()).days

    def get_user_role(self, user):
        """
        Détermine le rôle de l'utilisateur dans le projet.
        """
        if user.is_superuser:
            return "Admin"
        elif user == self.coordinateur:
            return "Coordinateur des Operations"
        elif user == self.chef_project:
            return "Chef de Projet"
        elif user == self.conducteur_travaux:
            return "Conducteurs des Travaux"
        elif user in self.list_intervenant.all():
            return "Intervenant"
        elif user == self.directeur_energie:
            return "Directeur Energie"
        elif user == self.daf:
            return "Directeur Administratif et Financier"
        elif user == self.pdg:
            return "Président Directeur Générale"
        else:
            return "Aucun"

    def get_user_by_role_name(self, role_name):
        """
        Récupère l'utilisateur ayant le rôle spécifié dans ce projet.
        Retourne None si aucun utilisateur ne correspond à ce rôle.
        """
        if role_name == "Coordinateur des Operations":
            return self.coordinateur
        elif role_name == "Chef de Projet":
            return self.chef_project
        elif role_name == "Conducteurs des Travaux":
            return self.conducteur_travaux
        elif role_name == "Directeur Energie":
            return self.directeur_energie
        elif role_name == "PDG":
            return self.pdg
        elif role_name == "DAF":
            return self.daf
        return None

    def get_user_by_type_choice(self, id):
        USER_TYPE_CHOICES = {
            4: "Directeur Energie",
            6: "Coordinateur des Operations",
            7: "Conducteurs des Travaux",
            8: "Chef de Projet",
            12: "PDG",
            13: "DAF",
            # 11: 'Intervenant',
        }

        return USER_TYPE_CHOICES[id]


class Task(models.Model):
    STATUS = (
        (1, "NON DÉBUTÉ"),
        (2, "EN COURS"),
        (3, "Terminer"),
    )
    name = models.CharField(max_length=100, default=None)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    list_materiels = models.ManyToManyField(Materiels)
    budget = models.IntegerField(default=0)
    attribuer_a = models.ManyToManyField(User, related_name="attribuer_a")
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=None)
    pieces_jointes = models.FileField(
        verbose_name="image",
        upload_to="media/upload/documents",
        null=True,
        blank=True,
        default=None,
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
            raise ValidationError(
                "La date de fin ne peut pas être antérieure à la date de début."
            )

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
            raise ValidationError(
                "La date de fin ne peut pas être antérieure à la date de début."
            )

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


class Achat(models.Model):
    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("approuve", "Approuvé"),
        ("rejete", "Rejeté"),
    ]
    STATUT_CHOICES_2 = [
        ("non_envoyer", "Non Envoyer"),
        ("envoyer", "Envoyer"),
        ("archiver", "Archiver"),
    ]
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUT_CHOICES_2, default="non_envoyer"
    )
    approbation_dg_coordinateur = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="en_attente"
    )
    approbation_daf = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="en_attente"
    )
    approbation_pdg = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="en_attente"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def approuver(self, user):
        """
        Met à jour le statut d'approbation en fonction du rôle de l'utilisateur.
        """
        notification_url = reverse(
            "projectmanagement:liste_achats", kwargs={"projet_id": self.projet.id}
        )
        message_approuve = (
            f"La demande d'achat #{self.id} a été approuvée par {user.username}"
        )
        message_demande = (
            f"La demande d'achat #{self.id} est en attente de votre approbation."
        )
        recipients_approuve = []
        recipients_demande = []

        if user.is_chefDeProjet():
            self.status = "envoyer"
            recipients_demande = [
                self.projet.coordinateur,
                self.projet.directeur_energie,
            ]
        elif user.is_coordinateur_or_directeur_energie():
            self.approbation_dg_coordinateur = "approuve"
            recipients_approuve = [self.projet.chef_project]
            recipients_demande = [self.projet.daf]
        elif user.is_daf():
            self.approbation_daf = "approuve"
            recipients_approuve = [
                self.projet.coordinateur,
                self.projet.directeur_energie,
                self.projet.chef_project,
            ]
            recipients_demande = [self.projet.pdg]
        elif user.is_pdg():
            self.approbation_pdg = "approuve"
            recipients_approuve = [
                self.projet.daf,
                self.projet.coordinateur,
                self.projet.directeur_energie,
                self.projet.chef_project,
            ]
        else:
            return

        self.save()

        # Envoyer les notifications d'approbation
        if recipients_approuve:
            send_notification(
                notification_type=PURCHASE_REQUEST,
                message=message_approuve,
                url=notification_url,
                recipients=recipients_approuve,
            )

        # Envoyer les notifications de demande d'approbation
        if recipients_demande:
            send_notification(
                notification_type=PURCHASE_REQUEST,
                message=message_demande,
                url=notification_url,
                recipients=recipients_demande,
            )

    def rejeter(self, user):
        """
        Révoque une approbation si les conditions pour la révocation sont remplies.
        """
        if not self.peut_rejeter(user):
            return False  # Ajoutez une gestion appropriée pour informer l'utilisateur que la révocation n'est pas possible

        if user.is_chefDeProjet():
            self.status = "non_envoyer"
        elif user.is_coordinateur_or_directeur_energie():
            self.approbation_dg_coordinateur = "rejete"
        elif user.is_daf():
            self.approbation_daf = "rejete"
        elif user.is_pdg():
            self.approbation_pdg = "rejete"

        self.save()
        # Envoyer la notification de révocation
        self.envoyer_notification_de_rejet(user)

        return True

    def peut_rejeter(self, user):
        """
        Détermine si une approbation peut être révoquée par l'utilisateur en fonction de l'état actuel des approbations.
        """
        if user.is_daf() and self.approbation_pdg == "en_attente":
            return True
        if (
            user.is_coordinateur_or_directeur_energie()
            and self.approbation_daf == "en_attente"
        ):
            return True
        if (
            user.is_chefDeProjet()
            and self.approbation_dg_coordinateur == "en_attente"
            and self.status == "envoyer"
        ):
            return True
        return False

    def envoyer_notification_de_rejet(self, user):
        """
        Envoie une notification indiquant que la demande a été révoquée.
        """
        notification_url = reverse(
            "projectmanagement:liste_achats", kwargs={"projet_id": self.projet.id}
        )
        message = f"La demande d'achat #{self.id} a été révoquée par {user.username}."
        recipients = []

        if user.is_coordinateur_or_directeur_energie():
            recipients = [self.projet.chef_project]
        elif user.is_daf():
            recipients = [
                self.projet.chef_project,
                self.projet.coordinateur,
                self.projet.directeur_energie,
            ]
        elif user.is_pdg():
            recipients = [
                self.projet.chef_project,
                self.projet.coordinateur,
                self.projet.directeur_energie,
                self.projet.daf,
            ]

        send_notification(
            notification_type="PURCHASE_REQUEST_REJECTED",  # Modifier pour refléter le type d'action
            message=message,
            url=notification_url,
            recipients=recipients,
        )


class ArticleAchat(models.Model):
    achat = models.ForeignKey(Achat, related_name="articles", on_delete=models.CASCADE)
    article = models.CharField(max_length=200)
    prix = models.PositiveIntegerField()
    quantite = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.article} - {self.quantite}"
