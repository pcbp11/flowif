from django.contrib import admin
from django.urls import path
from reportes import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Administración de Django
    path('', views.index, name='index'),  # Página principal
    path('flujodecaja/', views.flujodecaja_view, name='flujodecaja'),  # Página de Flujo de Caja
    path('ingresos/', views.ingresos_view, name='ingresos'),  # Página de Ingresos
    path('gastos/', views.gastos_view, name='gastos'),  # Página de Gastos
    
    # Login, Logout y Registro
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Página de login
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Página de logout
    path('register/', views.register_view, name='register'),  # Página de registro de usuarios
]
