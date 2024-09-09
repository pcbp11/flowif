from django import forms
from django.utils.safestring import mark_safe

class CurrencyInput(forms.NumberInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'currency', 'style': 'text-align: right;'})

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        # Usar mark_safe para asegurar que el HTML se renderice correctamente
        return mark_safe(f'<span>$</span> {super().render(name, value, attrs, renderer)}')
