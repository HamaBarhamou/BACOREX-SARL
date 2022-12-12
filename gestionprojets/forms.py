from django import forms
from django.forms import ModelForm, Textarea
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
    start_date = forms.DateField(widget=forms.SelectDateWidget(),
                                 label="Debut du Projet"
                                 )

    end_date = forms.DateField(widget=forms.SelectDateWidget(),
                               label="Fin du Projet"
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ self.fields['name'].widget.attrs.update({'class': 'special'})
        self.fields['description'].widget.attrs.update(size='20') """
