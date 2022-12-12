from django import forms
from django.forms import ModelForm, Textarea
from django.db import models
from .models import Client, Projet, Task
from django.utils.translation import gettext_lazy as _
from userprofile.models import User
from gestiondesstock.models import Materiels


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'adresse']


class ProjetForm(ModelForm):
    chef_project = forms.ModelChoiceField(queryset=User.objects.filter(fonction=8),
                                          label="Chef de Projet",
                                          empty_label="Faite un choix",
                                          )
    conducteur_travaux = forms.ModelChoiceField(queryset=User.objects.filter(fonction=7),
                                          label="Conducteur des Travaux",
                                          empty_label="Faite un choix",
                                          )
    list_intervenant = forms.ModelMultipleChoiceField(queryset=User.objects.filter(fonction=11),
                                          label="Liste des Intdervenants",
                                          required=False,
                                          widget=forms.CheckboxSelectMultiple
                                          )
    list_materiels = forms.ModelMultipleChoiceField(queryset=Materiels.objects.all(),
                                          label="Liste des Materiels",
                                          required=False,
                                          widget=forms.CheckboxSelectMultiple
                                          )
    class Meta:
        model = Projet
        fields = '__all__'
        labels = {
            'name': _('Nom du projet'),
            'start_date': _('Date du debut des travaux'),
            'end_date': _('Date de fin des travaux'),
            'status': _('Etat des travaux'),
            'pieces_jointes': _('Pieces jointes')
        }
        widgets = {
            'name': Textarea(attrs={'cols': 60, 'rows': 1}),
            'description': Textarea(attrs={'cols': 60, 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs.update({'class': 'special'})
        #self.fields['description'].widget.attrs.update(size='20')