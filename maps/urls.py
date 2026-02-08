from rest_framework.routers import DefaultRouter
from .views import HopitalViewSet, EcoleViewSet, ParcelleViewSet, CommerceViewSet, BoutiqueViewSet

router = DefaultRouter()
router.register("hopitaux", HopitalViewSet, basename="hopitaux")
router.register("ecoles", EcoleViewSet, basename="ecoles")
router.register("parcelles", ParcelleViewSet, basename="parcelles")
router.register("commerces", CommerceViewSet, basename="commerces")
router.register("boutique", BoutiqueViewSet, basename="boutique")

urlpatterns = router.urls
