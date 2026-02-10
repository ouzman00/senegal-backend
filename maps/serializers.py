from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Hopital, Ecole, Parcelle, Commerce, Boutique, Point, ZA

# on pourrait mettre __all__ pour charger tout mais pk ou fid pour indexer la classe
class HopitalSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hopital
        geo_field = "geom"
        fields = ("pk",)

class EcoleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Ecole
        geo_field = "geom"
        fields = ("pk",)

class ParcelleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcelle
        geo_field = "geom"
        fields = ("pk",)

class CommerceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Commerce
        geo_field = "geom"
        fields = ("pk",)


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
        fields = ("pk",)

    def get_catégorie(self, obj):
        return "Boutique"


class PointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Point
        geo_field = "geom"
        fields = ("pk",)

    def to_representation(self, instance):
        if instance.geom and instance.geom.srid != 4326:
            instance.geom = instance.geom.clone()
            instance.geom.transform(4326)
        return super().to_representation(instance)

class ZASerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZA
        geo_field = "geom"
        fields= ("pk",)
        # fields = ("fid", "ref_id") __all__ ou les noms des colonnes pour tous les champs, plus sur
    def to_representation(self, instance):
        if instance.geom and instance.geom.srid != 4326:
            instance.geom = instance.geom.clone()
            instance.geom.transform(4326)
        return super().to_representation(instance)



# UTILISER "fid", ou pk pour un chargement plus rapide

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

