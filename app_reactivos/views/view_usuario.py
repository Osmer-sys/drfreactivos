from django.contrib.auth.models import User
from ..serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_usuario(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser | IsAuthenticated])
def crear_usuario(request):
    if not request.user.is_staff:
        return Response({'message': 'La creación de usuario solo puede ser realizada por un administrador.'}, status=403)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Usuario guardado con éxito.', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def usuario(request, pk):
    try:
        usuario = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'message': 'El usuario no existe.'}, status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden actualizar el usuario.'}, status=403)

        serializer = UserSerializer(
            usuario, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario actualizado con éxito.', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'message': 'Acceso denegado. Solo los usuarios administradores pueden eliminar el usuario.'}, status=403)

        usuario.delete()
        return Response({'message': 'Usuario eliminado con éxito.'}, status=204)
