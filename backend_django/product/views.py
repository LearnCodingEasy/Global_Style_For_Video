# 📄 [ Vendor/api.py ] ملف


from rest_framework import viewsets
from .models import Category
# from .models import Category, Product
from .serializers import CategorySerializer
# from .serializers import CategorySerializer, ProductSerializer

# Console
from rich.console import Console
from rich import print
console = Console()


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
