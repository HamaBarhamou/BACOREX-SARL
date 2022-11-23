from django import forms
from django.db import models
from userprofile.models import User

class MessageForm(forms.Form):
    messages = forms.CharField(required=False, widget=forms.Textarea)
    #emetteur = forms.ModelChoiceField(queryset=None, empty_label="(Nothing)")
    recepteur = forms.ModelChoiceField(queryset=None, empty_label="(Destinataire du message)")
    date_envoie = forms.DateTimeField()
    status_envoie = forms.BooleanField()
    