from django import forms
from .models import DAO

class DaoForm(forms.Form):
    dao_number = forms.CharField(max_length=200)
    dao_title = forms.CharField(max_length=200)
    date_publication = forms.DateTimeField()
    date_soumission = forms.DateTimeField()
    document_link = forms.CharField(max_length=500)
    """class Meta:
        model = DAO
        fields = (
                    'dao_number',
                    'dao_title', 
                    'date_publication',
                    'date_soumission',
                    'document_link'
                )
        """