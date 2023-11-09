from ..models import Codigo
from ..serializers import CodigoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_codigo(request):
    queryset = Codigo.objects.all()
    serializer = CodigoSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_codigo(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de codigo solo puede ser realizada por un administrador.'}, status=403)

    serializer = CodigoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Codigo guardado con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def codigo(request, pk):
    try:
        codigo = Codigo.objects.get(pk=pk)
    except Codigo.DoesNotExist:
        return Response({'message': 'El codigo no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar el codigo.'}, status=403)

        serializer = CodigoSerializer(
            codigo, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Codigo actualizado con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar el codigo.'}, status=403)

        codigo.delete()
        return Response({'message': 'Codigo eliminado con éxito.'}, status=204)





