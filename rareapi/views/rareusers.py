from rest_framework import viewsets
from rest_framework import serializers
from rareapi.models import RareUser


class RareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'active', 'user_id')  # add other fields as needed
        
class RareUserViewSet(viewsets.ViewSet):
    pass      