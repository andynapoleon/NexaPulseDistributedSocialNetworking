from rest_framework.response import Response
from rest_framework.decorators import api_view
from authors.models import Author
from authors.serializers import AuthorSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

@api_view(['GET'])
def getData(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addAuthor(request):
    serializer = AuthorSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

class Profile(APIView):
    permission_classes = [AllowAny]
    
    def get_user_from_id(self, user_id):
        try:
            user = Author.objects.get(id=user_id)
            return user
        except Author.DoesNotExist:
            return None
    
    def get(self, request, user_id):
        user = self.get_user_from_id(user_id)
        if not user:
            return Response({'error': 'User not found'}, status=404)
        
        full_name = f"{user.firstName} {user.lastName}"
        github = user.github
        email = user.email

        context = {
            'full_name': full_name,
            'github': github,
            'email': email,
        }
        return Response(context)