from django import forms
from .models import User
from ckeditor.widgets import CKEditorWidget



class MessageForm(forms.Form):
    objet = forms.CharField(max_length=200)
    messages = forms.CharField(required=False, widget=CKEditorWidget())
    recepteurs = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
    )
    documents = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        projet = kwargs.pop('projet', None)
        super(MessageForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['recepteurs'].queryset = User.objects.exclude(id=user.id)

        if projet:
            # Si un projet est spécifié, filtrez les utilisateurs en fonction de ce projet
            #self.fields['recepteurs'].queryset = projet.get_all_users().exclude(id=user.id) if user else projet.get_all_users()
            # Convertir les utilisateurs du projet en liste d'identifiants
            user_ids = [u.id for u in projet.get_all_users()]
            # Filtrer le queryset des récepteurs pour inclure uniquement les utilisateurs du projet
            self.fields['recepteurs'].queryset = User.objects.filter(id__in=user_ids)
