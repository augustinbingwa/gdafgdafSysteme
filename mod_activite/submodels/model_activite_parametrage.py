from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.humanize.templatetags.humanize import intcomma

from decimal import Decimal

#-------------------------------------------------------------
class NomMarche(models.Model):
	"""
	Modèle Nom des marchés (Paramétrage)
	"""
	nom = models.CharField(max_length=30, unique=True)
	
	class Meta:
		ordering = ('nom', )
		
	def __str__(self):
		return self.nom

#-------------------------------------------------------------
class DroitPlaceMarche(models.Model):
	"""
	Modèle Droit de place dans le marché (Paramétrage)
	"""
	# nom du marché
	nom_marche = models.ForeignKey(NomMarche, on_delete=models.CASCADE, verbose_name="Marché")

	# Numéro de la place dans le marché
	numero_place = models.CharField(max_length=10, verbose_name="Place n°")

	# Le coût de la place (impôt)
	cout_place = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))], verbose_name="Coût")

	#Si occupée, ce champs sera mis à jour via la validation l'accocation de la place dans le marché
	occupee = models.BooleanField(default=False, verbose_name="Occupée")
	
	class Meta:
		# 'nom_marche', 'numero_place' doivent être 'UNIQUE'
		index_together = unique_together = [['nom_marche', 'numero_place']]

		# Tri
		ordering = ('nom_marche', 'numero_place', )
		
	def __str__(self):
		return self.nom_marche.nom + ' - Place n°' + self.numero_place + ' - ' + str(self.cout_place) + ' BIF'

#-------------------------------------------------------------
class SiteTouristique(models.Model):
	"""
	Modèle Site touristoque (Parametre des lieux touristique : moniment / mausolée / ...)
	"""
	adresse_place = models.CharField(max_length=100)

	# le tarif de la visite par pièce (impôt)
	tarif = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.adresse_place + ' (' +  str(intcomma(self.tarif)) + ' BIF)'