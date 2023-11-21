from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer 
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import Tag


class TagView(ViewSet):
    """Rare tags view"""

    def list(self, request):
        tags = Tag.objects.all().order_by('label')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"