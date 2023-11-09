from ..models import Consecutivo
from ..serializers import ConsecutivoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_consecutivo(request):
    queryset = Consecutivo.objects.all()
    serializer = ConsecutivoSerializer(queryset, many=True)
    return Response(serializer.data)