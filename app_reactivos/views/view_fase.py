from ..models import Fase
from ..serializers import FaseSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_fase(request):
    queryset = Fase.objects.all()
    serializer = FaseSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_fase(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de fase solo puede ser realizada por un administrador.'}, status=403)

    serializer = FaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Fase guardada con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def fase(request, pk):
    try:
        fase = Fase.objects.get(pk=pk)
    except Fase.DoesNotExist:
        return Response({'message': 'La fase no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar la fase.'}, status=403)

        serializer = FaseSerializer(
            fase, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Fase actualizada con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar la fase.'}, status=403)

        fase.delete()
        return Response({'message': 'Fase eliminada con éxito.'}, status=204)