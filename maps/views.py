from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination

from .models import Hopital, Ecole
from .serializers import HopitalSerializer, EcoleSerializer


class StandardGeoPagination(GeoJsonPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 5000


class HopitalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hopital.objects.all()
    serializer_class = HopitalSerializer
    pagination_class = StandardGeoPagination


class EcoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ecole.objects.all()
    serializer_class = EcoleSerializer
    pagination_class = StandardGeoPagination
