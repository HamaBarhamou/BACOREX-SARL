from django import forms
from .models import ExperienceSimilaire


class DaoForm(forms.Form):
    dao_number = forms.CharField(max_length=200)
    dao_title = forms.CharField(max_length=200)
    date_publication = forms.DateTimeField()
    date_soumission = forms.DateTimeField()
    document_link = forms.URLField()


class ExperienceSimilaireForm(forms.ModelForm):
    class Meta:
        model = ExperienceSimilaire
        fields = [
            "dao",
            "reference_marche",
            "objet",
            "description_travaux",
            "delai_execution_jours",
            "nom_client",
            "financement",
            "maitre_ouvrage",
            "montant_contrat",
            "date_demarrage_travaux",
            "date_fin_travaux",
            "document",
        ]
        widgets = {
            "dao": forms.Select(attrs={"class": "form-control"}),
            "reference_marche": forms.TextInput(attrs={"class": "form-control"}),
            "objet": forms.TextInput(attrs={"class": "form-control"}),
            "description_travaux": forms.Textarea(attrs={"class": "form-control"}),
            "delai_execution_jours": forms.NumberInput(attrs={"class": "form-control"}),
            "nom_client": forms.TextInput(attrs={"class": "form-control"}),
            "financement": forms.TextInput(attrs={"class": "form-control"}),
            "maitre_ouvrage": forms.TextInput(attrs={"class": "form-control"}),
            "montant_contrat": forms.NumberInput(attrs={"class": "form-control"}),
            "date_demarrage_travaux": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "date_fin_travaux": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "document": forms.FileInput(attrs={"class": "form-control"}),
        }
