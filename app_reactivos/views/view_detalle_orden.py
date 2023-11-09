from ..models import Detalle_Orden, Orden
from ..serializers import Detalle_OrdenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_detalle(request):
    queryset = Detalle_Orden.objects.all()
    serializer = Detalle_OrdenSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_detalle(request):
    orden_request = request.data.get('orden')
    orden = Orden.objects.get(id=orden_request)
    user_orden = orden.user
    usuario = request.user

    if not request.user.is_staff or user_orden != usuario:
       return Response({'message': 'Acceso denegado. Solo el usuario administrador o el propietario de la orden pueden crear el detalle de la orden.'}, status=403)

    serializer = Detalle_OrdenSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Detalle de orden guardado con éxito.', 'data': serializer.data}, status=201)
    


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def detalle(request, pk):
    try:
        detalle = Detalle_Orden.objects.get(pk=pk)
    except Detalle_Orden.DoesNotExist:
        return Response({'message': 'El detalle no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        orden_request = request.data.get('orden')
        orden = Orden.objects.get(id=orden_request)
        user_orden = orden.user
        usuario = request.user
        if not request.user.is_staff or user_orden != usuario:
            return Response({'message': 'Acceso denegado. Solo el usuario administrador o el propietario de la orden  pueden actualizar el detalle.'}, status=403)

        serializer = Detalle_OrdenSerializer(detalle, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Detalle de la orden actualizado con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff or user_orden != usuario:
            return Response({'message': 'Acceso denegado. Solo el usuario administrador o el propietario pueden eliminar el detalle.'}, status=403)

        detalle.delete()
        return Response({'message': 'Detalle eliminado con éxito.'}, status=204)