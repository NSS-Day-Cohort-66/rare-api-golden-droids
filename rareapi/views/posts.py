from rareapi.models import Post
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .comments import CommentAuthorSerializer
from .categories import CategorySerializer
from rest_framework import status


# ? serializer to show logged in user's posts


class PostSerializer(serializers.ModelSerializer):

    rare_user = CommentAuthorSerializer(many=False)
    category = CategorySerializer(many=False)
    class Meta:
        model = Post
        fields = ['id', 'title', 'rare_user', 'category', 'publication_date', 'content']

class PostView(viewsets.ViewSet):
    def list(self, request):
        #? rare_user__user=request.auth.user starts at rare_user table and joins user table to check user's id pk to authorized user's id
        posts = Post.objects.filter(rare_user__user=request.auth.user).order_by('-publication_date')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single post

        Returns:
            Response -- JSON serialized object
        """
        try:
            tag = Post.objects.get(pk=pk)
            serializer = PostSerializer(tag, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)