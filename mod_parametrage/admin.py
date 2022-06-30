from django.contrib import admin
from .models import Province, Commune, Zone, Quartier, RueOuAvenue, Accroissement, Penalite, GlobalVariables,Authority,Fonction,Departement,Service

#--------------------Paramétrage des adresses--------------------------
class ProvinceAdmin(admin.ModelAdmin):
	list_display = ("numero", "nom",)

class CommuneAdmin(admin.ModelAdmin):
	list_display = ("numero", "nom", "province",)	

class ZoneAdmin(admin.ModelAdmin):
	list_display = ("numero", "nom", "commune",)

class QuartierAdmin(admin.ModelAdmin):
	list_display = ("numero", "nom", "zone",)	

class RueOuAvenueAdmin(admin.ModelAdmin):
	list_display = ("zone", "nom", "accessibilite", ) 

class AccroissementAdmin(admin.ModelAdmin):
	list_display = ("id", "date_debut", "date_fin", "taux",)

class PenaliteAdmin(admin.ModelAdmin):
	list_display = ("id", "date_debut", "date_fin", "taux",)

class GlobalVariablesAdmin(admin.ModelAdmin):
	list_display = ("group", "cle", "valeur", "description",)

class AuthorityAdmin(admin.ModelAdmin):
	list_display = ("nom", "prenom",)

class FonctionAdmin(admin.ModelAdmin):
	list_display = ("libele","title")

class DepartementAdmin(admin.ModelAdmin):
	list_display = ("nom",)

class ServiceAdmin(admin.ModelAdmin):
	list_display = ("nom",)

admin.site.register(Province, ProvinceAdmin)
admin.site.register(Commune, CommuneAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Quartier, QuartierAdmin)
admin.site.register(RueOuAvenue, RueOuAvenueAdmin)
admin.site.register(Accroissement, AccroissementAdmin)
admin.site.register(Penalite, PenaliteAdmin)
admin.site.register(GlobalVariables, GlobalVariablesAdmin)
admin.site.register(Authority, AuthorityAdmin)
admin.site.register(Fonction, FonctionAdmin)
admin.site.register(Departement, DepartementAdmin)
admin.site.register(Service, ServiceAdmin)