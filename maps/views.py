# views.py
from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination
from django.contrib.gis.db.models.functions import Transform

from .models import Hopital, Ecole, Parcelle, Commerce, Boutique, Point
from .serializers import (
    HopitalSerializer, EcoleSerializer, ParcelleSerializer,
    CommerceSerializer, BoutiqueSerializer, PointSerializer
)


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


class ParcelleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Parcelle.objects.all()
    serializer_class = ParcelleSerializer
    pagination_class = StandardGeoPagination


class CommerceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Commerce.objects.all()
    serializer_class = CommerceSerializer
    pagination_class = StandardGeoPagination


class BoutiqueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer
    pagination_class = StandardGeoPagination


#  ✅ LA VERSION LA PLUS SIMPLE POUR TRANSFORMER 2154 -> 4326
class PointViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PointSerializer
    pagination_class = StandardGeoPagination

    def get_queryset(self):
        return (
            Point.objects.exclude(geom__isnull=True)
            .annotate(geom_4326=Transform("geom", 4326))
        )
