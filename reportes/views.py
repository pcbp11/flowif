from django.shortcuts import render, redirect
from .models import Ingresos, Gastos, FlujodeCaja
from .forms import IngresosForm, GastosForm

def index(request):
    return render(request, 'reportes/index.html')

def flujodecaja_view(request):
    flujos = FlujodeCaja.objects.all()  # Recuperar todos los registros de FlujodeCaja

    # Crear una lista de flujos con los valores formateados
    flujos_con_formato = []
    for flujo in flujos:
        flujo_dict = {
            'fecha_inicio': flujo.fecha_inicio,
            'fecha_fin': flujo.fecha_fin,
            'total_ingresos': f"{flujo.total_ingresos:,}".replace(",", "."),
            'total_gastos': f"{flujo.total_gastos:,}".replace(",", "."),
            'balance': f"{flujo.balance:,}".replace(",", ".")
        }
        flujos_con_formato.append(flujo_dict)

    return render(request, 'reportes/flujodecaja.html', {'flujos': flujos_con_formato})



def ingresos_view(request):
    ingresos = Ingresos.objects.all()  # Recuperar todos los registros de Ingresos
    if request.method == 'POST':
        form = IngresosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingresos')
    else:
        form = IngresosForm()
    return render(request, 'reportes/ingresos.html', {'ingresos': ingresos, 'form': form})

def gastos_view(request):
    gastos = Gastos.objects.all()  # Recuperar todos los registros de Gastos
    if request.method == 'POST':
        form = GastosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gastos')
    else:
        form = GastosForm()

    # Crear una lista de gastos con los montos formateados
    gastos_con_formato = []
    for gasto in gastos:
        try:
            monto_int = int(gasto.monto)  # Convertir el monto a entero
            monto_formateado = f"{monto_int:,}".replace(",", ".")  # Formatear el monto con puntos
            gastos_con_formato.append({
                'fecha': gasto.fecha,
                'monto_formateado': monto_formateado,
                'categoria': gasto.categoria,
                'descripcion': gasto.descripcion
            })
        except (ValueError, TypeError) as e:
            print(f"Error al formatear el monto: {e}")

    return render(request, 'reportes/gastos.html', {'gastos': gastos_con_formato, 'form': form})
