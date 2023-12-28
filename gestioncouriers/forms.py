from django import forms
from .models import User, MessagePredefini
from ckeditor.widgets import CKEditorWidget



class MessageForm(forms.Form):

    message_predefini = forms.ModelChoiceField(
        queryset=MessagePredefini.objects.none(),  # Initialisé à none, sera mis à jour dans __init__
        required=False,
        label='Message prédéfini'
    )

    objet = forms.CharField(max_length=200)
    messages = forms.CharField(required=False, widget=CKEditorWidget())
    recepteurs = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
    )

    documents = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    # Création du dictionnaire ROLE_MAPPING à partir des USER_TYPE_CHOICES
    ROLE_MAPPING = {label: value for value, label in User.USER_TYPE_CHOICES}


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        projet = kwargs.pop('projet', None)
        super(MessageForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['recepteurs'].queryset = User.objects.exclude(id=user.id)

        #print('projet=',projet)
        if projet:
            # Convertir les utilisateurs du projet en liste d'identifiants
            user_ids = [u.id for u in projet.get_all_users()]
            # Filtrer le queryset des récepteurs pour inclure uniquement les utilisateurs du projet
            self.fields['recepteurs'].queryset = User.objects.filter(id__in=user_ids)

            # Obtenez les rôles de l'utilisateur dans le projet
            #print('ROLE_MAPPING=',self.ROLE_MAPPING)
            user_role_str = projet.get_user_role(user)
            #print('user_role_str=',user_role_str)
            user_role_value = self.ROLE_MAPPING.get(user_role_str)
            #print('user_role_value=',user_role_value)
            # Filtrer les messages prédéfinis en fonction des rôles de l'utilisateur
            if user_role_value is not None:
                self.fields['message_predefini'].queryset = MessagePredefini.objects.filter(expeditaire_role=user_role_value)
                self.fields['message_predefini'].label_from_instance = lambda obj: f"{obj.titre}"
                #print("Queryset mis à jour pour message_predefini: ", self.fields['message_predefini'].queryset)
            else:
                # Masquer le champ si aucun rôle n'est déterminé
                self.fields['message_predefini'].widget = forms.HiddenInput()

    def update_messages_field(self, message_predefini_id):
        try:
            message_predefini = MessagePredefini.objects.get(id=message_predefini_id)
            self.fields['messages'].initial = message_predefini.corps
        except MessagePredefini.DoesNotExist:
            pass