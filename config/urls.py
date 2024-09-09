from django.contrib import admin
from django.urls import path
from reportes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Página principal
    path('flujodecaja/', views.flujodecaja_view, name='flujodecaja'),  # Página de Flujo de Caja
    path('ingresos/', views.ingresos_view, name='ingresos'),  # Página de Ingresos
    path('gastos/', views.gastos_view, name='gastos'),  # Página de Gastos
]
