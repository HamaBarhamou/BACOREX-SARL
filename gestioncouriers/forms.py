from django import forms
from .models import User
from ckeditor.widgets import CKEditorWidget

class MessageForm(forms.Form):
    objet = forms.CharField(max_length=200)
    messages = forms.CharField(required=False, widget=CKEditorWidget())
    recepteurs = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    documents = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
