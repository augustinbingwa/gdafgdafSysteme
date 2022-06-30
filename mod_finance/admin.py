from django.contrib import admin

from mod_finance.submodels.model_parametrage import *  # Import de tous les models de paiement.py
from mod_finance.submodels.model_taxe import *  # Import de tous les models de taxe.py

# ------------------------------------------------------
# --------------------Admin taxes ----------------------
# ------------------------------------------------------
class TaxeCategorieAdmin(admin.ModelAdmin):
    list_display = ("id", "libelle", "type_impot")


class TaxeAdmin(admin.ModelAdmin):
    list_display = (
        "categorie_taxe",
        "taxe_filter",
        "code",
        "libelle",
        "type_tarif",
        "tarif",
        "imputation_budgetaire",
        "periode_type",
    )


admin.site.register(TaxeCategorie, TaxeCategorieAdmin)

admin.site.register(Taxe, TaxeAdmin)

# ------------------------------------------------------
# ---------------------Admin paiements------------------
# ------------------------------------------------------
class AgenceUserAdmin(admin.ModelAdmin):
    list_display = ("user", "agence")


class AgenceUserInline(admin.TabularInline):
    model = AgenceUser
    autocomplete_fields = ("user",)


class AgenceAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "sigle", "nom", "compte", "operateur")
    inlines = [AgenceUserInline]


class OperateurAdmin(admin.ModelAdmin):
    list_display = ("id", "libelle")


class PeriodeTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "libelle", "temps", "categorie")


class PeriodeAdmin(admin.ModelAdmin):
    list_display = ("id", "element", "periode_type")


admin.site.register(AgenceUser, AgenceUserAdmin)
admin.site.register(Agence, AgenceAdmin)
admin.site.register(Operateur, OperateurAdmin)
admin.site.register(PeriodeType, PeriodeTypeAdmin)
admin.site.register(Periode, PeriodeAdmin)
