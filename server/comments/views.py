from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Comment
from .serializers import CommentSerializer, AuthorRefSerializer

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, author_id, post_id):
        comments = self.get_queryset().filter(post_id=post_id)

        page = self.paginate_queryset(comments)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
        


# @api_view(['GET'])
# def get_comment(request, comment_id):
#     try:
#         comment = Comment.objects.get(id=comment_id)
#     except Comment.DoesNotExist:
#         return Response({"error": "Comment not found"}, status=404)

#     serializer = CommentSerializer(comment)
#     author_serializer = AuthorRefSerializer(comment.author)
#     data = {
#         "type": "comment",
#         "author": author_serializer.data
#         **serializer.data
#     }
#     return Response(data)

# @api_view(['POST'])
# def create_comment(request, post_id):
#     request.data['post_id'] = post_id
#     serializer = CommentSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)


