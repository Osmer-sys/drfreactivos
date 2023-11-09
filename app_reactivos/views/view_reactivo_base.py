from ..models import Base
from ..serializers import BaseSerializer,BaseListarSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
import re


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_base(request):
    queryset = Base.objects.select_related('codigo_reactivo').all()
    serializer = BaseListarSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_base(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de información básica de reactivos solo puede ser realizada por un administrador.'}, status=403)

    serializer = BaseSerializer(data=request.data)
    if serializer.is_valid():
        numero_cas = request.data.get('numero_cas')
        if not validar_numero_cas(numero_cas):
            return Response({'message': 'El formato del número CAS es incorrecto.'}, status=400)
        
        serializer.save()
        return Response({'message': 'Información básica de reactivos guardada con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


def validar_numero_cas(numero_cas):
    # Patrón para validar el número CAS (ejemplo: 12345-67-8)
    patron = r'^\d{2,7}-\d{2}-\d{1}$'
    return re.match(patron, numero_cas) is not None


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def base(request, pk):
    try:
        base = Base.objects.get(pk=pk)
    except Base.DoesNotExist:
        return Response({'message': 'La información básica del reactivo no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar la información básica de reactivos.'}, status=403)

        serializer = BaseSerializer(
            base, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Información básica de reactivos actualizada con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar la información básica de reactivos.'}, status=403)

        base.delete()
        return Response({'message': 'Información básica de reactivos eliminada con éxito.'}, status=204)
