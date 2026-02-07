from django.contrib import admin
from .models import Hopital, Ecole

@admin.register(Hopital)
class HopitalAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "adresse")
    search_fields = ("nom", "adresse")

@admin.register(Ecole)
class EcoleAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "adresse")
    search_fields = ("nom", "adresse")
