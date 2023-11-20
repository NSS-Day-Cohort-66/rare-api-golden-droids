from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rareapi.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        label = request.data.get('label')

        category = Category.objects.create(
            label=label
        )

        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    