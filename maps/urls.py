from rest_framework.routers import DefaultRouter
from .views import HopitalViewSet, EcoleViewSet, ParcellesViewSet

router = DefaultRouter()
router.register(r"hopitaux", HopitalViewSet, basename="hopitaux")
router.register(r"ecoles", EcoleViewSet, basename="ecoles")
router.register(r"parcelles", ParcellesViewSet, basename="parcelles")

urlpatterns = router.urls
