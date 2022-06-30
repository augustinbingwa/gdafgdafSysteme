from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from mod_crm.models import Contribuable
from mod_parametrage.models import *
from mod_parametrage.enums import *

from mod_finance.models import Taxe

from mod_activite.models import *
from mod_activite.submodels.model_allocation_espace_publique import *
from mod_activite.submodels.model_allocation_place_marche import *

from mod_helpers.hlp_paths import PathsHelpers

from decimal import Decimal

#-------------------------------------------------------------
class BaseActivite(models.Model):
	"""
	Modele Base activité
	"""
	# Numéro chronologique de l'activité
	numero_activite  = models.CharField(max_length=30, unique=True)

	# Coût de l'activité carte professionnelle : (Note d’imposition)
	taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE,
		related_name='%(class)s_requests_taxe_ai_cout_activite', verbose_name="Coût de l'activité (NOTE)")
	
	# Coût de la carte professionnelle : (Avis d’imposition)
	ai_cout_carte = models.ForeignKey(Taxe, on_delete=models.CASCADE,
		related_name='%(class)s_requests_taxe_ai_cout_carte', verbose_name="Coût de la carte professionnelle (AVIS)")

	# Date début de l'activité
	date_debut = models.DateField()

	# Date fin de l'activité (Mis à jour à partir de l'arrêt service de l'activité)
	date_fin = models.DateField(blank=True, null=True)
	
	# Solde de départ (montant des arrierés)
	solde_depart = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])
	
	# Si activité est active ou non
	actif = models.BooleanField(blank=True, default=True)

	#--------------------------------------------------------
	# --------------- CONTROLE D'IMPRESSION -----------------
	#--------------------------------------------------------
	# Numero de la carte physique à resaisir au moment de l'impression pour controler l'authenticité de la carte
	numero_carte_physique = models.CharField(max_length=10, blank=True, null=True)
	
	# Nombre d'impressions (Voir global_variables (PRINT, MAX_NUMBER))
	nombre_impression = models.PositiveSmallIntegerField(default=0)

	#--------------------------------------------------------
	# ----------------- TRAÇABILITÉ -------------------------
	#--------------------------------------------------------
	date_create = models.DateTimeField(auto_now_add=True)
	date_update = models.DateTimeField(null=True)
	date_validate = models.DateTimeField(null=True)
	date_print = models.DateTimeField(null=True)
	
	user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
	user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_updated', null=True)
	user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_validate',null=True)
	user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_print', null=True)
	
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

	# -------------------------------------------------------
	# Ecriture des AI et NI
	date_ecriture = models.DateTimeField(null=True)

	user_ecriture = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
									related_name='%(class)s_requests_ecriture', null=True)
	
	@property
	def is_ecriture_valid(self):
		"""
		Si l'écriture a été générée (validée)
		"""
		return self.date_ecriture and self.user_ecriture

	# Si déjà imprimé
	@property
	def is_printed(self):
		if self.nombre_impression>0 and self.date_print is not None and self.user_print is not None:
			return True

		return False

	class Meta:
		ordering = ('-id', )

	def __str__(self):
		return self.numero_activite

	def class_name(self):
		"""utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
		return self.__module__ + '.'+  self.__class__.__name__

#--------------------------------------------------------------------

def path_fichier_activite_standard_autorisation(instance, filename):
	"""
	Parametrage du path de l'autorisation de transport
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.ACTIVITE_STANDARD_AUTORISATION_FOLDER)

#--------------------------------------------------------------------
class Standard(BaseActivite):	
	"""
	Modèle Activité  Standard/Ordinnaire
	"""
	# Identifiant du contribuable
	contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE)
	
	# Adresse de l'activité qui est null si type_espace = publique, Non null si Type_espace=Privé
	adresse = models.ForeignKey(Quartier, on_delete=models.CASCADE)

	# Numero de rue/avenue
	numero_rueavenue = models.ForeignKey(RueOuAvenue, on_delete=models.CASCADE) 

	# Numéro de police privée  'facultatif)'
	numero_police = models.CharField(max_length=15, blank=True, null=True)
	
	# Fichier d'autorisation de transport venant du Ministère de Commerce
	fichier_autorisation = models.FileField(upload_to=path_fichier_activite_standard_autorisation, max_length=255, null=True, blank=True)

	# Type de l'espace (Publique ou Privé), Si Publique alors seléctionner l'objet 'allocation espace publique' 
	# Par défaut l'activit est en mode privé
	type_espace = models.IntegerField(choices=choix_espace, default=PRIVE) 

	# Affecter l'allocation d'espace publique si le Type_espace = Publique
	allocation_espace_publique = models.ForeignKey(AllocationEspacePublique, on_delete=models.CASCADE, blank=True, null=True) 
		
	def __str__(self):
		return self.numero_activite

	def view_list_name(self):
		"""utilisé pour la note"""
		return 'activite_standard_list'

#--------------------------------------------------------------------
class Marche(BaseActivite):
	"""
	Modele Activité dans le marché
	"""
	# Information de l'allocation de la place dans le marché
	allocation_place_marche = models.ForeignKey(AllocationPlaceMarche, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.numero_activite

	def view_list_name(self):
		"""utilisé pour la note"""
		return 'activite_marche_list'