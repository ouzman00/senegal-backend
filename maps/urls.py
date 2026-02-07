from rest_framework.routers import DefaultRouter
from .views import HopitalViewSet, EcoleViewSet, ParcelleViewSet, CommerceViewSet

router = DefaultRouter()
router.register(r"hopitaux", HopitalViewSet, basename="hopitaux")
router.register(r"ecoles", EcoleViewSet, basename="ecoles")
router.register(r"parcelles", ParcelleViewSet, basename="parcelles")
router.register(r"commerces", CommerceViewSet, basename="commerces")

urlpatterns = router.urls
