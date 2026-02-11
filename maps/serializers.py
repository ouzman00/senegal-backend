from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Hopital, Ecole, Parcelle, Commerce, Point, ZA, ZAER

# on pourrait mettre ("pk",) ou ("id",) pour charger jouer un peu sur la rapidité
class HopitalSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hopital
        geo_field = "geom"
        fields = "__all__"

class EcoleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Ecole
        geo_field = "geom"
        fields = "__all__"

class ParcelleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcelle
        geo_field = "geom"
        fields = "__all__"

class CommerceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Commerce
        geo_field = "geom"
        fields = "__all__"


class PointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Point
        geo_field = "geom"
        fields = "__all__"

    def to_representation(self, instance):
        if instance.geom and instance.geom.srid != 4326:
            instance.geom = instance.geom.clone()
            instance.geom.transform(4326)
        return super().to_representation(instance)

class ZASerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZA
        geo_field = "geom"
        fields= "__all__"
    def to_representation(self, instance):
        if instance.geom and instance.geom.srid != 4326:
            instance.geom = instance.geom.clone()
            instance.geom.transform(4326)
        return super().to_representation(instance)
    
class ZAERSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZAER
        geo_field = "geom"
        fields= "__all__"
    def to_representation(self, instance):
        if instance.geom and instance.geom.srid != 4326:
            instance.geom = instance.geom.clone()
            instance.geom.transform(4326)
        return super().to_representation(instance)



# EXEMPLE DE TECHNIQUE POUR EVITER LES REPETITIONS
# TECHNIQUE DE RECONVERSION DES DONNEES EN 4326 QUI SONT EN 2154 SUR MODELE (ma base)

# from rest_framework_gis.serializers import GeoFeatureModelSerializer
# class Reproject2154To4326GeoSerializer(GeoFeatureModelSerializer):
#     def to_representation(self, instance):
#         if instance.geom and instance.geom.srid != 4326:
#             instance.geom = instance.geom.clone()
#             instance.geom.transform(4326)
#         return super().to_representation(instance)
# from .models import Hopital, Ecole, Parcelle, Commerce

# class HopitalSerializer(Reproject2154To4326GeoSerializer):
#     class Meta:
#         model = Hopital
#         geo_field = "geom"
#         fields = ("__all__")

# class EcoleSerializer(Reproject2154To4326GeoSerializer):
#     class Meta:
#         model = Ecole
#         geo_field = "geom"
#         fields = ("pk")

# class ParcelleSerializer(Reproject2154To4326GeoSerializer):
#     class Meta:
#         model = Parcelle
#         geo_field = "geom"
#         fields = ("id", "nom", "adresse")

