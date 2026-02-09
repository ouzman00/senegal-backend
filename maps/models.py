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
    

# MODELE QUI POINT VERS LA COUCHE CREER

class Point(models.Model):
    fid = models.BigIntegerField(primary_key=True, db_column="fid")

    # colonne SQL "id" (varchar) -> on évite d'appeler le champ Django "id"
    ref_id = models.CharField(max_length=255, blank=True, null=True, db_column="id")

    # x = models.BigIntegerField(blank=True, null=True)
    # y = models.BigIntegerField(blank=True, null=True)
    geom = models.PointField(srid=4326)

    class Meta:
        db_table = "maps_point"
        managed = False

    def __str__(self):
        return self.ref_id or f"Point {self.fid}"
