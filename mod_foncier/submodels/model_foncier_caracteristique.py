from django.conf import settings
from django.db import models

from mod_foncier.models import FoncierImpot 
from mod_foncier.models import FoncierExpertise

from django.core.validators import MinValueValidator, MaxValueValidator

class FoncierCaracteristique(models.Model):	 
	"""
	Modèle Caracteristique de la parcelle (les info technjques des terrains non batîs et batîs)
	"""
	# L'identifiant de l'expertise technique
	expertise = models.ForeignKey(FoncierExpertise, on_delete=models.CASCADE)

	# La superficie batîe (information de la construction)
	superficie_batie = models.PositiveIntegerField(default=0,
		validators=[
			MinValueValidator(0),
			MaxValueValidator(999999)
		]
	)
	
	# Limpot correspondant à chaque caractéristique
	impot_batie = models.ForeignKey(FoncierImpot, on_delete=models.CASCADE)
	
	# Année de mise en valeur de la construction (du batiment)
	# Si l'année de mise en valeur est inférieur ou égal à 2 ans alors la déclaration de ce batiment est éxhonérée 
	annee_mise_valeur = models.PositiveSmallIntegerField(
		validators=[
			MinValueValidator(2014),
			MaxValueValidator(9999)
		], null=True
	) 

	class Meta:
		# expertise et impot_batie doit être 'unique'
		index_together = unique_together = [['expertise', 'impot_batie']]

		ordering = ('-id',)
		
	def __int__(self):
		return self.id