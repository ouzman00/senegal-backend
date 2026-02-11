from rest_framework.routers import DefaultRouter
from .views import HopitalViewSet, EcoleViewSet, ParcelleViewSet, CommerceViewSet, PointViewSet, ZAViewSet, ZAERViewSet

router = DefaultRouter()
router.register("hopitaux", HopitalViewSet, basename="hopitaux")
router.register("ecoles", EcoleViewSet, basename="ecoles")
router.register("parcelles", ParcelleViewSet, basename="parcelles")
router.register("commerces", CommerceViewSet, basename="commerces")
router.register("points", PointViewSet, basename="points")
router.register("za", ZAViewSet, basename="za")
router.register("zaer", ZAERViewSet, basename="zaer")

urlpatterns = router.urls
