from ..models import Orden
from ..serializers import OrdenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_orden(request):
    queryset = Orden.objects.all()
    serializer = OrdenSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_orden(request):
    serializer = OrdenSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message': 'Orden guardada con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def orden(request, pk):
    try:
        orden = Orden.objects.get(pk=pk)
    except Orden.DoesNotExist:
        return Response({'message': 'El orden no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff and request.user != orden.user:
            return Response({'message': 'Acceso denegado. Solo el usuario administrador o el propietario de la orden pueden actualizar la orden.'}, status=403)

        data = {}
        if 'observacion' in request.data:
            data['observacion'] = request.data['observacion']
        else:
            return Response({'message': 'No se puede modificar este campo, solo puede modificar el campo observacion.'})
        serializer = OrdenSerializer(orden, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Observacion actualizada con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff and request.user != orden.user:
            return Response({'message': 'Acceso denegado. Solo el usuario administrador o el propietario del orden pueden eliminar el orden.'}, status=403)

        orden.delete()
        return Response({'message': 'Orden eliminado con éxito.'}, status=204)