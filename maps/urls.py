from rest_framework.routers import DefaultRouter
from .views import HopitalViewSet, EcoleViewSet

router = DefaultRouter()
router.register(r"hopitaux", HopitalViewSet, basename="hopitaux")
router.register(r"ecoles", EcoleViewSet, basename="ecoles")

urlpatterns = router.urls
