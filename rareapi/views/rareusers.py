from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, RareUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'active', 'user_id')  # add other fields as needed
        
class UserViewSet(viewsets.ViewSet):
    queryset = RareUser.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            rareuser = RareUser.objects.create_user(
                bio=serializer.validated_data['bio']
                user_id=serializer.validated_data['user.id']
            )
            token, created = Token.objects.get_or_create(rareuser=rareuser)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        