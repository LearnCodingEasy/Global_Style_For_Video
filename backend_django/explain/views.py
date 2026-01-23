# backend_django\explain\views.py

from rest_framework import viewsets, status, filters, permissions

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from django.utils import timezone

from .models import ExplainCategory
from .serializers import ExplainCategorySerializer

from .models import Explain
from .serializers import ExplainSerializer


# ==================================================
# 1️⃣ Explain
# ==================================================

class ExplainCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExplainCategory.objects.all()
    serializer_class = ExplainCategorySerializer


class ExplainViewSet(viewsets.ModelViewSet):
    queryset = Explain.objects.all()
    serializer_class = ExplainSerializer
    parser_classes = (MultiPartParser, FormParser)
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user,
                        profile=self.request.user
                        )
