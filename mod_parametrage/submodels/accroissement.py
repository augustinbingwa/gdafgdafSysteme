from django.db import models
from django.core.validators import MinValueValidator
import datetime
from decimal import Decimal

#----------------------------------------------------------------------
#----------------- MODELE PARAMETRAGE ACCROISSMENT --------------------
#----------------------------------------------------------------------
class Accroissement(models.Model):
	"""
	Modèle Parametrage des Accroissements
	"""	
	date_debut = models.DateField(default=datetime.date(1900, 1, 1))
	date_fin = models.DateField(default=datetime.date(1900, 1, 1))
	
	taux = models.DecimalField(decimal_places=1, max_digits=10, validators=[MinValueValidator(Decimal('0.0'))], default=0.0)

	# Taux de l'année déjà écouléé
	is_taux_annee_ecoulee = models.BooleanField(default=False)

	class Meta:
		ordering = ('id',)

class AccroissementTaxe(models.Model):
	"""
	Modèle Parametrage des Accroissements
	"""
	date_debut = models.DateField(default=datetime.date(1900, 1, 1))
	date_fin = models.DateField(default=datetime.date(1900, 1, 1))

	taux = models.DecimalField(decimal_places=1, max_digits=10, validators=[MinValueValidator(Decimal('0.0'))],
							   default=0.0)

	# Taux de l'année déjà écouléé
	is_taux_annee_ecoulee = models.BooleanField(default=False)

	class Meta:
		ordering = ('id',)