from ..models import Fabricante
from ..serializers import FabricanteSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_fabricante(request):
    queryset = Fabricante.objects.all()
    serializer = FabricanteSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_fabricante(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de fabricante solo puede ser realizada por un administrador.'}, status=403)

    serializer = FabricanteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Fabricante guardado con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def fabricante(request, pk):
    try:
        fabricante = Fabricante.objects.get(pk=pk)
    except Fabricante.DoesNotExist:
        return Response({'message': 'El fabricante no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar el fabricante.'}, status=403)

        serializer = FabricanteSerializer(
            fabricante, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Fabricante actualizado con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar el fabricante.'}, status=403)

        fabricante.delete()
        return Response({'message': 'Fabricante eliminado con éxito.'}, status=204)
