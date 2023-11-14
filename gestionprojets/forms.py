from django import forms
from django.forms import ModelForm, Textarea, NumberInput
from django.forms import ClearableFileInput
from django.db import models
from .models import Client, Projet, Task, Phase
from django.utils.translation import gettext_lazy as _
from userprofile.models import User
from gestiondesstock.models import Materiels
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError



class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'adresse']


class ProjetForm(ModelForm):
    class Meta:
        model = Projet
        fields = '__all__'
        exclude = ('status',)
        labels = {
            'name': _('Nom du projet'),
            'start_date': _('Debut du projet'),
            'end_date': _('Fin du projet'),
            'status': _('Etat des travaux'),
            'pieces_jointes': _('Pieces jointes')
        }
        widgets = {
            'name': Textarea(attrs={'cols': 60, 'rows': 1}),
            'description': Textarea(attrs={'cols': 60, 'rows': 3}),
            'start_date': NumberInput(attrs={'type': 'date'}),
            'end_date': NumberInput(attrs={'type': 'date'}),
            'pieces_jointes': ClearableFileInput(attrs={'multiple': True})
        }
    coordinateur = forms.ModelChoiceField(
                        queryset=User.objects.filter(fonction=6),
                        label="Coordinateur Operation",
                        empty_label="Faite un choix",
                        )
    chef_project = forms.ModelChoiceField(
                        queryset=User.objects.filter(fonction=8),
                        label="Chef de Projet",
                        empty_label="Faite un choix",
                        )
    conducteur_travaux = forms.ModelChoiceField(
                            queryset=User.objects.filter(fonction=7),
                            label="Conducteur des Travaux",
                            empty_label="Faite un choix",
                            )
    list_intervenant = forms.ModelMultipleChoiceField(
                            queryset=User.objects.filter(fonction=11),
                            label="Liste des Intdervenants",
                            required=False,
                            widget=forms.CheckboxSelectMultiple
                            )
    list_materiels = forms.ModelMultipleChoiceField(
                        queryset=Materiels.objects.all(),
                        label="Liste des Materiels",
                        required=False,
                        widget=forms.CheckboxSelectMultiple
                        )
    pieces_jointes = forms.FileField(
                        required=False,
                        widget=forms.ClearableFileInput(
                                        attrs={'multiple': True}
                                        )
                        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ self.fields['name'].widget.attrs.update({'class': 'special'})
        self.fields['description'].widget.attrs.update(size='20') """


class TaskForm(ModelForm):
    list_materiels = forms.ModelMultipleChoiceField(
        queryset=Materiels.objects.all(),
        label="Liste des Materiels",
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    attribuer_a = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="Attribuer aux persones",
        widget=forms.CheckboxSelectMultiple
    )
    pieces_jointes = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Task
        fields = '__all__'
        #exclude = ('status', 'projet')
        exclude = ('projet',)
        labels = {
            'name': _('Nom de la tache'),
            'start_date': _('Debut de la tache'),
            'end_date': _('Fin de la tache'),
            'status': _('Etat des travaux'),
            'pieces_jointes': _('Pieces jointes')
        }
        widgets = {
            'name': Textarea(attrs={'cols': 60, 'rows': 1}),
            'description': Textarea(attrs={'cols': 60, 'rows': 3}),
            'start_date': NumberInput(attrs={'type': 'date'}),
            'end_date': NumberInput(attrs={'type': 'date'}),
            # 'pieces_jointes': ClearableFileInput(attrs={'multiple': True})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError(_("La date de fin de la tâche doit être postérieure à la date de début."))

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        projet = kwargs.pop('projet', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        if projet is not None:
            user_set = projet.get_all_users()  # Ceci est un set d'utilisateurs
            user_ids = [user.id for user in user_set]  # Convertir en liste d'IDs
            self.fields['attribuer_a'].queryset = User.objects.filter(id__in=user_ids)


class TaskLimitedForm(ModelForm):
    list_materiels = forms.ModelMultipleChoiceField(
        queryset=Materiels.objects.all(),
        label="Liste des Materiels",
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task
        fields = ['status', 'list_materiels']  # Les seuls champs que l'utilisateur peut modifier
        labels = {
            'status': _('Etat des travaux'),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Pas besoin de vérifier les dates ici car elles ne font pas partie du formulaire

        return cleaned_data


class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase
        fields = ['name', 'description', 'start_date', 'end_date']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class AgentForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Sélectionnez un agent"
    )

    def __init__(self, *args, **kwargs):
        projet = kwargs.pop('projet')
        super(AgentForm, self).__init__(*args, **kwargs)
        all_users_in_project = projet.get_all_users()
        self.fields['user'].queryset = User.objects.exclude(
            id__in=[user.id for user in all_users_in_project]
        )
