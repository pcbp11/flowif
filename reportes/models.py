from django.db import models

# Create your models here.
class Ingresos(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=0)
    categoria = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"


    def __str__(self):
        return f"{self.fecha} - {self.descripcion} - {self.monto}"

class Gastos(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=0)
    categoria = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self):
        return f"{self.fecha} - {self.descripcion} - {self.monto}"

class FlujodeCaja(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    class Meta:
        verbose_name = "Flujo de Caja"
        verbose_name_plural = "Flujos de Caja"

    @property
    def total_ingresos(self):
        return Ingresos.objects.filter(fecha__range=(self.fecha_inicio, self.fecha_fin)).aggregate(total=models.Sum('monto'))['total'] or 0

    @property
    def total_gastos(self):
        return Gastos.objects.filter(fecha__range=(self.fecha_inicio, self.fecha_fin)).aggregate(total=models.Sum('monto'))['total'] or 0

    @property
    def balance(self):
        return self.total_ingresos - self.total_gastos

    def __str__(self):
        return f"Flujo de Caja del {self.fecha_inicio} al {self.fecha_fin}"