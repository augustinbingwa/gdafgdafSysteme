from django.contrib import admin
from .models import VehiculeCategorie, VehiculeSousCategorie, VehiculeMarque, VehiculeModele

class VehiculeCategorieAdmin(admin.ModelAdmin):
	list_display = ("nom", "type_roue", )


class VehiculeSousCategorieAdmin(admin.ModelAdmin):
	list_display = ("categorie", "nom", "transport_commun", "has_plaque", "has_compte_propre", "ai_cout_carte_propriete", "ai_cout_carte_professionnelle", "taxe_proprietaire", "taxe_activite", "taxe_stationnement")	

class VehiculeMarqueAdmin(admin.ModelAdmin):
	list_display = ("nom", )

class VehiculeModeleAdmin(admin.ModelAdmin):
	list_display = ("nom", "marque")

admin.site.register(VehiculeCategorie, VehiculeCategorieAdmin)
admin.site.register(VehiculeSousCategorie, VehiculeSousCategorieAdmin)
admin.site.register(VehiculeMarque, VehiculeMarqueAdmin)
admin.site.register(VehiculeModele, VehiculeModeleAdmin)