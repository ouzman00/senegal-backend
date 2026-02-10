
from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination

from .models import Hopital, Ecole, Parcelle, Commerce, Boutique, Point, ZA
from .serializers import HopitalSerializer, EcoleSerializer, ParcelleSerializer, CommerceSerializer, BoutiqueSerializer, PointSerializer, ZASerializer


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


# On a la classe avec le scr ici pour directement transformer notre données 2154 en 4326
class PointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Point.objects.exclude(geom__isnull=True)
    #ne maîtrises pas à 100 % son contenu c'est pour cela on n'a pas objects.all()
    serializer_class = PointSerializer

class ZAViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ZA.objects.exclude(geom__isnull=True)
    #ne maîtrises pas à 100 % son contenu c'est pour cela on n'a pas objects.all()
    serializer_class = ZASerializer