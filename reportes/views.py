from django.shortcuts import render, redirect
from .models import Ingresos, Gastos, FlujodeCaja
from .forms import IngresosForm, GastosForm
from django.db.models import Sum


def index(request):
    return render(request, 'reportes/index.html')

def flujodecaja_view(request):
    ingresos = Ingresos.objects.all()
    gastos = Gastos.objects.all()

    print(f"Cantidad de ingresos: {ingresos.count()}")
    print(f"Cantidad de gastos: {gastos.count()}")

    if ingresos.exists() or gastos.exists():
        total_ingresos = ingresos.aggregate(Sum('monto'))['monto__sum'] or 0
        total_gastos = gastos.aggregate(Sum('monto'))['monto__sum'] or 0
        balance = total_ingresos - total_gastos

        fecha_inicio = ingresos.order_by('fecha').first()
        fecha_fin = ingresos.order_by('-fecha').first()

        fecha_inicio = fecha_inicio.fecha if fecha_inicio and fecha_inicio.fecha else "N/A"
        fecha_fin = fecha_fin.fecha if fecha_fin and fecha_fin.fecha else "N/A"

        # Crear un flujo con formato y agregarlo a una lista
        flujo = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_ingresos': f"{total_ingresos:,}".replace(",", "."),
            'total_gastos': f"{total_gastos:,}".replace(",", "."),
            'balance': f"{balance:,}".replace(",", "."),
        }

        # Enviamos una lista con un solo flujo
        return render(request, 'reportes/flujodecaja.html', {'flujos': [flujo]})
    else:
        print("No hay ingresos ni gastos registrados.")
        flujo = {
            'fecha_inicio': "N/A",
            'fecha_fin': "N/A",
            'total_ingresos': 0,
            'total_gastos': 0,
            'balance': 0,
        }
        return render(request, 'reportes/flujodecaja.html', {'flujos': [flujo]})


def ingresos_view(request):
    ingresos = Ingresos.objects.all()  # Recuperar todos los registros de Ingresos
    if request.method == 'POST':
        form = IngresosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingresos')
    else:
        form = IngresosForm()

    ingresos_con_formato = []
    for ingreso in ingresos:
        try:
            monto_int = int(float(ingreso.monto))  # Convertir el monto a entero
            monto_formateado = f"{monto_int:,}".replace(",", ".")  # Formatear el monto con puntos y signo de peso
        except (ValueError, TypeError) as e:
            print(f"Error al formatear el monto: {e}")
            monto_formateado = "Error"  # Manejar cualquier error en el formateo

        ingresos_con_formato.append({
            'fecha': ingreso.fecha,
            'monto': monto_formateado,
            'categoria': ingreso.categoria,
            'descripcion': ingreso.descripcion if ingreso.descripcion else ""  # Evita mostrar None
        })

    return render(request, 'reportes/ingresos.html', {'ingresos': ingresos_con_formato, 'form': form})



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
