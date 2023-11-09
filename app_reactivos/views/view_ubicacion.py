from ..models import Ubicacion
from ..serializers import UbicacionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_ubicacion(request):
    queryset = Ubicacion.objects.all()
    serializer = UbicacionSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_ubicacion(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de ubicacion solo puede ser realizada por un administrador.'}, status=403)

    serializer = UbicacionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Ubicacion guardada con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def ubicacion(request, pk):
    try:
        ubicacion = Ubicacion.objects.get(pk=pk)
    except Ubicacion.DoesNotExist:
        return Response({'message': 'La ubicacion no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los administradores pueden actualizar la ubicacion.'}, status=403)

        serializer = UbicacionSerializer(
            ubicacion, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ubicacion actualizada con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los administradores pueden eliminar la ubicacion.'}, status=403)

        ubicacion.delete()
        return Response({'message': 'Ubicacion eliminada con éxito.'}, status=204)
