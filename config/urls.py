from django.contrib import admin
from django.urls import path
from reportes import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'reportes'

urlpatterns = [
    path('admin/', admin.site.urls),  # Administración de Django
    path('', views.index, name='index'),  # Página principal
    path('flujodecaja/', views.flujodecaja_view, name='flujodecaja'),  # Página de Flujo de Caja
    path('ingresos/', views.ingresos_view, name='ingresos'),  # Página de Ingresos
    path('gastos/', views.gastos_view, name='gastos'),  # Página de Gastos
    
    # Login, Logout y Registro
    path('login/', LoginView.as_view(template_name='reportes/login.html'), name='login'),
]
