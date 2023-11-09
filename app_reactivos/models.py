from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Fabricante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return '{0}'.format(self.nombre)


class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return '{0}'.format(self.nombre)


class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return '{0}'.format(self.nombre)

class Lugar(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return '{0}'.format(self.nombre)

class Ubicacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)

    def __str__(self):
        return '{0},{1}'.format(self.nombre, self.lugar)

class Fase(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return '{0}'.format(self.nombre)

class Codigo(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20)

    def __str__(self):
        return '{0}'.format(self.codigo)

class Cantidad(models.Model):
    numero = models.IntegerField(primary_key=True)

    def __str__(self):
        return '{0}'.format(self.numero)

class Base(models.Model):
    numero_cas = models.CharField(primary_key=True)
    nombre = models.CharField(max_length=30)
    controlado = models.BooleanField() 
    codigo_reactivo = models.ForeignKey(Codigo, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE) 
    codigo_sap = models.CharField(blank=True, max_length=20, null=True)

    def __str__(self):
        return '{0}'.format(self.numero_cas)

class Unidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return '{0}'.format(self.nombre)

#La vigencia es un valor autocalculado
 
class Reactivo(models.Model): 
    id = models.AutoField(primary_key=True) 
    consecutivo_ingreso = models.CharField(max_length=50, blank=True, null=True)
    vigencia = models.CharField(max_length=20)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    numero_cas = models.ForeignKey(Base, on_delete=models.CASCADE)
    lote_proveedor = models.CharField(max_length=20)
    concentracion = models.CharField(max_length=10)
    cantidad = models.FloatField()
    unidad_medida = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    unidades_recibidas = models.ForeignKey(Cantidad, on_delete=models.CASCADE)
    fecha_recepcion = models.DateField()
    fecha_vencimiento = models.DateField()
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)


    @property
    def vigencia(self):
        # Cálculo de la vigencia
        if self.fecha_vencimiento < timezone.now().date():
            return "Vencido"
        else:
            return "Vigente"

    @vigencia.setter
    def vigencia(self, value):
        # Este método impide la modificación directa de la propiedad vigencia
        # lanzando una excepción si se intenta modificar su valor
        raise AttributeError(
            "No se puede modificar la propiedad 'vigencia'. Es de solo lectura.")

    def __str__(self):
        return '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}'.format( self.consecutivo_ingreso, self.vigencia, self.estado, self.fabricante, self.proveedor,self.numero_cas, self.lote_proveedor, self.concentracion,  self.cantidad, self.unidad_medida, self.unidades_recibidas, self.fecha_recepcion, self.fecha_vencimiento, self.fecha_inicio, self.fecha_finalizacion, self.fecha_registro)

class Consecutivo(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    reactivo = models.ForeignKey(Reactivo, on_delete=models.CASCADE)
    año = models.CharField(max_length=4)

    def __str__(self):
        return '{0},{1},{2}'.format(self.numero, self.reactivo, self.año)

class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    observacion = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0},{1},{2}'.format(self.observacion, self.fecha_creacion, self.user)


class Detalle_Orden(models.Model):
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    reactivo = models.ForeignKey(Reactivo, on_delete=models.CASCADE)

    def __str__(self):
        return '{0},{1},{2}'.format(self.id, self.orden, self.reactivo)

class Consumo(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.FloatField()
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    reactivo = models.ForeignKey(Reactivo, on_delete=models.CASCADE)
    fecha_consumo = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{0},{1},{2},{3},{4}'.format(self.cantidad, self.unidad, self.usuario, self.reactivo, self.fecha_consumo)