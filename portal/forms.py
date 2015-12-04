from django import forms

class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Selecciones archivo csv'
    )