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
        # if self.request.user.is_staff:
        #     return Vendor.objects.all()
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update_data(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong Object Owner')
        serializer.save()
