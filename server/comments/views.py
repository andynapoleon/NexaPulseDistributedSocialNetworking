from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Comment
from .serializers import CommentSerializer, CommentSerializerPost

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializerPost
        return CommentSerializer

class CommentDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    queryset = Comment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializerPost
        return CommentSerializer

    def get(self, request, author_id, post_id):
        try:
            comment = Comment.objects.filter(post_id=post_id) # get the comments of the post given post_id
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        base_url = request.build_absolute_uri('/')
        serializer = self.get_serializer(comment, many=True, context={'base_url': base_url})
        if (serializer.is_valid):
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, author_id, post_id):
        serializer = self.get_serializer(data=request.data)
        
        # Validate the serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



