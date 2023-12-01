from rareapi.models import Post, PostReaction, RareUser, Category
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .comments import RareUserSerializer
from .categories import CategorySerializer
from rest_framework import status
from django.utils import timezone
import uuid
import base64
from django.core.files.base import ContentFile

# ? serializer to show logged in user's posts

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ['id', 'post', 'rare_user', 'reaction']


class PostSerializer(serializers.ModelSerializer):

    rare_user = RareUserSerializer(many=False)
    category = CategorySerializer(many=False)
    post_reactions = PostReactionSerializer(many=True, source='postreaction_set')
    class Meta:
        model = Post
        fields = ['id', 'title', 'rare_user', 'category', 'publication_date', 'image_url', 'content', 'post_reactions', 'approved']

class PostView(viewsets.ViewSet):
    def list(self, request):
        # get query parameters from request for specific user
        rare_user = self.request.query_params.get('rare_user', None)

        # filter to allow for all and specific user's posts
        # if checks for specific user
        if rare_user is not None and rare_user == "current":
            posts = Post.objects.filter(rare_user__user=request.auth.user).order_by('-publication_date')
        else:
            # otherwise get all posts & filter by approved and dates in the past
            posts = Post.objects.filter(approved=True, publication_date__lt=timezone.now()).order_by('-publication_date')
        for post in posts:
            post.publication_date = post.publication_date.strftime("%m-%d-%Y")

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single post

        Returns:
            Response -- JSON serialized object
        """
        try:
            post = Post.objects.get(pk=pk)
            post.publication_date = post.publication_date.strftime("%m-%d-%Y")
            serializer = PostSerializer(post, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- empty response body
        """
        try:
            post = Post.objects.get(pk=pk)
            if post.rare_user.user_id == request.user.id or request.user.is_staff:
                post.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "You are not the author of this post."}, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, pk=None):
        """Handle PUT requests for a single post

        Returns:
            Response -- JSON serialized object
        """
        try:
            post = Post.objects.get(pk=pk)
            format, imgstr = request.data["image_url"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data[""]}')
            
            if post.rare_user.user_id == request.user.id:
                serializer = PostSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                    post.category = Category.objects.get(pk=request.data["categoryId"])
                    post.title = serializer.validated_data["title"]
                    post.image_url = serializer.validated_data["image_url"]
                    post.content = serializer.validated_data["content"]
                    post.save()

                    serializer = PostSerializer(post, context={"request": request})
                    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You are not the author of this post."}, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

