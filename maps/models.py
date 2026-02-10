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
    geom = models.PointField(srid=2154)

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
    geom = models.GeometryField(srid=2154, db_column="geom") 

    class Meta:
        db_table = "maps_za"
        managed = False
#ICI ON METS LE NOM DE LA TABLE A IMPORTER ET MANAGED=FALSE POUR LA TABLE EXTERNE QU'ON MAITRISE PAS
    def __str__(self):
        return self.ref_id or f"ZA {self.fid}"