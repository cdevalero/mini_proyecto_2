from django import forms
from django.forms import DateInput
from .models import Cliente

class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('identificacion','nombre','apellido','direccion')