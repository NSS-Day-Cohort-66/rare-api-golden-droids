from rareapi.models import Post
from rest_framework import serializers, viewsets
from rest_framework.response import Response

# ? serializer to show logged in user's posts
class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'rare_user', 'category', 'publication_date', 'content']

class UserPostView(viewsets.ViewSet):
    def list(self, request):
        #? rare_user__user=request.auth.user starts at rare_user table and joins user table to check user's id pk to authorized user's id
        posts = Post.objects.filter(rare_user__user=request.auth.user).order_by('-publication_date')
        serializer = UserPostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)