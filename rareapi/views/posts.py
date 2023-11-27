from rareapi.models import Post
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .comments import CommentAuthorSerializer
from .categories import CategorySerializer
from django.utils import timezone

# ? serializer to show logged in user's posts


class PostSerializer(serializers.ModelSerializer):

    rare_user = CommentAuthorSerializer(many=False)
    category = CategorySerializer(many=False)
    class Meta:
        model = Post
        fields = ['id', 'title', 'rare_user', 'category', 'publication_date', 'content']

class PostView(viewsets.ViewSet):
    def list(self, request):
        # get query parameters from request for specific user
        rare_user = self.request.query_params.get('rare_user', None)

        # filter approved posts only
        posts = Post.objects.filter(approved=True, publication_date__lte=timezone.now())

        # filter to allow for all and specific user's posts
        # if checks for specific user
        if rare_user is not None and rare_user == "current":
            posts = Post.objects.filter(rare_user__user=request.auth.user).order_by('-publication_date')
        else:
            # otherwise get all posts
            posts = Post.objects.all().order_by('-publication_date')

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

