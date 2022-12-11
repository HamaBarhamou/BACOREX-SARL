from django import forms
from django.forms import ModelForm
from django.db import models
from .models import Client, Projet, Task


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'adresse']


class ProjetForm(ModelForm):
    class Meta:
        model = Projet
        fields = ['name',
                  'description',
                  'start_date',
                  'end_date',
                  'chef_project',
                  'conducteur_travaux',
                  'list_intervenant',
                  'list_materiels',
                  'client',
                  'status',
                  'budget',
                  'pieces_jointes'
                ]