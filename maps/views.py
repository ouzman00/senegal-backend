from rest_framework import viewsets
from .models import Hopital, Ecole
from .serializers import HopitalSerializer, EcoleSerializer

class HopitalViewSet(viewsets.ModelViewSet):
    queryset = Hopital.objects.all()  # ou .filter(geom__isnull=False)
    serializer_class = HopitalSerializer

class EcoleViewSet(viewsets.ModelViewSet):
    queryset = Ecole.objects.all()
    serializer_class = EcoleSerializer
