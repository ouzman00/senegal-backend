from django.contrib.gis.db import models

# pk mieux que l'option id parceque ca prend directement le nom de la clé primaire

class Hopital(models.Model):
    geom = models.PointField(srid=4326)
    def __str__(self) -> str:
        return f"Hopital {self.pk}" 

class Ecole(models.Model):
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    def __str__(self) -> str:
        return f"Ecole {self.pk}" 

class Parcelle(models.Model):
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    def __str__(self) -> str:
        return f"Parcelle {self.pk}" 

class Commerce(models.Model):
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    def __str__(self):
        return f"Commerce {self.pk}" 

class Boutique(models.Model):
    geom = models.PointField(srid=4326, blank=True, null=True)

    def __str__(self) -> str:
        return f"Boutique {self.pk}" 
    

# MODELE QUI POINT VERS LA COUCHE CREER EN 2154

class Point(models.Model):
    # fid = models.BigIntegerField(primary_key=True, db_column="fid")
    # ref_id = models.CharField(max_length=255, blank=True, null=True, db_column="id")

    # On pourrait mettre geom = models.GeometryField(srid=2154) s'il s'agit que des points mais Geometryfield pour toutes les géométries (P, L, P)
    geom = models.PointField(srid=2154)

    class Meta:
        db_table = "maps_point"
        managed = False
#ICI ON METS LE NOM DE LA TABLE A IMPORTER ET MANAGED=FALSE POUR LA TABLE EXTERNE QU'ON MAITRISE PAS
    def __str__(self):
        return f"Point {self.pk}"


class ZA(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    geom = models.MultiPolygonField(srid=2154)

    class Meta:
        db_table = "maps_za"
        managed = False

    def __str__(self):
        return f"ZA {self.pk}"






# POUR GEOM
# PointField ==> Points uniquement
# LineStringField	==> Lignes uniquement
# PolygonField	==> Polygones uniquement
# MultiPolygonField	==> Multipolygones uniquement
# GeometryField	==> Tous les types


# Quand je parle de geom dans mon code, va chercher la colonne wkb_geometry dans la base de données
# ca permet d'aller chercher le polygone et de l'afficher si on n'a pas le meme nom que sur la base de données
# geom = models.GeometryField(srid=2154, db_column="geom")
