from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, permission_classes
from .models import Node
from .serializers import NodeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class NodeList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        response = {
            "type": "nodes",
            "items": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)



