from django.db import models
from mod_parametrage.enums import *
from django.core.validators import MinValueValidator
from django.contrib.humanize.templatetags.humanize import intcomma

from mod_finance.submodels.model_parametrage import *
from mod_crm.models import Contribuable
from mod_parametrage.enums import *

from decimal import Decimal

class TaxeCategorie(models.Model):
    """
    Modele : Catégorie des taxes
    """
    # 1 - Libellé de la catégorie de taxe
    libelle = models.CharField(max_length=100, blank=False, unique=True, verbose_name="Libellé de la catégorie de taxes ")
    
    # 2 = Avis d'imposition ou 1 = Note d'imposition
    type_impot = models.IntegerField(choices=choix_imposition, verbose_name="Type d'impôt")  

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.libelle

# Modele : Taxes ou Matières imposables
class Taxe(models.Model):
    categorie_taxe = models.ForeignKey(TaxeCategorie, on_delete=models.CASCADE, verbose_name="Catégorie des taxes")
    
    code = models.CharField(max_length=5, blank=False, unique=True)
    
    libelle = models.CharField(max_length=100, blank=False, unique=True, verbose_name="Matière imposable")
    
    nom_activite = models.CharField(max_length=100, blank=True, null=True)  

    type_tarif = models.IntegerField(choices=choix_tarif, verbose_name="Type du tarif")
    
    tarif = models.DecimalField(decimal_places=0, max_digits=10, validators=[MinValueValidator(Decimal('0.00'))])

    periode_type = models.ForeignKey(PeriodeType, on_delete=models.CASCADE)

    imputation_budgetaire = models.CharField(max_length=10, blank=False, verbose_name="Imputation budgétaire")
    
    commentaire = models.TextField(max_length=1024, blank=True, null=True)

    # Facilite le filtre des taxes, exemple : Transport, Activité Standard et Marché, Administratif, Espace publique, Panneau, Mur, ....
    taxe_filter = models.IntegerField(choices=choix_taxe_filter, default=0, verbose_name="Type de taxe")

    class Meta:
        ordering = ('code',)

    def __str__(self):
        if self.type_tarif == FORFAITAIRE:
            libelle_tarif = ', Tarif ' + self.periode_type.libelle + ': ' + str(intcomma(self.tarif)) + ' BIF)'
        if self.type_tarif == POURCENTAGE:
            libelle_tarif = ', Tarif ' + self.periode_type.libelle + ': ' + str(self.tarif) + '%)'
        elif self.type_tarif == VARIABLE:
            libelle_tarif = ', Tarif ' + self.periode_type.libelle + ': ' +  self.get_type_tarif_display().lower() + ')'

        return self.code + ' - ' + self.libelle + libelle_tarif   
