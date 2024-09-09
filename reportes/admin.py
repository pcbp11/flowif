from django.contrib import admin
from django import forms
from .models import Ingresos, Gastos, FlujodeCaja
from .widgets import CurrencyInput
from django.templatetags.static import static 


# Definir formularios personalizados
class IngresosAdminForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        fields = '__all__'
        widgets = {
            'monto': CurrencyInput(),  # Usar el widget personalizado para el campo 'monto'
        }

class GastosAdminForm(forms.ModelForm):
    class Meta:
        model = Gastos
        fields = '__all__'
        widgets = {
            'monto': CurrencyInput(),  # Usar el widget personalizado para el campo 'monto'
        }

def format_currency(value):
    if value is None:
        return "-"
    return "${:,.0f}".format(value).replace(",", ".")


# Registro de modelos en el admin usando los formularios personalizados
@admin.register(Ingresos)
class IngresosAdmin(admin.ModelAdmin):
    form = IngresosAdminForm
    list_display = ('fecha', 'monto_formateado', 'categoria', 'descripcion')
    search_fields = ('fecha', 'categoria')

    def monto_formateado(self, obj):
        return format_currency(obj.monto)
    monto_formateado.short_description = 'Monto'


    class Media:
        js = (static('reportes/admin.js'),)


@admin.register(Gastos)
class GastosAdmin(admin.ModelAdmin):
    form = GastosAdminForm
    list_display = ('fecha', 'monto_formateado', 'categoria', 'descripcion')
    search_fields = ('fecha', 'categoria')

    def monto_formateado(self, obj):
        return format_currency(obj.monto)  # Utiliza la función personalizada para mostrar el monto con el formato correcto
    monto_formateado.short_description = 'Monto'

    class Media:
        js = (static('reportes/admin.js'),)


@admin.register(FlujodeCaja)
class FlujodeCajaAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'total_ingresos_formateado', 'total_gastos_formateado', 'balance_formateado')
    ordering = ('fecha_inicio',)

    def total_ingresos_formateado(self, obj):
        return format_currency(obj.total_ingresos)
    total_ingresos_formateado.short_description = 'Total Ingresos'

    def total_gastos_formateado(self, obj):
        return format_currency(obj.total_gastos)
    total_gastos_formateado.short_description = 'Total Gastos'

    def balance_formateado(self, obj):
        return format_currency(obj.balance)
    balance_formateado.short_description = 'Balance'

    class Media:
        js = (static('reportes_financieros/admin.js'),)
