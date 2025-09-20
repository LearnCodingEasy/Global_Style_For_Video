# 📄 [ Vendor/api.py ] ملف


from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rich import print
from rich.console import Console
from .models import Vendor
from .serializers import VendorSerializer, VendorDetailSerializer
from users_accounts.serializers import UserSerializer

# Console
console = Console()


class vendorViews(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    print(f"queryset {queryset}")
    # parser_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Vendor.objects.all()
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        عند الانشاء
        بنضيف created_by = المستخدم الحالي
        """
        instance = serializer.save(created_by=self.request.user)

        # طباعة في الكنسول
        console.rule("[bold green]New Category Created")
        console.print(f"[yellow]Name:[/yellow] {instance.name}")
        console.print(f"[cyan]Created By:[/cyan] {instance.created_by}")
        console.print(f"[magenta]ID:[/magenta] {instance.id}")
        console.rule()

    def create(self, request, *args, **kwargs):
        """
        نعمل Override للـ create
        عشان نقدر نرجع Response مخصص
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        console.log("[bold blue]API Response Sent Successfully")

        return Response(
            {
                "message": "✅ Category created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update_data(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong Object Owner')
        serializer.save()
