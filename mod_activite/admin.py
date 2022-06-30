from django.contrib import admin
from .models import NomMarche, DroitPlaceMarche, SiteTouristique

class NomMarcheAdmin(admin.ModelAdmin):
	list_display = ("nom",)

class DroitPlaceMarcheAdmin(admin.ModelAdmin):
	list_display = ("nom_marche", "numero_place", "cout_place", "occupee")

class SiteTouristiqueAdmin(admin.ModelAdmin):
	list_display = ("adresse_place", "tarif")

admin.site.register(NomMarche, NomMarcheAdmin)
admin.site.register(DroitPlaceMarche, DroitPlaceMarcheAdmin)
admin.site.register(SiteTouristique, SiteTouristiqueAdmin)