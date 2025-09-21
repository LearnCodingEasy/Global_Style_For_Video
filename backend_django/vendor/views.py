# 📄 [ Vendor/api.py ] ملف

# Rest Framework
from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

# Element
from .models import Vendor
from .serializers import VendorSerializer, VendorDetailSerializer
from users_accounts.serializers import UserSerializer

# Console
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print
console = Console()


class vendorViews(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    # ✨ Search & Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']

    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    # -------- LIST --------
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print('request', self.request.user)

        serializer = self.get_serializer(queryset, many=True)

        # ✅ Create Table
        console.rule("[bold green]All Vendor Table")
        table = Table(
            title="All Vendors",
            box=box.SIMPLE_HEAVY,
            header_style="bold magenta"
        )
        table.add_column("Name", style="green")
        table.add_column("created_by", style="yellow")
        table.add_column("Created At", style="red")
        for item in serializer.data:
            table.add_row(
                str(item.get("name", "")),
                str(item.get(self.request.user, "")),
                # str(item.get("created_by", "")),
                str(item.get("created_at_formatted", item.get("created_at", ""))),
            )
        console.print(table)
        console.rule()

        return Response(
            {"message": "Vendors list", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    # -- Control user View --

    def get_queryset(self):
        # admin يشوف كل حاجة
        if self.request.user.is_staff:
            return Vendor.objects.all()
        # الباقي يشوف الحاجات اللي هو عملها بس
        return self.queryset.filter(created_by=self.request.user)

    # -------- CREATE --------
    def perform_create(self, serializer):
        """
        عند الانشاء
        بنضيف created_by = المستخدم الحالي
        """
        instance = serializer.save(created_by=self.request.user)

        # Toggle Is Vendor On App User
        user = self.request.user
        user.is_vendor = True
        user.save()

        # Print in console
        console.rule("[bold green]New Vendor Created")
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
                "message": "Vendor Created Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update_data(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.created_by:
            raise PermissionDenied('You are not the owner of this Vendor')
        serializer.save()
