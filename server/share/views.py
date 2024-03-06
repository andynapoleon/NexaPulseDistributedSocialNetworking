from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import SharedPost


class SharePostAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "hi there!"}, status=200)

    def post(self, request):
        post_id = request.data.get("post_id")
        try:
            # Implement logic to share the post
            # For example:
            shared_post = SharedPost.objects.create(
                author=request.user, post_id=post_id
            )
            return Response({"message": "Post shared successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
