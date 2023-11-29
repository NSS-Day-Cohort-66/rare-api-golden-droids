from rareapi.models import Post
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .comments import RareUserSerializer
from .categories import CategorySerializer
from rest_framework import status
from django.utils import timezone

# ? serializer to show logged in user's posts
print(timezone.now())

class PostSerializer(serializers.ModelSerializer):

    rare_user = RareUserSerializer(many=False)
    category = CategorySerializer(many=False)
    class Meta:
        model = Post
        fields = ['id', 'title', 'rare_user', 'category', 'publication_date', 'image_url', 'content', 'approved']

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

