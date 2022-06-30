from django.db import models
from mod_parametrage.enums import *

#----------------------------------------------------------------------
#------------------- Paramétrage des adresses -------------------------
#----------------------------------------------------------------------
class Province(models.Model):
	"""
	Modele Province.
	"""
	numero = models.PositiveSmallIntegerField(unique=True, verbose_name="Numéro de la province")
	nom = models.CharField(max_length=15, unique=True, verbose_name="Nom de la province")
	
	class Meta:
		ordering = ('numero', )
		
	def __str__(self):
		return self.nom

#----------------------------------------------------------------------
class Commune(models.Model):
	"""
	Modele Commune. Une province peut avoir plusieurs communes
	"""
	numero = models.PositiveSmallIntegerField(unique=True, verbose_name="Numéro de la commune")
	nom = models.CharField(max_length=25,unique=True, verbose_name="Nom de la commune")
	province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province de la commune")
	
	class Meta:
		ordering = ('nom','numero' )

	def __str__(self):
		return self.nom + ' - (Province de ' + self.province.nom + ')'

#----------------------------------------------------------------------
class Zone(models.Model):
	"""
	Modele Zone. Une commune peut avoir plusieurs zones
	"""
	numero = models.PositiveSmallIntegerField(unique=True, verbose_name="Numéro de la zone")
	nom = models.CharField(max_length=25, unique=True, verbose_name="Nom de la zone")
	commune = models.ForeignKey(Commune, on_delete=models.CASCADE, verbose_name="Commune de la zone")
	class Meta:
		ordering = ('commune','numero' )

	def __str__(self):
		return self.nom + ' - (Commune de ' + self.commune.nom + ')'

#----------------------------------------------------------------------
class Quartier(models.Model):
	"""
	Modele Quartier. Une zone peut avoir plusieurs quartiers
	"""
	numero = models.PositiveSmallIntegerField(verbose_name="Numéro du quartier")
	nom = models.CharField(max_length=25, verbose_name="Nom du quartier")
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="Zone du quartier")
	
	class Meta:
		# zone + nom + numero doivent être 'unique'
		index_together = unique_together = [['zone', 'nom', 'numero']]

		ordering = ('zone','numero', )

	def __str__(self):
		return self.nom + ' - (Zone de ' + self.zone.nom + ')'

#----------------------------------------------------------------------
class Accessibilite(models.Model):
	"""
	#Modèle Accessibilité d'un terrain non batît ou non batît. Ex : Route revetûe
	"""	
	nom = models.CharField(max_length=100, unique=True)	

	class Meta:
		ordering = ('id',)

	def __str__(self):
		return self.nom

#----------------------------------------------------------------------
class RueOuAvenue(models.Model):
	"""
	Modele RueOuAvenue. Ex : Boulevard de l'europe, Avenue d' independance n°1, ...
	"""
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	nom = models.CharField(max_length=50, verbose_name="Nom de rue ou avenue")	
	accessibilite = models.ForeignKey(Accessibilite, on_delete=models.CASCADE, null=True)
	
	class Meta:
		# zone + nom doit être 'unique'
		index_together = unique_together = [['zone', 'nom']]

		ordering = ('zone', )

	def __str__(self):
		return self.nom


# ----------------------------------------------------------------------
class Departement(models.Model):

	nom = models.CharField(max_length=50,unique=True, verbose_name="Nom du département")
	class Meta:

		ordering = ('nom',)

	def __str__(self):
		return self.nom


# ----------------------------------------------------------------------
class Service(models.Model):

	nom = models.CharField(max_length=50,unique=True, verbose_name="Nom du Service")

	class Meta:

		ordering = ('nom',)

	def __str__(self):
		return self.nom