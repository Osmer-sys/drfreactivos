from ..models import Cantidad
from ..serializers import CantidadSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_cantidad(request):
    queryset = Cantidad.objects.all()
    serializer = CantidadSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_cantidad(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de cantidad solo puede ser realizada por un administrador.'}, status=403)

    serializer = CantidadSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Cantidad guardada con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def cantidad(request, pk):
    try:
        cantidad = Cantidad.objects.get(pk=pk)
    except Cantidad.DoesNotExist:
        return Response({'message': 'La cantidad no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar la cantidad.'}, status=403)

        serializer = CantidadSerializer(
            cantidad, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cantidad actualizada con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar la cantidad.'}, status=403)

        cantidad.delete()
        return Response({'message': 'Cantidad eliminada con éxito.'}, status=204)





