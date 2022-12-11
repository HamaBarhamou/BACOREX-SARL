from django import forms
from django.forms import ModelForm
from django.db import models
from .models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'adresse']