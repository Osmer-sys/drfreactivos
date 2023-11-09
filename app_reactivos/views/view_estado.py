from ..models import Estado
from ..serializers import EstadoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_estado(request):
    queryset = Estado.objects.all()
    serializer = EstadoSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_estado(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de estado solo puede ser realizada por un administrador.'}, status=403)

    serializer = EstadoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Estado guardado con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def estado(request, pk):
    try:
        estado = Estado.objects.get(pk=pk)
    except Estado.DoesNotExist:
        return Response({'message': 'El estado no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar el estado.'}, status=403)

        serializer = EstadoSerializer(
            estado, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Estado actualizado con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar el estado.'}, status=403)

        estado.delete()
        return Response({'message': 'Estado eliminado con éxito.'}, status=204)