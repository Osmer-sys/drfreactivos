from ..models import Consumo, Reactivo, Unidad
from ..serializers import ConsumoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_consumo(request):
    queryset = Consumo.objects.all()
    serializer = ConsumoSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_consumo(request):
    serializer = ConsumoSerializer(data=request.data)
    reactivo_id = request.data.get('reactivo')
    cantidad_consumo = request.data.get('cantidad')
    unidad_consumo = request.data.get('unidad')
    reactivo = Reactivo.objects.get(id=reactivo_id)
    unidad = Unidad.objects.get(nombre=reactivo.unidad_medida)
    unidad_enviada = Unidad.objects.get(id=unidad_consumo)
    if unidad.id == unidad_consumo:
        if reactivo.cantidad >= cantidad_consumo:
            reactivo.cantidad -= cantidad_consumo
            if serializer.is_valid(): 
                reactivo.save()
                serializer.save(usuario=request.user)
                return Response({'message': 'Consumo guardado con éxito.', 'data': serializer.data}, status=201)
            return Response(serializer.errors, status=400)
        else:
            return Response({'message': f'La cantidad actual ({reactivo.cantidad} {reactivo.unidad_medida}) es menor que el consumo a registrar.'}, status=400)
    else:
        return Response({'message': f'La unidad del reactivo ({unidad.nombre}) y del consumo ({unidad_enviada.nombre}) no coinciden.'}, status=400)






@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def consumo(request, pk):
    try:
        consumo = Consumo.objects.get(pk=pk)
    except Consumo.DoesNotExist:
        return Response({'message': 'El consumo no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff and request.user != consumo.user:
            return Response({'message': 'Acceso denegado. Solo el usuario administrador o el propietario del consumo pueden actualizar el consumo.'}, status=403)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo el usuario administrador puede eliminar el consumo.'}, status=403)

        consumo.delete()
        return Response({'message': 'Consumo eliminado con éxito.'}, status=204)