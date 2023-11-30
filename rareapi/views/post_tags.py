from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import Tag, Post, PostTag
from .posts import PostSerializer

# class PostSerializer(ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['title']

# class TagSerializer(ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['label']

class PostTagSerializer(ModelSerializer):

    # post = PostSerializer(many=False)
    # tag = TagSerializer(many=False)

    class Meta:
        model = PostTag
        fields = ["id", "post", "tag"]
        # , "post", "tag"

class PostTagView(ViewSet):
    """Rare Post Tags view"""
    def list(self, request):
        """Handle GET requests for all post tags
        
        Returns:
            Response -- JSON serialized array
        """
        post_tags= PostTag.objects.all()
        serializer = PostTagSerializer(post_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = PostTagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
