from rest_framework.routers import DefaultRouter
from .views import HopitalViewSet, EcoleViewSet, ParcellesViewSet, CommerceViewSet

router = DefaultRouter()
router.register(r"hopitaux", HopitalViewSet, basename="hopitaux")
router.register(r"ecoles", EcoleViewSet, basename="ecoles")
router.register(r"parcelles", ParcellesViewSet, basename="parcelles")
router.register(r"Commerce", CommerceViewSet, basename="Commerce")

urlpatterns = router.urls
