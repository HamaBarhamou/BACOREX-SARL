from django import forms

class DaoForm(forms.Form):
    dao_number = forms.CharField(label='AA0/ OOA', max_length=200)
    dao_title = forms.CharField(label='Tile', max_length=200)
    date_publication = forms.DateTimeField(label='Date')
    date_soumission = forms.DateTimeField(label='Date')
    document_link = forms.CharField(label=' N AA0/ OOA', max_length=500)