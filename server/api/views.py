from rest_framework.response import Response
from rest_framework.decorators import api_view
from authors.models import Authors
from authors.serializers import AuthorsSerializer

@api_view(['GET'])
def getData(request):
    authors = Authors.objects.all()
    serializer = AuthorsSerializer(authors, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addAuthor(request):
    serializer = AuthorsSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)





