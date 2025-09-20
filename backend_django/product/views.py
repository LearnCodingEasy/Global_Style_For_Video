# 📄 [ Vendor/api.py ] ملف


# Rest Framework
from rest_framework import viewsets, filters, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

# Element
from .models import Category
from .serializers import CategorySerializer

from datetime import datetime
import uuid


# Console
from rich.console import Console
from rich.table import Table
from rich import box
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
    # --- تابع مساعد لطباعة الجدول في الكونسول ---

    def _print_table_console(self, data_list):
        """
        data_list: list of dict (مثلاً serializer.data)
        هينشئ جدول مرتب ويطبعه في الكونسول باستخدام rich.Table
        """
        if not data_list:
            console.print("[yellow]No data to display[/yellow]")
            return

        # حدد الأعمدة اللي عايز تعرضها وبالترتيب
        columns = ['id', 'name', 'description', 'slug', 'ordering',
                   'created_by', 'created_at', 'created_at_formatted', 'image']

        table = Table(title="All Category", box=box.SIMPLE_HEAVY)
        # أنشئ رؤوس الأعمدة
        for col in columns:
            table.add_column(col, overflow="fold", no_wrap=False)

        # أضف كل صف من البيانات
        for item in data_list:
            row = []
            for col in columns:
                val = item.get(col, None)

                # تنسيقات صغيرة لكل نوع بيانات
                if val is None:
                    cell = "-"
                elif col == 'created_by':
                    # لو قيمة UUID object أو string
                    if isinstance(val, (uuid.UUID,)):
                        cell = str(val)
                    else:
                        # ممكن يكون تم تمثيله كـ "UUID('...')" أو string
                        cell = str(val)
                elif col in ('created_at', 'updated_at'):
                    # لو التاريخ ISO string، حاول نخليه أقصر
                    try:
                        dt = datetime.fromisoformat(val.replace('Z', '+00:00'))
                        cell = dt.strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        cell = str(val)
                else:
                    cell = str(val)
                row.append(cell)
            table.add_row(*row)

        console.print(table)

    def get_queryset(self):
        # admin يشوف كل حاجة
        if self.request.user.is_staff:
            return Category.objects.all()
        # الباقي يشوف الحاجات اللي هو عملها بس
        return Category.objects.filter(created_by=self.request.user)

    # -------- CREATE --------
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"message": "✅ Category created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    # -------- UPDATE --------
    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.created_by and not self.request.user.is_staff:
            raise PermissionDenied("❌ You are not the owner of this category")
        instance = serializer.save()
        console.rule("[bold blue]Category Updated")
        console.print(f"[yellow]Name:[/yellow] {instance.name}")
        console.print(f"[cyan]Updated By:[/cyan] {self.request.user}")
        console.rule()

    # -------- DELETE --------
    def perform_destroy(self, instance):
        if self.request.user != instance.created_by and not self.request.user.is_staff:
            raise PermissionDenied(
                "❌ You are not allowed to delete this category")

        console.rule("[bold red]Category Deleted")
        console.print(f"[yellow]Name:[/yellow] {instance.name}")
        console.print(f"[cyan]Deleted By:[/cyan] {self.request.user}")
        console.rule()

        instance.delete()

    # ----- Toggle Active -----
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        category = self.get_object()
        category.is_active = not category.is_active
        category.save()
        return Response(
            {"message": "✅ Status toggled", "is_active": category.is_active}
        )
