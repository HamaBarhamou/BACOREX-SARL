from django import forms
from .models import (
    ExperienceSimilaire,
    DAO,
    Lot,
    ReponseDAO,
    RapportDepouillement,
    LigneRapport,
    OffreLot,
)


class DAOForm(forms.ModelForm):
    class Meta:
        model = DAO
        fields = [
            "dao_number",
            "dao_title",
            "date_publication",
            "date_soumission",
            "is_closed",
            "fichier",
        ]
        widgets = {
            "date_publication": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "date_soumission": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fichier": forms.FileInput(attrs={"class": "form-control"}),
        }


class LotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ["dao", "nom_lot", "description"]


class ReponseDAOForm(forms.ModelForm):
    class Meta:
        model = ReponseDAO
        fields = ["type_reponse", "fichier", "url"]  # Retiré 'dao' des fields
        widgets = {
            "type_reponse": forms.Select(attrs={"class": "form-control"}),
            "fichier": forms.FileInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
        }


class RapportDepouillementForm(forms.ModelForm):
    class Meta:
        model = RapportDepouillement
        fields = ["dao"]


class LigneRapportForm(forms.ModelForm):
    class Meta:
        model = LigneRapport
        fields = ["rapport", "nom_soumissionnaire", "observations"]


class OffreLotForm(forms.ModelForm):
    class Meta:
        model = OffreLot
        fields = ["ligne_rapport", "lot", "offre_financiere"]


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
