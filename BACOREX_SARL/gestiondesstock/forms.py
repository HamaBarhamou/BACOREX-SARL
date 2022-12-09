from django import forms
from django.forms import ModelForm
from django.db import models
from .models import CategoriMateriel
from .models import Entrepot, Materiels


class CategoriMaterielForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(required=False, widget=forms.Textarea)

class EntrepotForm(forms.Form):
    name = forms.CharField(max_length=50)
    adresse = forms.CharField(max_length=100)

#class MaterielsForm(ModelForm):
class MaterielsForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(required=False, widget=forms.Textarea)
    qte = forms.IntegerField()
    categorie = forms.ModelChoiceField(queryset=CategoriMateriel.objects.all(),
                                       empty_label="Categories du materiels")
    entrepot = forms.ModelChoiceField(queryset=Entrepot.objects.all(),
                                       empty_label="Entrepot")
    #image = forms.ImageField()
    image = forms.FileField()

    """ class Meta:
        model = Materiels
        fields = ['name', 'description', 'qte', 'categorie', 'entrepot', 'image'] """