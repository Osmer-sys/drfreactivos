from ..models import Reactivo, Consecutivo, Base
from ..serializers import ReactivoSerializer, ReactivoListarSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from datetime import datetime, date
from django.db.models import F

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_reactivo(request):
    queryset = Reactivo.objects.select_related('numero_cas', 'fabricante', 'estado', 'proveedor', 'unidad_medida').all()
    # Filtrar los reactivos con cantidad mayor a cero
    queryset = queryset.filter(cantidad__gt=0.0)
    serializer = ReactivoListarSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_reactivo(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de reactivo solo puede ser realizada por un administrador.'}, status=403)

    serializer = ReactivoSerializer(data=request.data)
    fecha_recepcion = request.data.get('fecha_recepcion')
    fecha_vencimiento = request.data.get('fecha_vencimiento')
    unidades_recibidas = request.data.get('unidades_recibidas')
    current_year = str(datetime.now().year)[-2:]

    if serializer.is_valid():
         # Obtener el último registro de la tabla 'Consecutivo' y actualizar 'consecutivo'
        try:
            ultimo_consecutivo = Consecutivo.objects.latest('id')
            consecutivo = ultimo_consecutivo.numero
            consecutivo_year = ultimo_consecutivo.año
        except Consecutivo.DoesNotExist:
            consecutivo = 0
            consecutivo_year = current_year

        try:
            validar_fecha_recepcion(fecha_recepcion)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

        try:    
            validar_fecha_vencimiento(fecha_vencimiento)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

        if unidades_recibidas <= 0:
            return Response({'message': 'El valor de unidades recibidas debe ser un número positivo mayor a cero.'}, status=400)

        consecutivo += 1
        i = 1
        while i <= unidades_recibidas: 
            
            if consecutivo_year != current_year:
                consecutivo = 0
            
            consecutivo_str = str(consecutivo).zfill(4)
            consecutivo_ingreso = f'R{consecutivo_str}-{current_year} {i}/{unidades_recibidas}'
            # Agregar 'consecutivo_ingreso' a los datos del request
            request.data['consecutivo_ingreso'] = consecutivo_ingreso  
            serializer = ReactivoSerializer(data=request.data)
            if serializer.is_valid():   
                serializer.save()                       
                Consecutivo.objects.create(numero=consecutivo, reactivo=Reactivo.objects.latest('id'), año = current_year)
                
            i += 1        
        return Response({'message': 'Reactivo(s) guardado(s) con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)

    
@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def reactivo(request, pk):
    try:
        reactivo = Reactivo.objects.get(pk=pk)
    except Reactivo.DoesNotExist:
        return Response({'message': 'El reactivo no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar el reactivo.'}, status=403)

        serializer = ReactivoSerializer(
            reactivo, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
                fecha_recepcion = request.data.get('fecha_recepcion')
                date_fecha_recepcion = datetime.strptime(fecha_recepcion, "%Y-%m-%d").date()
                fecha_vencimiento = request.data.get('fecha_vencimiento')
                date_fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()   

                try:
                    validar_fecha_recepcion(date_fecha_recepcion)
                except Exception as e:
                    return Response({'message': str(e)}, status=400)

                try:    
                    validar_fecha_vencimiento(date_fecha_vencimiento)
                except Exception as e:
                    return Response({'message': str(e)}, status=400)

                serializer.save()
                return Response({'message': 'Reactivo actualizado con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar el reactivo.'}, status=403)

        reactivo.delete()
        return Response({'message': 'Reactivo eliminado con éxito.'}, status=204)

def validar_fecha_recepcion(fecha_recepcion):
    date_fecha_recepcion = datetime.strptime(fecha_recepcion, "%Y-%m-%d").date()

    if date_fecha_recepcion > datetime.now().date():
        raise Exception('La fecha de recepcion no puede ser mayor a la fecha actual.')


def validar_fecha_vencimiento(fecha_vencimiento):
    date_fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()
    
    if date_fecha_vencimiento < datetime.now().date():
         raise Exception('El reactivo esta vencido.')