from rest_framework.routers import DefaultRouter
from .views import HopitalViewSet, EcoleViewSet, ParcelleViewSet, CommerceViewSet

router = DefaultRouter()
router.register("hopitaux", HopitalViewSet, basename="hopitaux")
router.register("ecoles", EcoleViewSet, basename="ecoles")
router.register("parcelles", ParcelleViewSet, basename="parcelles")
router.register("commerces", CommerceViewSet, basename="commerces")

urlpatterns = router.urls
