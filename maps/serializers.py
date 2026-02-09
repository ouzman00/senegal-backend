from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Hopital, Ecole, Parcelle, Commerce, Boutique, Point


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
    # "localisation" est un alias de "adresse"
    localisation = serializers.CharField(source="adresse", allow_null=True, required=False)

    class Meta:
        model = Boutique
        geo_field = "geom"
        fields = ("id", "localisation", "catégorie")



from rest_framework_gis.serializers import GeoFeatureModelSerializer

class PointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Point
        geo_field = "geom"
        fields = ("fid", "ref_id")

    def to_representation(self, instance):
        if instance.geom and instance.geom.srid != 4326:
            instance.geom = instance.geom.clone()
            instance.geom.transform(4326)
        return super().to_representation(instance)


# class PointSerializer(GeoFeatureModelSerializer):
#     class Meta:
#         model = Point
#         geo_field = "geom"
#         fields = [f.name for f in Point._meta.fields if f.name != "geom"] OLD VERSION ==> NE MARCHE PAS SI ON VEUT TRANSFORMER DIRECTEMENT LE SCR SUR DJANGO

        # ou fields = ("fid", "ref_id")