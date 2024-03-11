from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CommentLikes, PostLikes
from .serializers import LikesSerializerComment, LikesSerializerPost

class PostLikeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = PostLikes.objects.all()
    serializer_class = LikesSerializerPost
    lookup_field = 'post_id'

    @action(detail=True, methods=['get'])
    def post_likes(self, request, author_id, post_id):
        # Query to retrieve likes on the specified post excluding the likes made by the post author
        likes = PostLikes.objects.filter(post_id=post_id).exclude(author_id=author_id)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'])
    def like_post(self, request, author_id=None, post_id=None):
        serializer = self.get_serializer(data=request.data)
        
        # Check if the author_id provided in the URL matches the ID of the currently logged-in user
        if request.data.get('author') != author_id:
            return Response({"error": "You are not authorized to like posts on behalf of other users."}, status=status.HTTP_403_FORBIDDEN)

        try:
            like = PostLikes.objects.create(author_id=author_id, post_id=post_id)
            base_url = request.build_absolute_uri('/')
            serializer = self.get_serializer(like, context={'base_url': base_url})
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    
        
class CommentLikeViewSet(viewsets.ModelViewSet):
    permission_class=[AllowAny]

    queryset = CommentLikes.objects.all()
    serializer_class = LikesSerializerComment
    lookup_field = 'comment_id'

    @action(detail=True, methods=['get'])
    def comment_likes(self, request, author_id=None, post_id=None, comment_id=None):
        # Check if the comment is from post of post_id
        try:
            comment = CommentLikes.objects.get(id=comment_id)
        except CommentLikes.DoesNotExist:
            return Response(status=404)
        
        if comment.post_id != post_id:
            return Response(status=404)
        
        # Query to retrieve likes on the specified comment excluding the likes made by the author who posted
        likes = CommentLikes.objects.filter(post_id=post_id, comment_id=comment_id).exclude(author_id=author_id)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data, status=200)
        


