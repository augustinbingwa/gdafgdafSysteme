from django.conf import settings #authetification user model
from django.db import models

from mod_parametrage.models import Quartier, RueOuAvenue
from mod_parametrage.enums import *
from mod_helpers.hlp_paths import PathsHelpers

import datetime

#------------------------------------------------------------
#---------------------- MODELES PARAMETRAGE -----------------
#------------------------------------------------------------

def path_photo(instance, filename):
	"""
	Path photo d'identité
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.PHOTO_FOLDER)

#------------------------------------------------------------
def path_identite_file(instance, filename):
	"""
	Path scan de d'identité (CNI/Passeport)
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.IDENTITE_FOLDER)

#------------------------------------------------------------
def path_nif_file(instance, filename):
	"""
	Path scan du NIF
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.NIF_FOLDER)

#------------------------------------------------------------
def path_rc_file(instance, filename):
	"""
	Path scan du registre du commerce
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.RC_FOLDER)	

#------------------------------------------------------------
class Contribuable(models.Model):
	"""
	Modele Contribuable. Classe parent
	"""
	matricule = models.CharField(max_length=17, unique=True)
	nom = models.CharField(max_length=100)
	
	# Adresse précise (Commune - Zone - Quartier)
	# Physique : adresse de domicile
	# Morale : adresse du siège
	adresse = models.ForeignKey(Quartier, on_delete=models.CASCADE, blank=True, null=True)

	# Adresse exacte
	# Physique : adresse domicile (locale ou étrangère)
	# Morale : siège (locale)
	adresse_exacte = models.CharField(max_length=255, blank=True, null=True)

	numero_rueavenue = models.ForeignKey(RueOuAvenue, on_delete=models.CASCADE, blank=True, null=True)
	numero_police = models.CharField(max_length=15, blank=True, null=True)

	code_postal = models.CharField(max_length=5, blank=True, null=True)
	tel = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=70, blank=True, null=True)
	
	# numero NIF
	nif_numero = models.CharField(max_length=15, blank=True, null=True)

	# Repertoire d'upload du NIF
	nif_file = models.FileField(upload_to=path_nif_file, max_length=255, null=True, blank=True) 

	# Traçabilité
	date_create = models.DateTimeField(auto_now_add=True)
	date_update = models.DateTimeField(null=True)	
	date_validate = models.DateTimeField(null=True)
	
	user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		related_name='%(class)s_requests_created')
	user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		related_name='%(class)s_requests_updated', null=True)
	user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		related_name='%(class)s_requests_validate', null=True)

	#-------------------------------------------------------
	#------------------- NOTE ET REPONSE -------------------
	#-------------------------------------------------------
	# Note envoyée par un autre user ou lui même
	note = models.CharField(max_length=255, blank=True, null=True)
	user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
		related_name='%(class)s_requests_note', null=True)
	date_note = models.DateTimeField(null=True)

	# Réponse de la note par l'user de création
	reponse_note = models.CharField(max_length=255, blank=True, null=True)

	# Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
	demande_annulation_validation = models.BooleanField(default=False)

	# Traçabilité de l'annulation
	date_cancel = models.DateTimeField(null=True)
	user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
		related_name='%(class)s_requests_cancel', null=True)

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.matricule + ' - ' + self.nom

	def class_name(self):
		"""utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
		return self.__module__ + '.'+  self.__class__.__name__

#------------------------------------------------------------
class PersonnePhysique(Contribuable):
	"""
	Modele Contribuable. Classe Personne physique
	Code '0', Voir Chrono
	"""	
	sexe = models.IntegerField(choices=choix_sexe)
	
	date_naiss = models.DateField()
	
	lieu_naiss = models.CharField(max_length=250)
	
	identite = models.IntegerField(choices=choix_identite)
	
	identite_numero = models.CharField(max_length=50, unique=True)
	
	#repertoire d'upload,
	identite_file =  models.FileField(upload_to=path_identite_file, max_length=255, null=True, blank=True)
	
	#repertoire d'upload,
	photo_file = models.FileField(upload_to=path_photo, max_length=255, null=True, blank=True)

	def __str__(self):
		return super().__str__()

	def view_list_name(self):
		"""utilisé pour la note"""
		return 'physique_list'
	
#------------------------------------------------------------
class PersonneMorale(Contribuable):
	"""
	Modele Contribuable. Classe Personne Morale
	Code 1
	"""
	# Type caractère, 'à caractère COMMERCIAL = 0' ou 'sans but LUCRATIF = 1'
	# Par défaut : à carctère commecial
	type_caractere = models.IntegerField(choices=choix_caractere, default=COMMERCIAL)
	
	# Optinnel pour le type_caractere = LUCRATIF
	rc_numero = models.CharField(max_length=50, blank=True)

	# Repertoire d'upload,
	rc_file = models.FileField(upload_to=path_rc_file, max_length=255, null=True, blank=True) 

	def __str__(self):
		return super().__str__()

	def view_list_name(self):
		"""utilisé pour la note"""
		return 'morale_list'