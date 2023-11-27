from rareapi.models import Post
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .comments import CommentAuthorSerializer
from .categories import CategorySerializer

# ? serializer to show logged in user's posts


class UserPostSerializer(serializers.ModelSerializer):

    rare_user = CommentAuthorSerializer(many=False)
    category = CategorySerializer(many=False)
    class Meta:
        model = Post
        fields = ['id', 'title', 'rare_user', 'category', 'publication_date', 'content']

class UserPostView(viewsets.ViewSet):
    def list(self, request):
        #? rare_user__user=request.auth.user starts at rare_user table and joins user table to check user's id pk to authorized user's id
        posts = Post.objects.filter(rare_user__user=request.auth.user).order_by('-publication_date')
        serializer = UserPostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    # ? left off asking chat GPT how i could get all posts and then filter to current user's in same view
    # ? not sure how you'd implement it correctly or if having duplicate code is easier