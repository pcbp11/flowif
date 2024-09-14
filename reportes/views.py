from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Ingresos, Gastos, FlujodeCaja
from .forms import IngresosForm, GastosForm
from django.db.models import Sum


# Vista para el registro de usuarios
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loguear al usuario automáticamente después del registro
            return redirect('index')  # Redirigir a la página principal después del registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Vista principal
@login_required  # Requiere que el usuario esté logueado para ver la página principal
def index(request):
    return render(request, 'reportes/index.html')


@login_required
def flujodecaja_view(request):
    ingresos = Ingresos.objects.all()
    gastos = Gastos.objects.all()

    if ingresos.exists() or gastos.exists():
        total_ingresos = ingresos.aggregate(Sum('monto'))['monto__sum'] or 0
        total_gastos = gastos.aggregate(Sum('monto'))['monto__sum'] or 0
        balance = total_ingresos - total_gastos

        fecha_inicio = ingresos.order_by('fecha').first()
        fecha_fin = ingresos.order_by('-fecha').first()

        fecha_inicio = fecha_inicio.fecha if fecha_inicio and fecha_inicio.fecha else "N/A"
        fecha_fin = fecha_fin.fecha if fecha_fin and fecha_fin.fecha else "N/A"

        flujo = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_ingresos': f"{total_ingresos:,}".replace(",", "."),
            'total_gastos': f"{total_gastos:,}".replace(",", "."),
            'balance': f"{balance:,}".replace(",", "."),
        }

        return render(request, 'reportes/flujodecaja.html', {'flujos': [flujo]})
    else:
        flujo = {
            'fecha_inicio': "N/A",
            'fecha_fin': "N/A",
            'total_ingresos': 0,
            'total_gastos': 0,
            'balance': 0,
        }
        return render(request, 'reportes/flujodecaja.html', {'flujos': [flujo]})


@login_required
def ingresos_view(request):
    ingresos = Ingresos.objects.all()
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
            monto_int = int(float(ingreso.monto))
            monto_formateado = f"{monto_int:,}".replace(",", ".")
        except (ValueError, TypeError) as e:
            print(f"Error al formatear el monto: {e}")
            monto_formateado = "Error"

        ingresos_con_formato.append({
            'fecha': ingreso.fecha,
            'monto': monto_formateado,
            'categoria': ingreso.categoria,
            'descripcion': ingreso.descripcion if ingreso.descripcion else ""
        })

    return render(request, 'reportes/ingresos.html', {'ingresos': ingresos_con_formato, 'form': form})


@login_required
def gastos_view(request):
    gastos = Gastos.objects.all()
    if request.method == 'POST':
        form = GastosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gastos')
    else:
        form = GastosForm()

    gastos_con_formato = []
    for gasto in gastos:
        try:
            monto_int = int(gasto.monto)
            monto_formateado = f"{monto_int:,}".replace(",", ".")
            gastos_con_formato.append({
                'fecha': gasto.fecha,
                'monto_formateado': monto_formateado,
                'categoria': gasto.categoria,
                'descripcion': gasto.descripcion
            })
        except (ValueError, TypeError) as e:
            print(f"Error al formatear el monto: {e}")

    return render(request, 'reportes/gastos.html', {'gastos': gastos_con_formato, 'form': form})
