from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Post
from .serializers import PostSerializer, ServerPostSerializer
from follow.models import Follows
from asgiref.sync import sync_to_async
from django.utils import timezone
from django.db.models import Q
import uuid
from authors.models import Author
from authors.serializers import AuthorSerializer
from markdownx.utils import markdownify



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-published")
    serializer_class = PostSerializer


class ProfilePost(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        try:
            # Filter posts by author ID
            queryset = Post.objects.filter(
                authorId=author_id, visibility__in=["PUBLIC", "FRIENDS"]
            )
            queryset = queryset.exclude(contentType__startswith="image/")

            # Order by published date
            queryset = queryset.order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(queryset, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)
        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)


class ProfilePostForStranger(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        try:
            # Validate author_id as UUID
            uuid.UUID(author_id)
            print(author_id, type(author_id))
            # Filter posts by author ID
            queryset = Post.objects.filter(authorId=author_id, visibility="PUBLIC")
            queryset = queryset.exclude(contentType__startswith="image/")

            # Order by published date
            queryset = queryset.order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(queryset, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)
        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)


class ProfilePostForHimself(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        try:
            # Filter posts by author ID
            queryset = Post.objects.filter(authorId=author_id)
            queryset = queryset.exclude(contentType__startswith="image/")

            # Order by published date
            queryset = queryset.order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(queryset, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)
        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)


class PostById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
            print(post.visibility)
            if post.visibility != "FRIENDS":
                serializer = PostSerializer(post)
                return Response(serializer.data)
            else:
                followed_users_ids = Follows.objects.filter(
                    follower_id=author_id, acceptedRequest=True
                ).values_list("followed_id", flat=True)
                followed_users_ids = list(followed_users_ids)
                followed_users_ids = [str(value) for value in followed_users_ids]
                followed_users_ids.append(author_id)
                if str(post.authorId.id) in followed_users_ids:
                    serializer = PostSerializer(post)
                    return Response(serializer.data)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PostDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return PostSerializer

    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
            base_url = request.build_absolute_uri("/")
            serializer = PostSerializer(post, context={"base_url": base_url})
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)

            request_data = request.data.copy()
            request_data["authorId"] = author_id
            print("Current request_data image:", request_data["image"])
            if request_data["image"]:
                # Delete old image post
                if post.image_ref:
                    image_blob = request.data["image"]
                    image_info = image_blob.split(",")
                    post.image_ref.content = image_info[1]
                    post.image_ref.contentType = image_info[0][5:]
                    post.image_ref.save()
                else:
                    print("I AM CREATING A NEW POST | Current post_id:", post_id)
                    print("Before making | Current image_ref?:", post.image_ref)
                    # Create a new one
                    id, response = self.create_image_post(
                        request, author_id, post_id, request.data["image"]
                    )
                    if response:
                        request_data["image_ref"] = id
                        print("After making | Current image_ref:", id)

            # serializer accepts CommonMark content
            request_data['content'] = markdownify(request_data['content'])

            serializer = PostSerializer(post, data=request_data, partial=True)
            if serializer.is_valid():
                if str(request.user.id) == author_id:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            # print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create_image_post(self, request, author_id, post_id, image_blob):
        try:
            request_data = request.data.copy()
            image_info = image_blob.split(",")

            request_data["content"] = image_info[1]
            request_data["contentType"] = image_info[0][5:]
            request_data["image"] = None
            # Ensure that authorId is passed as an integer
            request_data["authorId"] = author_id
            # print("New Data created:")
            print(request_data)

            serializer = PostSerializer(data=request_data, partial=True)

            if serializer.is_valid():
                if str(request.user.id) == author_id:
                    serializer.save()
                    saved_data = serializer.data
                    saved_id = saved_data.get("id", None)
                    print("Saved id:", saved_id)
                    return saved_id, True
            # print(serializer.errors)
            return None, False
        except Post.DoesNotExist:
            return None, False

    def delete(self, request, author_id, post_id):
        try:
            regular_post = Post.objects.get(id=post_id)
            if str(regular_post.authorId.id) == author_id:
                # Delete the associated image post, if it exists
                if regular_post.image_ref:
                    regular_post.image_ref.delete()

                # Delete the regular post
                regular_post.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AuthorPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        queryset = Post.objects.filter(authorId=author_id)
        queryset = queryset.exclude(contentType__startswith="image/")

        # Order by published date
        queryset = queryset.order_by("-published")
        base_url = request.build_absolute_uri("/")
        serializer = PostSerializer(queryset, many=True, context={"base_url": base_url})
        return Response(serializer.data)

    def post(self, request, author_id):
        request_data = request.data.copy()
        print("DATA", request_data)
        request_data["authorId"] = author_id
        if request_data["image"]:
            id, response = self.create_image_post(
                request, author_id, request.data["image"]
            )
            if response:
                request_data["image_ref"] = id
                print("After making | Current image_ref?:", id)

        # serializer accepts CommonMark content
        request_data['content'] = markdownify(request_data['content'])

        serializer = ServerPostSerializer(data=request_data)
        if serializer.is_valid():
            print("VALID OR NOT")
            if str(request.user.id) == author_id:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_image_post(self, request, author_id, image_blob):
        try:
            request_data = request.data.copy()
            image_info = image_blob.split(",")
            request_data["content"] = image_info[1]
            request_data["contentType"] = image_info[0][5:]
            request_data["image"] = None
            request_data["authorId"] = author_id

            print("image post: ", request_data)
            serializer = ServerPostSerializer(data=request_data)
            print("Serializer validated:", serializer.is_valid())
            if serializer.is_valid():
                if str(request.user.id) == author_id:
                    serializer.save()
                    saved_data = serializer.data
                    saved_id = saved_data.get("id", None)
                    return saved_id, True
            return None, False
        except Exception as e:
            return None, False


class PublicPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter posts by authorId and visibility='PUBLIC'
        queryset = Post.objects.filter(visibility="PUBLIC")
        queryset = queryset.exclude(contentType__startswith="image/")

        # Order by published date
        queryset = queryset.order_by("-published")
        base_url = request.build_absolute_uri("/")
        serializer = PostSerializer(queryset, many=True, context={"base_url": base_url})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
                Q(visibility="PUBLIC") | Q(visibility="FRIENDS"),
                authorId__in=followed_users_ids,
            ).exclude(contentType__startswith="image/")
            # queryset = queryset.exclude(contentType__startswith="image/")

            # Order by published date
            queryset = queryset.order_by("-published")

            # Serialize the queryset to JSON
            base_url = request.build_absolute_uri("/")
            serializer = PostSerializer(
                queryset, many=True, context={"base_url": base_url}
            )

            # Return serialized data as JSON response
            return Response(serializer.data)

        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)


class SharedPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        print("I ENTERED HERE")
        if post.visibility == "PUBLIC" and author_id != str(post.authorId.id):
            serializer = ServerPostSerializer(post)
            shared_post = serializer.data
            shared_post["published"] = timezone.now()
            shared_post["isShared"] = True
            # sharedBy means original author
            shared_post["sharedBy"] = shared_post["authorId"]
            # authorId is the author sharing the post
            shared_post["authorId"] = author_id
            shared_post["visibility"] = "FRIENDS"
            shared_post["originalContent"] = shared_post["content"]
            shared_post["content"] = request.data["content"]
            if post.image_ref:
                shared_post["image_ref"] = post.image_ref.id
            else:
                shared_post["image_ref"] = None
            print(shared_post)
            serializer = ServerPostSerializer(data=shared_post)
            print("VALID?: ", serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "You are not authorized to share this post"},
                status=status.HTTP_403_FORBIDDEN,
            )


class ImagePost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
            if post.image_ref != None:
                base_url = request.build_absolute_uri("/")
                serializer = PostSerializer(
                    post.image_ref, context={"base_url": base_url}
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, author_id, post_id):
        try:
            regular_post = Post.objects.get(id=post_id)
            if str(regular_post.authorId.id) == author_id:
                # Delete the associated image post, if it exists
                if regular_post.image_ref:
                    regular_post.image_ref.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
