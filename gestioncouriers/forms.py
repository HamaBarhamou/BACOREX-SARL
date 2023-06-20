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
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['recepteurs'].queryset = User.objects.exclude(id=user.id)

