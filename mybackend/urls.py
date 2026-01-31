from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return HttpResponse("Bienvenue sur l'API GeoMap !")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("maps.urls")),
    path("", home),
]

# 👉 pour éviter le 404 sur /favicon.ico
urlpatterns += static(
    "/favicon.ico",
    document_root=settings.STATICFILES_DIRS[0]
)
