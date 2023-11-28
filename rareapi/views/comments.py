"""View module for handling requests about comments"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import status
from rareapi.models import Post, Comment, RareUser
from django.contrib.auth.models import User
from django.http import HttpResponseServerError


class CommentView(ViewSet):
    """Rare comments view"""

    def list(self, request):
        """Handle GET requests for all comments

        Returns:
            Response -- JSON serialized array
        """
        post_id = self.request.query_params.get("post", None)

        try:
            comments = Comment.objects.all().order_by('created_on')
            # Format created_on to only have the date before serializing
            if post_id is not None:
                comments = Comment.objects.filter(post_id=post_id).order_by('created_on')
            for comment in comments:
                comment.created_on = comment.created_on.strftime("%m-%d-%Y")
            serializer = CommentSerializer(comments, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized comment instance
        """

        post_id = Post.objects.get(pk=request.data['postId'])
        rare_user = RareUser.objects.get(user=request.user.id)
        content = request.data.get("content")

        comment = Comment.objects.create(
            post = post_id,
            author = rare_user,
            content = content,
        )

        comment.created_on = comment.created_on.strftime("%m-%d-%Y")

        try:
            serializer = CommentSerializer(comment, context={"request": request} )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)
        

    # def destroy(self, request, pk=None):




"""Serializers for Comments"""

class AuthorUserSerializer(ModelSerializer):
    """JSON serializer for user tied to author"""

    full_name = SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ("id", "full_name",)

class CommentAuthorSerializer(ModelSerializer):
    """JSON serializer for author of comments (rare_user)"""

    user = AuthorUserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ("id", "user",)

class CommentSerializer(ModelSerializer):
    """JSON serializer for comments"""

    is_owner = SerializerMethodField()
    author = CommentAuthorSerializer(many=False)

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.author.user

    class Meta:
        model = Comment
        fields = "__all__"

