from django import forms
from .models import User, MessagePredefini
from ckeditor.widgets import CKEditorWidget


class MessageForm(forms.Form):
    message_predefini = forms.ModelChoiceField(
        queryset=MessagePredefini.objects.none(),
        required=False,
        label="Message prédéfini",
    )
    objet = forms.CharField(max_length=200)
    messages = forms.CharField(required=False, widget=CKEditorWidget())
    recepteurs = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
    )
    documents = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False
    )
    ROLE_MAPPING = {label: value for value, label in User.USER_TYPE_CHOICES}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        projet = kwargs.pop("projet", None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["recepteurs"].queryset = User.objects.exclude(id=user.id)
        if projet:
            user_ids = [u.id for u in projet.get_all_users()]
            self.fields["recepteurs"].queryset = User.objects.filter(id__in=user_ids)
            user_role_str = projet.get_user_role(user)
            user_role_value = self.ROLE_MAPPING.get(user_role_str)
            if user_role_value is not None:
                self.fields[
                    "message_predefini"
                ].queryset = MessagePredefini.objects.filter(
                    expeditaire_role=user_role_value
                )
                self.fields[
                    "message_predefini"
                ].label_from_instance = lambda obj: f"{obj.titre}"
            else:
                self.fields["message_predefini"].widget = forms.HiddenInput()

    def update_messages_field(self, message_predefini_id):
        try:
            message_predefini = MessagePredefini.objects.get(id=message_predefini_id)
            self.fields["messages"].initial = message_predefini.corps
        except MessagePredefini.DoesNotExist:
            pass
