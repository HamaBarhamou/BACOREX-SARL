from django import forms
from django.db import models
from models import CategoriMateriel


class CategoriMaterielForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)

class MaterielsForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    categorie = forms.ModelChoiceField(queryset=CategoriMateriel.objects.all(),
                                       empty_label="Destinateur du message")
     