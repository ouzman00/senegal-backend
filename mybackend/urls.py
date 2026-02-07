from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(_request):
    return HttpResponse("Bienvenue sur l'API GeoMap !")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("maps.urls")),
    path("", home),
]
