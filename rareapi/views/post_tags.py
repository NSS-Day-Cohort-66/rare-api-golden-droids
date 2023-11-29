from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import Tag, Post, PostTag

class PostTagSerializer(ModelSerializer):
    class Meta:
        model = PostTag
        fields = "__all__"

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