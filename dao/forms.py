from django import forms
from .models import (
    ExperienceSimilaire,
    DAO,
    Lot,
    ReponseDAO,
    RapportDepouillement,
    LigneRapport,
    OffreLot,
    Soumissionnaire,
    AttributionLot,
)
from django.forms import inlineformset_factory


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
            "dao_number": forms.TextInput(attrs={"class": "form-control"}),
            "dao_title": forms.TextInput(attrs={"class": "form-control"}),
            "date_publication": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "date_soumission": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "fichier": forms.FileInput(attrs={"class": "form-control"}),
            "is_closed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


# Création du formset pour les lots
LotFormSet = inlineformset_factory(
    DAO,
    Lot,
    fields=("nom_lot", "description"),
    extra=1,  # Nombre de formulaires vides à afficher
    can_delete=True,  # Permet la suppression des lots
    widgets={
        "nom_lot": forms.TextInput(attrs={"class": "form-control"}),
        "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    },
)


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
        widgets = {"dao": forms.HiddenInput()}


class LigneRapportForm(forms.ModelForm):
    nouveau_soumissionnaire = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nouveau soumissionnaire (si non existant)",
    )

    class Meta:
        model = LigneRapport
        fields = ["soumissionnaire", "observations"]
        widgets = {
            "soumissionnaire": forms.Select(attrs={"class": "form-control"}),
            "observations": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["soumissionnaire"].queryset = Soumissionnaire.objects.all()
        self.fields["soumissionnaire"].required = False

    def clean(self):
        cleaned_data = super().clean()
        soumissionnaire = cleaned_data.get("soumissionnaire")
        nouveau_soumissionnaire = cleaned_data.get("nouveau_soumissionnaire")

        if not soumissionnaire and not nouveau_soumissionnaire:
            raise forms.ValidationError(
                "Vous devez sélectionner un soumissionnaire existant ou en créer un nouveau."
            )

        if nouveau_soumissionnaire:
            soumissionnaire, created = Soumissionnaire.objects.get_or_create(
                nom=nouveau_soumissionnaire
            )
            cleaned_data["soumissionnaire"] = soumissionnaire

        return cleaned_data


class OffreLotForm(forms.ModelForm):
    class Meta:
        model = OffreLot
        fields = ["lot", "offre_financiere", "devise", "est_htva"]
        widgets = {
            "lot": forms.Select(attrs={"class": "form-control"}),
            "offre_financiere": forms.NumberInput(attrs={"class": "form-control"}),
            "devise": forms.Select(attrs={"class": "form-control"}),
            "est_htva": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


# Création des formsets
LigneRapportFormSet = inlineformset_factory(
    RapportDepouillement,
    LigneRapport,
    form=LigneRapportForm,
    extra=1,
    can_delete=True,
)

OffreLotFormSet = inlineformset_factory(
    LigneRapport, OffreLot, form=OffreLotForm, extra=1, can_delete=True
)


class AttributionLotForm(forms.ModelForm):
    class Meta:
        model = AttributionLot
        fields = [
            "soumissionnaire",
            "statut",
            "motif_rejet",
            "document_attribution",
            "date_attribution",
            "observations",
        ]
        widgets = {
            "soumissionnaire": forms.Select(attrs={"class": "form-select"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
            "date_attribution": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "motif_rejet": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "observations": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def __init__(self, *args, lot=None, **kwargs):
        super().__init__(*args, **kwargs)
        if lot:
            # Filtrer les soumissionnaires qui ont fait une offre pour ce lot
            offres = OffreLot.objects.filter(lot=lot)
            soumissionnaires_ids = offres.values_list(
                "ligne_rapport__soumissionnaire", flat=True
            )
            self.fields["soumissionnaire"].queryset = Soumissionnaire.objects.filter(
                id__in=soumissionnaires_ids
            )
            # Initialiser le lot (qui n'est pas dans le formulaire)
            self.instance.lot = lot


class ExperienceSimilaireForm(forms.ModelForm):
    class Meta:
        model = ExperienceSimilaire
        fields = [
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
