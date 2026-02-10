from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Hopital, Ecole, Parcelle, Commerce, Boutique, Point, ZA


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


# BoutiqueSerializer est différent parce qu’il ne reflète pas directement la table :
# il transforme volontairement le modèle pour exposer une API plus métier.
class BoutiqueSerializer(GeoFeatureModelSerializer):
    # "localisation" est un alias de "adresse"
    localisation = serializers.CharField(source="adresse", allow_null=True, required=False)

    # "catégorie" n'existe pas en base -> on la calcule (ou valeur fixe)
    catégorie = serializers.SerializerMethodField()

    class Meta:
        model = Boutique
        geo_field = "geom"
        fields = ("id", "localisation", "catégorie")

    def get_catégorie(self, obj):
        return "Boutique"



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
# MARCHE SI ON A AJOUTE UNE COUHE A LA BD RENDER ET QU'ON VEUT L'IMPORTER EN PLUS DEJA EN 4326

        # ou fields = ("fid", "ref_id")






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
#         fields = ("id", "nom", "adresse")

# class EcoleSerializer(Reproject2154To4326GeoSerializer):
#     class Meta:
#         model = Ecole
#         geo_field = "geom"
#         fields = ("id", "nom", "adresse")

# class ParcelleSerializer(Reproject2154To4326GeoSerializer):
#     class Meta:
#         model = Parcelle
#         geo_field = "geom"
#         fields = ("id", "nom", "adresse")

class ZASerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZA
        geo_field = "geom"
        fields = ("fid", "ref_id")

    def to_representation(self, instance):
        if instance.geom and instance.geom.srid != 4326:
            instance.geom = instance.geom.clone()
            instance.geom.transform(4326)
        return super().to_representation(instance)