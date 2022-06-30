from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from mod_parametrage.models import Accessibilite
import datetime
#----------------------------------------------------------------------
#---------------- MODELES PARAMETRAGE CONSTRUCTION  -------------------
#----------------------------------------------------------------------
class FoncierCategorie(models.Model):
	"""
	Modèle Catégorie de la contruction. Ex: Construction avec ossature en béton armé ou métallique
	"""
	nom = models.CharField(max_length=100, unique=True)			

	class Meta:
		ordering = ('id',)

	def __str__(self):
		return self.nom

#----------------------------------------------------------------------
class FoncierTypeConfort(models.Model):	
	"""
	Modèle Type de confort d'une construction. Ex: WC intérieur
	"""
	nom = models.CharField(max_length=100,unique=True)

	class Meta:
		ordering = ('id',)

	def __str__(self):
		return self.nom 

#----------------------------------------------------------------------
class FoncierImpot(models.Model):	
	"""
	Modèle Impôt, qui contient le paramétrage des différents impôt selon les caractéristiquess
	"""
	categorie = models.ForeignKey(FoncierCategorie, on_delete=models.CASCADE)
	
	type_confort = models.ForeignKey(FoncierTypeConfort, on_delete=models.CASCADE)
	
	accessibilite = models.ForeignKey(Accessibilite, on_delete=models.CASCADE)
	
	impot = models.DecimalField(decimal_places=0, max_digits=10, validators=[MinValueValidator(Decimal('0.00'))])
	
	class Meta:
		# 'categorie', 'type_confort', 'accessibilite' doivent être 'UNIQUE'
		index_together = unique_together = [['categorie', 'type_confort', 'accessibilite']]

		ordering = ('id',)

	def __str__(self):
		return self.categorie.nom  + " - " + self.type_confort.nom + " - " + self.accessibilite.nom + " - " + self.impot.__str__()

#----------------------------------------------------------------------
#----------	MODELE PARAMETRAGE TERRAIN NON BATIE (TNB) ----------------
#----------------------------------------------------------------------
class FoncierTnbCategorie(models.Model):
	"""
	Modèle Categorie des Terrains NON batît. Ex: Raccordé au réseau d'eau potable et au réseau d'électricité
	"""
	nom = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ('id',)

	def __str__(self):
		return self.nom

#----------------------------------------------------------------------
class FoncierTnbImpot(models.Model):
	"""
	Modèle Impôt attribué au terrain NON batî
	"""	
	tnb_categorie = models.ForeignKey(FoncierTnbCategorie, on_delete=models.CASCADE)	
	
	accessibilite = models.ForeignKey(Accessibilite, on_delete=models.CASCADE)
	
	impot = models.DecimalField(decimal_places=3, max_digits=10, validators=[MinValueValidator(Decimal('0.00'))])
	
	class Meta:
		# 'tnb_categorie', 'accessibilite' doievent être 'UNIQUE'
		index_together = unique_together = [['tnb_categorie', 'accessibilite']]

		ordering = ('id',)

	def __str__(self):
		return self.tnb_categorie.nom  + " - " + self.accessibilite.nom + " - " + self.impot.__str__().replace('.',',')