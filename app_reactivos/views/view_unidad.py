from ..models import Unidad
from ..serializers import UnidadSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_unidad(request):
    queryset = Unidad.objects.all()
    serializer = UnidadSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_unidad(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de unidad solo puede ser realizada por un administrador.'}, status=403)

    serializer = UnidadSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Unidad guardada con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def unidad(request, pk):
    try:
        unidad = Unidad.objects.get(pk=pk)
    except Unidad.DoesNotExist:
        return Response({'message': 'La unidad no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar la unidad.'}, status=403)

        serializer = UnidadSerializer(
            unidad, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Unidad actualizada con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar la unidad.'}, status=403)

        unidad.delete()
        return Response({'message': 'Unidad eliminada con éxito.'}, status=204)
