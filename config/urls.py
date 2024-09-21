from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from reportes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(([
        path('', views.index, name='index'),
        path('flujodecaja/', views.flujodecaja_view, name='flujodecaja'),
        path('ingresos/', views.ingresos_view, name='ingresos'),
        path('gastos/', views.gastos_view, name='gastos'),
        path('ingresos/editar/<int:ingreso_id>/', views.editar_ingresos, name='editar_ingresos'),
        path('ingresos/borrar/<int:ingreso_id>/', views.borrar_ingresos, name='borrar_ingresos'),
        path('gastos/editar/<int:gasto_id>/', views.editar_gastos, name='editar_gastos'),
        path('gastos/borrar/<int:gasto_id>/', views.borrar_gastos, name='borrar_gastos'),
        path('about/', views.about, name='about'),  # Añadida la URL 'about' dentro del namespace 'reportes'
    ], 'reportes'))),
    path('login/', LoginView.as_view(template_name='reportes/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.register_view, name='registro'),
]