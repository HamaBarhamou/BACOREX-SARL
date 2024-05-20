from django import forms
from .models import DAO, ExperienceSimilaire


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
            "delai_execution_mois",
            "nom_client",
            "financement",
            "maitre_ouvrage",
            "montant_contrat",
            "date_demarrage_travaux",
            "date_fin_travaux",
            "document",
        ]
