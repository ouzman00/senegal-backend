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
