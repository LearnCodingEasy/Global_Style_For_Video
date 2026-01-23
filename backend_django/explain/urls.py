
# backend_django\Explain\urls.py
from rest_framework.routers import DefaultRouter
from .views import ExplainViewSet
from .views import ExplainCategoryViewSet


router = DefaultRouter()

router.register("explains_category", ExplainCategoryViewSet,
                basename="explains_category")
router.register("explains", ExplainViewSet, basename="explains")


urlpatterns = router.urls
