from rest_framework import serializers
from .models import Fabricante, Proveedor, Estado, Ubicacion, Unidad, Reactivo, Orden, Detalle_Orden, Base, Lugar, Fase, Codigo, Cantidad, Consecutivo, Consumo
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_superuser', 'email',
                  'is_staff', 'is_active', 'date_joined', 'last_login')


class FabricanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricante
        fields = ('id', 'nombre')


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ('id', 'nombre')


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ('id', 'nombre')

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = ('id', 'nombre')

class UbicacionSerializer(serializers.ModelSerializer):
    lugar = serializers.CharField(source='lugar.nombre', read_only=True)
    class Meta:
        model = Ubicacion
        fields = ('id', 'nombre','lugar')

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ('id', 'nombre')

class FaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fase
        fields = ('id', 'nombre')

class CodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigo
        fields = ('id', 'codigo')

class BaseListarSerializer(serializers.ModelSerializer):
    estado = serializers.CharField(source='estado.nombre', read_only=True)
    ubicacion = serializers.CharField(source='ubicacion.nombre', read_only=True)
    lugar = serializers.CharField(source='ubicacion.lugar', read_only=True)
    codigo_reactivo = serializers.CharField(source='codigo_reactivo.codigo', read_only=True)
    fase = serializers.CharField(source='fase.nombre', read_only=True)

    class Meta:
        model = Base
        fields = ('numero_cas', 'nombre', 'controlado', 'codigo_reactivo','fase', 'lugar','ubicacion','estado', 'codigo_sap')

class BaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Base
        fields = ('numero_cas', 'nombre', 'controlado', 'codigo_reactivo','fase', 'ubicacion','codigo_sap')

class CantidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cantidad
        fields = ('numero',)

class ReactivoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Reactivo
        fields = ('id','consecutivo_ingreso','vigencia', 'numero_cas', 'estado','cantidad', 'unidad_medida', 'lote_proveedor', 'concentracion', 'unidades_recibidas', 'fecha_recepcion','fecha_vencimiento', 'fecha_inicio','fecha_finalizacion', 'fabricante', 'proveedor', 'fecha_registro')


class ReactivoListarSerializer(serializers.ModelSerializer):
    numero_cas = BaseSerializer()
    fabricante = serializers.CharField(source='fabricante.nombre', read_only=True)
    estado = serializers.CharField(source='estado.nombre', read_only=True)
    proveedor = serializers.CharField(source='proveedor.nombre', read_only=True)
    unidad_medida = serializers.CharField(source='unidad_medida.nombre', read_only=True)
    class Meta:
        model = Reactivo
        fields = ('id','consecutivo_ingreso', 'vigencia', 'estado', 'fabricante', 'proveedor', 'numero_cas', 'lote_proveedor', 'concentracion', 'cantidad', 'unidad_medida', 'unidades_recibidas', 'fecha_recepcion', 'fecha_vencimiento', 'fecha_inicio', 'fecha_finalizacion')


class ConsecutivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consecutivo
        fields = ('id', 'numero', 'reactivo', 'año')

class OrdenSerializer(serializers.ModelSerializer):
    usuario_orden = serializers.CharField(
        source='user.first_name', read_only=True)

    class Meta:
        model = Orden
        fields = ('id', 'fecha_creacion', 'observacion', 'usuario_orden')


class Detalle_OrdenSerializer(serializers.ModelSerializer):
    orden = OrdenSerializer()
    reactivo = ReactivoListarSerializer()

    class Meta:
        model = Detalle_Orden
        fields = ('id', 'orden', 'reactivo')

class ConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = ('cantidad', 'unidad', 'usuario', 'reactivo','fecha_consumo')
