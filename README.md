Proyecto Flowif - Gestión Financiera - Pía Barraza
Este proyecto es una aplicación web de gestión financiera que permite registrar, visualizar y administrar los ingresos, gastos y el flujo de caja de una empresa o negocio. Fue desarrollado con Django y ofrece una interfaz sencilla para ingresar datos y visualizar reportes de manera organizada.

Funcionalidades principales
1. Registro de Ingresos
Los usuarios pueden registrar los ingresos diarios de la empresa, añadiendo detalles como:

Fecha
Monto
Categoría
Descripción (opcional)
Los ingresos registrados se muestran en una tabla con formato adecuado de miles para una visualización más clara de los montos.

2. Registro de Gastos
De igual manera, los usuarios pueden registrar los gastos de la empresa, añadiendo los siguientes detalles:

Fecha
Monto
Categoría
Descripción (opcional)
Los gastos también se muestran en una tabla con el formato adecuado de miles, facilitando su interpretación.

3. Visualización del Flujo de Caja
El sistema ofrece una visualización clara del flujo de caja, que incluye:

Fecha de inicio y fin del período.
Total de ingresos registrados.
Total de gastos registrados.
Balance general.
El balance se calcula restando el total de gastos al total de ingresos, y toda esta información se presenta en una tabla.

4. Formato personalizado de montos
Tanto los ingresos como los gastos están formateados con separadores de miles, utilizando un formato que reemplaza las comas por puntos para una presentación más amigable, especialmente en regiones que usan este formato.

Estructura del Proyecto
Modelos
Ingresos: Define los atributos principales de un ingreso: fecha, monto, categoría y descripción.
Gastos: Define los atributos principales de un gasto: fecha, monto, categoría y descripción.
Flujo de Caja: Calcula automáticamente el total de ingresos, total de gastos y el balance para un rango de fechas específico.
Vistas (Views)
Ingreso de Ingresos y Gastos: Los formularios permiten al usuario añadir ingresos y gastos con sus respectivos detalles. La información se valida antes de ser guardada en la base de datos.
Visualización del Flujo de Caja: Muestra el resumen del flujo de caja para el período completo de datos ingresados, incluyendo las fechas de inicio y fin de los registros.
Plantillas (Templates)
Base HTML: Una estructura común para todas las páginas con una barra de navegación que permite al usuario navegar entre las vistas de ingresos, gastos y flujo de caja.
Ingreso y Gastos: Formulario de registro y tabla para mostrar los datos ingresados.
Flujo de Caja: Tabla resumen que muestra el flujo de caja calculado.
Tecnologías Utilizadas
Python 3.x
Django 5.x
HTML y CSS para el diseño de las plantillas
SQLite como base de datos por defecto para el almacenamiento de los ingresos, gastos y flujo de caja.
Instalación y Configuración
Requisitos previos
Tener Python 3.x instalado en el sistema.
Tener pip para instalar las dependencias necesarias.
Pasos para instalar y ejecutar el proyecto
1.Clona el repositorio:
git clone https://github.com/pcbp11/flowif.git
cd flowif
2.Crea un entorno virtual y actívalo:
python -m venv .venv
.venv\Scripts\activate
3. Realiza las migraciones para crear la base de datos:
python manage.py migrate
4. Ejecuta el servidor local:
python manage.py runserver
5. Accede a la aplicación en tu navegador:
http://127.0.0.1:8000/

Próximas Mejoras
Filtros avanzados para visualizar el flujo de caja en rangos de fechas seleccionados por el usuario.
Implementación de gráficos para mostrar los ingresos y gastos en formato visual.

Contribuciones
Cualquier sugerencia o mejora al código es bienvenida. Puedes crear un pull request o abrir un issue en el repositorio.
