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
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single tag

        Returns:
            Response -- JSON serialized object
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        label = request.data.get('label')

        category = Category.objects.create(
            label=label
        )

        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            if request.user.is_staff:
                serializer = CategorySerializer(data=request.data)
                if serializer.is_valid():
                    category.label = serializer.validated_data["label"]
                    category.save()

                    serializer = CategorySerializer(category, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You don't have admin privileges"}, status=status.HTTP_403_FORBIDDEN)
        except Category.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a singular Category

        Returns:
            Response -- 204, 403, 404, or 500 status
        """
        try:
            category = Category.objects.get(pk=pk)
            if request.user.is_staff:
                category.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You don't have admin rights!"}, status=status.HTTP_403_FORBIDDEN)          
        except Category.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    