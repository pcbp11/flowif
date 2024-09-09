from django import forms
from .models import Ingresos, Gastos

class IngresosForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        fields = ['fecha', 'monto', 'categoria', 'descripcion']

class GastosForm(forms.ModelForm):
    class Meta:
        model = Gastos
        fields = ['fecha', 'monto', 'categoria', 'descripcion']
