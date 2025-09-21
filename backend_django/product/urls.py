from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView
# from .views import CategoryView, ProductView

router = DefaultRouter()
# ✅ plural
router.register(r'category', CategoryView, basename='category')  

# router.register(r'product', ProductView, basename="product")

urlpatterns = [
    path('', include(router.urls)),
]
