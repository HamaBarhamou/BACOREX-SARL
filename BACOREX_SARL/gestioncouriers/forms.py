from django import forms
from django.db import models
from userprofile.models import User

class MessageForm(forms.Form):
    messages = forms.CharField(required=False, widget=forms.Textarea)
    recepteur = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Destinateur du message")
    
    