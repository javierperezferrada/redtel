from django import forms
from .models import Mensaje

class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Selecciones archivo csv'
    )

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ('msg',)