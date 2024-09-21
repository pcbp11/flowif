from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum
from decimal import Decimal
from django.contrib import messages
from .models import Ingresos, Gastos, FlujodeCaja
from .forms import IngresosForm, GastosForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('reportes:index')
    else:
        form = UserCreationForm()
    return render(request, 'reportes/registro.html', {'form': form})

@login_required
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

        fecha_inicio = fecha_inicio.fecha if fecha_inicio else "N/A"
        fecha_fin = fecha_fin.fecha if fecha_fin else "N/A"

        flujo = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_ingresos': f"{total_ingresos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            'total_gastos': f"{total_gastos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            'balance': f"{balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        }

        return render(request, 'reportes/flujodecaja.html', {'flujos': [flujo]})
    else:
        flujo = {
            'fecha_inicio': "N/A",
            'fecha_fin': "N/A",
            'total_ingresos': "0,00",
            'total_gastos': "0,00",
            'balance': "0,00",
        }
        return render(request, 'reportes/flujodecaja.html', {'flujos': [flujo]})

@login_required
def ingresos_view(request):
    ingresos = Ingresos.objects.all().order_by('-fecha')
    if request.method == 'POST':
        form = IngresosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reportes:ingresos')
    else:
        form = IngresosForm()

    ingresos_formateados = []
    for ingreso in ingresos:
        try:
            if isinstance(ingreso.monto, Decimal):
                monto_float = float(ingreso.monto)
            elif isinstance(ingreso.monto, str):
                monto_float = float(ingreso.monto.replace(',', '.'))
            else:
                monto_float = float(ingreso.monto)
            
            monto_formateado = f"{monto_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error al formatear el monto: {e}")
            monto_formateado = str(ingreso.monto)
        
        ingresos_formateados.append({
            'id': ingreso.id,
            'fecha': ingreso.fecha,
            'monto': ingreso.monto,
            'monto_formateado': monto_formateado,
            'categoria': ingreso.categoria,
            'descripcion': ingreso.descripcion or ''
        })

    return render(request, 'reportes/ingresos.html', {'ingresos': ingresos_formateados, 'form': form})

@login_required
def editar_ingresos(request, ingreso_id):
    ingreso = get_object_or_404(Ingresos, id=ingreso_id)
    if request.method == 'POST':
        form = IngresosForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            return redirect('reportes:ingresos')
    else:
        form = IngresosForm(instance=ingreso)
    return render(request, 'reportes/editar_ingresos.html', {'form': form, 'ingreso': ingreso})

@login_required
def borrar_ingresos(request, ingreso_id):
    ingreso = get_object_or_404(Ingresos, id=ingreso_id)
    if request.method == 'POST':
        ingreso.delete()
        return redirect('reportes:ingresos')
    return render(request, 'reportes/borrar_ingresos.html', {'ingreso': ingreso})

@login_required
def gastos_view(request):
    gastos = Gastos.objects.all().order_by('-fecha')
    if request.method == 'POST':
        form = GastosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reportes:gastos')
    else:
        form = GastosForm()

    gastos_formateados = []
    for gasto in gastos:
        try:
            if isinstance(gasto.monto, Decimal):
                monto_float = float(gasto.monto)
            elif isinstance(gasto.monto, str):
                monto_float = float(gasto.monto.replace(',', '.'))
            else:
                monto_float = float(gasto.monto)
            
            monto_formateado = f"{monto_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error al formatear el monto: {e}")
            monto_formateado = str(gasto.monto)
        
        gastos_formateados.append({
            'id': gasto.id,
            'fecha': gasto.fecha,
            'monto': gasto.monto,
            'monto_formateado': monto_formateado,
            'categoria': gasto.categoria,
            'descripcion': gasto.descripcion or ''
        })

    return render(request, 'reportes/gastos.html', {'gastos': gastos_formateados, 'form': form})

@login_required
def editar_gastos(request, gasto_id):
    gasto = get_object_or_404(Gastos, id=gasto_id)
    if request.method == 'POST':
        form = GastosForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('reportes:gastos')
    else:
        form = GastosForm(instance=gasto)
    return render(request, 'reportes/editar_gastos.html', {'form': form, 'gasto': gasto})

@login_required
def borrar_gastos(request, gasto_id):
    gasto = get_object_or_404(Gastos, id=gasto_id)
    if request.method == 'POST':
        gasto.delete()
        return redirect('reportes:gastos')
    return render(request, 'reportes/borrar_gastos.html', {'gasto': gasto})