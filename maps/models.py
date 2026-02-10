from django.contrib.gis.db import models


class Hopital(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PointField(srid=4326)

    def __str__(self) -> str:
        return self.nom


class Ecole(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)

    def __str__(self) -> str:
        return self.nom


class Parcelle(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)

    def __str__(self) -> str:
        return self.nom

# SIMPLE
# class Commerce(models.Model):
#     geom = models.MultiPolygonField(srid=4326, blank=True, null=True)

#     def __str__(self):
#         return f"Commerce {self.id}"


class Commerce(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)

    def __str__(self) -> str:
        return self.nom


class Boutique(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    geom = models.PointField(srid=4326, blank=True, null=True)

    def __str__(self) -> str:
        return self.nom
    

# MODELE QUI POINT VERS LA COUCHE CREER EN 2154

class Point(models.Model):
    fid = models.BigIntegerField(primary_key=True, db_column="fid")

    # colonne SQL "id" (varchar) -> on évite d'appeler le champ Django "id"
    ref_id = models.CharField(max_length=255, blank=True, null=True, db_column="id")

    # x = models.BigIntegerField(blank=True, null=True)
    # y = models.BigIntegerField(blank=True, null=True)
    # On pourrait mettre geom = models.GeometryField(srid=2154) s'il s'agit que des points mais Geometryfield pour toutes les géométries (P, L, P)
    geom = models.GeometryField(srid=2154)

    class Meta:
        db_table = "maps_point"
        managed = False
#ICI ON METS LE NOM DE LA TABLE A IMPORTER ET MANAGED=FALSE POUR LA TABLE EXTERNE QU'ON MAITRISE PAS
    def __str__(self):
        return self.ref_id or f"Point {self.fid}"


class ZA(models.Model):
    fid = models.BigIntegerField(primary_key=True, db_column="fid")

    # colonne SQL "id" (varchar) -> on évite d'appeler le champ Django "id"
    ref_id = models.CharField(max_length=255, blank=True, null=True, db_column="id")
    geom = models.GeometryField(srid=2154) 

    class Meta:
        db_table = "maps_za"
        managed = False
#ICI ON METS LE NOM DE LA TABLE A IMPORTER ET MANAGED=FALSE POUR LA TABLE EXTERNE QU'ON MAITRISE PAS
    def __str__(self):
        return self.ref_id or f"ZA {self.fid}"
    



# PointField ==> Points uniquement
# LineStringField	==> Lignes uniquement
# PolygonField	==> Polygones uniquement
# MultiPolygonField	==> Multipolygones uniquement
# GeometryField	==> Tous les types


# Quand je parle de geom dans mon code, va chercher la colonne wkb_geometry dans la base de données
# ca permet d'aller chercher le polygone et de l'afficher si on n'a pas le meme nom que sur la base de données

# geom = models.GeometryField(srid=2154, db_column="geom")
