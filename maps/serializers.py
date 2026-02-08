from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Hopital, Ecole, Parcelle, Commerce, Boutique


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


class ParcelleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcelle
        geo_field = "geom"
        fields = ("id", "nom", "adresse")


class CommerceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Commerce
        geo_field = "geom"
        fields = ("id", "nom", "adresse")

class BoutiqueSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Boutique
        geo_field = "geom"
        fields = ("id", "localisation", "catégorie")