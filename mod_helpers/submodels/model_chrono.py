from django.db import models

#----------------------------------------------------------------------
#------------------------	MODULE HELPERS    -------------------------
#----------------------------------------------------------------------

"""
Il s'agit de la génération automatique des numéro de référence ou code de n'importe quelle modèle du système
Exemple : Numero d'avis ou note d'imposition, numéro de quittance, différentes cartes produites(carte d'activité, vélo, etc), etc.
Le numéro est composé de focntionalité comme prefixe +  année + mois + longeur de chiffre pour le numero chronologique
"""

#Modèle Numérotation Chronologique
class Chrono(models.Model):
	prefixe = models.CharField(max_length=3, blank=False, unique=True) #AI
	fonctionalite = models.CharField(max_length=50, blank=False, unique=True) #Avis d'Imposition
	annee = models.BooleanField(default=True) #Ex 2017
	mois = models.BooleanField(default=True) #Ex 12
	nombre = models.PositiveSmallIntegerField() #Ex 5 chiffres
	last_chrono = models.CharField(max_length=50, blank=True) #Ex AI20171200001

	class Meta:
		ordering = ('fonctionalite', 'annee', 'mois', )
		
	def __str__(self):
		return self.prefixe