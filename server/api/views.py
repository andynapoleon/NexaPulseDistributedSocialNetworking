from rest_framework.response import Response
from rest_framework.decorators import api_view
from authors.models import Author
from authors.serializers import AuthorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView, status
from rest_framework_simplejwt.tokens import AccessToken


@api_view(["GET"])
def getData(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addAuthor(request):
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
