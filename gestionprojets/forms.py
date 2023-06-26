from django import forms
from django.forms import ModelForm, Textarea, NumberInput
from django.forms import ClearableFileInput
from django.db import models
from .models import Client, Projet, Task
from django.utils.translation import gettext_lazy as _
from userprofile.models import User
from gestiondesstock.models import Materiels
from django.contrib.admin.widgets import AdminDateWidget


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
        exclude = ('status', 'projet')
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
