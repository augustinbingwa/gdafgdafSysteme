from django.contrib import admin
from mod_foncier.submodels.model_foncier_parametrage import * #Import de tous les models de construction.py
#------------------------------------------------------
#--------------------Admin CONSTRUCTION ----------------------
#------------------------------------------------------
class FoncierCategorieAdmin(admin.ModelAdmin):
	list_display = ("id", "nom",)
admin.site.register(FoncierCategorie,FoncierCategorieAdmin)

class FoncierTypeConfortAdmin(admin.ModelAdmin):
	list_display = ("id", "nom",)
admin.site.register(FoncierTypeConfort,FoncierTypeConfortAdmin)

class FoncierImpotAdmin(admin.ModelAdmin):
	list_display = ("id", "categorie", "type_confort", "accessibilite", "impot",)
admin.site.register(FoncierImpot,FoncierImpotAdmin)

class FoncierTnbCategorieAdmin(admin.ModelAdmin):
	list_display = ("id", "nom",)
admin.site.register(FoncierTnbCategorie,FoncierTnbCategorieAdmin)

class FoncierTnbImpotAdmin(admin.ModelAdmin):
	list_display = ("id", "tnb_categorie", "accessibilite", "impot",)
admin.site.register(FoncierTnbImpot,FoncierTnbImpotAdmin)