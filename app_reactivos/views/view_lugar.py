from ..models import Lugar
from ..serializers import LugarSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_lugar(request):
    queryset = Lugar.objects.all()
    serializer = LugarSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_lugar(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de lugar solo puede ser realizada por un administrador.'}, status=403)

    serializer = LugarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Lugar guardado con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def lugar(request, pk):
    try:
        lugar = Lugar.objects.get(pk=pk)
    except Lugar.DoesNotExist:
        return Response({'message': 'El lugar no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar el lugar.'}, status=403)

        serializer = LugarSerializer(
            lugar, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Lugar actualizado con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar el lugar.'}, status=403)

        lugar.delete()
        return Response({'message': 'Lugar eliminado con éxito.'}, status=204)
