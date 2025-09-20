# 📄 [ Vendor/api.py ] ملف


# rest_framework
from rest_framework import viewsets, filters, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

# Element
from .models import Category
from .serializers import CategorySerializer

# Console
from rich.console import Console
from rich import print
console = Console()


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # ✨ Search & Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']

    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    # -------- LIST --------
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        # Print in console
        console.rule("[bold green]All Category")
        console.print(f"[yellow]📋 Data:[/yellow] {serializer.data}")
        console.rule()

        return Response(
            {"message": "Categories list", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    # ✅ تخصيص الـ queryset

    def get_queryset(self):
        # admin يشوف كل حاجة
        if self.request.user.is_staff:
            return Category.objects.all()
        # الباقي يشوف الحاجات اللي هو عملها بس
        return Category.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        When creating the item
        Created_by = current user
        """
        instance = serializer.save(created_by=self.request.user)

        # Print in console
        console.rule("[bold green]New Category Created")
        console.print(f"[yellow]Name:[/yellow] {instance.name}")
        console.print(f"[cyan]Created By:[/cyan] {instance.created_by}")
        console.print(f"[magenta]ID:[/magenta] {instance.id}")
        console.rule()

        # ✅ عند التحديث

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.created_by and not self.request.user.is_staff:
            raise PermissionDenied("❌ You are not the owner of this category")
        instance = serializer.save()
        console.rule("[bold blue]Category Updated")
        console.print(f"[yellow]Name:[/yellow] {instance.name}")
        console.print(f"[cyan]Updated By:[/cyan] {self.request.user}")
        console.rule()
