from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Hopital, Ecole, Parcelle

class HopitalSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hopital
        geo_field = "geom"
        fields = ("id", "nom", "adresse")

class EcoleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Ecole
        geo_field = "geom"
        fields = ("id", "nom", "adresse")



class ParcellesSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcelle
        geo_field = "geom"
        fields = ("id", "Section", "Numero")
