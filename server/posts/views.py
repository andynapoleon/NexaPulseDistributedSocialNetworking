from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post
from .serializers import PostSerializer
from follow.models import Follows
from asgiref.sync import sync_to_async


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-published")
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        is_image_post = False

        if "content" in data and data["content"].startswith("data:image"):
            is_image_post = True

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            regular_post = serializer.save()

            if is_image_post:
                image_data = {
                    "type": "image",
                    "visibility": data.get("visibility", "PUBLIC"),
                    "authorId": data["authorId"],
                    "title": data.get("title", "Image Post"),
                    "published": data["published"],
                    "content_type": data["content_type"],
                    "content": data["content"],
                    "post": regular_post.id,
                }
                image_serializer = self.get_serializer(data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePost(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get(self, request, author_id):
        try:
            # Filter posts by author ID
            posts = Post.objects.filter(
                authorId=author_id, visibility__in=["PUBLIC", "FRIENDS"]
            ).order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(posts, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)
        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)


class ProfilePostForStranger(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get(self, request, author_id):
        try:
            # Filter posts by author ID
            posts = Post.objects.filter(
                authorId=author_id, visibility="PUBLIC"
            ).order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(posts, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)
        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)


class ProfilePostForHimself(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get(self, request, author_id):
        try:
            # Filter posts by author ID
            posts = Post.objects.filter(authorId=author_id).order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(posts, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)
        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)


class PostDetail(APIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return PostSerializer

    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
            print("POST ID: ", post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, post_id):
        try:
            if request.data["image"] != None:
                id, response = self.put_image(
                    request, author_id, post_id, request.data["image"]
                )
                # print("HEADER ID:", id)
                if response:

                    # Remove the 'image' key from request.data
                    request_data = request.data.copy()
                    request_data["image_ref"] = id
                    request_data.pop("image", None)
                    request_data["authorId"] = int(author_id)

            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post, data=request_data, partial=True)
            if serializer.is_valid():
                if request.user.id == int(author_id):
                    serializer.save()
                    return Response(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put_image(self, request, author_id, post_id, image_blob):
        try:
            post = Post.objects.get(id=post_id)
            request_data = request.data.copy()

            request_data["content"] = image_blob
            request_data["content_type"] = "image"
            request_data["image"] = None
            # Ensure that authorId is passed as an integer
            request_data["authorId"] = int(author_id)

            serializer = PostSerializer(post, data=request_data, partial=True)

            if serializer.is_valid():
                if request.user.id == int(author_id):
                    serializer.save()
                    saved_data = serializer.data
                    saved_id = saved_data.get('id', None)
                    
                    return saved_id, True
            print(serializer.errors)
            return None, False
        except Post.DoesNotExist:
            return None, False

    def delete(self, request, author_id, post_id):
        # Retrieve the regular post object
        try:
            regular_post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.id == int(author_id):
            # Delete the regular post
            regular_post.delete()

            # Also delete the corresponding image post, if exists
            try:
                image_post = Post.objects.get(id=post_id, type="image")
                image_post.delete()
            except Post.DoesNotExist:
                pass  # Image post does not exist

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_403_FORBIDDEN)


class ImagePostDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id, authorId=author_id, type="image")
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, post_id, image_blob):
        try:
            post = Post(content=image_blob, authorID=author_id)
        except:
            pass


class AuthorPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        posts = Post.objects.filter(authorId=author_id).order_by("-published")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, author_id):
        serializer = PostSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicPosts(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Filter posts by authorId and visibility='PUBLIC'
        posts = Post.objects.filter(visibility="PUBLIC").order_by("-published")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class FollowingPosts(APIView):
    def get(self, request):
        try:
            user_id = request.user.id

            # Get posts authored by users the current user follows
            followed_users_ids = Follows.objects.filter(
                follower_id=user_id, acceptedRequest=True
            ).values_list("followed_id", flat=True)

            # Include the current user's ID in the list of followed users
            followed_users_ids = list(followed_users_ids)
            followed_users_ids.append(user_id)

            queryset = Post.objects.filter(
                visibility="PUBLIC", authorId__in=followed_users_ids
            ).order_by("-published")

            # Order by published date
            queryset = queryset.order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(queryset, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)

        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)
