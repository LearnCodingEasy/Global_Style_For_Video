

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import vendorViews

router = DefaultRouter()
router.register('', vendorViews)

urlpatterns = [
    path('', include(router.urls)),
]
