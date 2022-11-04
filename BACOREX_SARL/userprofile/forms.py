#from django.forms import ModelForm
from django import forms
from .models import Profile

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    
    """class Meta:
        model = Profile
        fields = ['user', 'avatar', 'fonction']"""