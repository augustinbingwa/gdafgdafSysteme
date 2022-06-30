from django.db import models
from django.core.validators import MinValueValidator
import datetime
from decimal import Decimal

#----------------------------------------------------------------------
#----------------- MODELE PARAMETRAGE ACCROISSMENT --------------------
#----------------------------------------------------------------------
class Penalite(models.Model):
	"""
	Modèle Parametrage des pénalités de paiement des notes d'imposition
	"""	
	date_debut = models.DateField(default=datetime.date(1900, 1, 1))
	date_fin = models.DateField(default=datetime.date(1900, 1, 1))
	taux = models.DecimalField(decimal_places=1, max_digits=10, validators=[MinValueValidator(Decimal('0.0'))], default=0.0)
	is_taux_annee_ecoulee = models.DecimalField(decimal_places=0, max_digits=3, validators=[MinValueValidator(Decimal('0'))], default=0)

	class Meta:
		ordering = ('id',)

class PenaliteTransport(models.Model):
	"""
	Modèle Parametrage des pénalités de paiement des notes d'imposition
	"""
	entity = models.IntegerField(default=11)
	date_debut = models.DateField(default=datetime.date(1900, 1, 1))
	date_fin = models.DateField(default=datetime.date(1900, 1, 1))
	taux_ou_montant = models.DecimalField(decimal_places=1, max_digits=10, validators=[MinValueValidator(Decimal('0.0'))], default=0.0)
	is_taux_date_ecoule = models.BooleanField(default=False)

	class Meta:
		ordering = ('id',)
	