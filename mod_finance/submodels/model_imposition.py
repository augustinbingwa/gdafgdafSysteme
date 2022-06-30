from django.db import models
from django.conf import settings  # authetification user model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from mod_finance.submodels.model_taxe import *

from mod_crm.models import Contribuable

from mod_helpers.hlp_paths import PathsHelpers

from mod_parametrage.enums import *

from decimal import Decimal

import datetime

import pytz


# ----------------------------------------------------------------------------
# ------------------------ GESTION DES AVIS D' IMPOSITION --------------------
# ----------------------------------------------------------------------------

def path_bordereau_ai_file(instance, filename):
    """
	Path de l'avis d'imposition (fichier importé) ou bordereau de paiement
	"""
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.BORDEREAU_AI_FOLDER)

def path_update_ni_info_file(instance, filename):
	"""
	Path de l'avis d'imposition (fichier importé) ou bordereau de paiement
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.UPDATE_NI_INFORMATION)

class AvisImposition(models.Model):
    """
	Modele Avis d'imposition
	"""
    # Référence de l'avis d'imposition (chronologique)
    reference = models.CharField(max_length=25, blank=False, unique=True)

    # Nom du démandeur
    nom = models.CharField(max_length=100, blank=True, null=True, default='')

    # Contribuable (Ceci évite de chercher le contribuable dans l'entity qui risque d'alourdir la requette)
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE, blank=True, null=True)

    # Parametre taxe (type de document démandé)
    taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

    # Parametre montant taxe
    taxe_montant = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))])

    # Nombre de copies
    nombre_copie = models.PositiveSmallIntegerField(default=1)

    # Formule Montant_total = taxe_montant * nombre_copie
    montant_total = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))])

    # Validité de la demande (en jours)
    validite = models.PositiveSmallIntegerField(default=1)  # delai de validité de la demande

    # ------------------------------------------------------
    # Référence de l'Entity Modèle (voir parametrage.enum)
    entity = models.PositiveSmallIntegerField(choices=choix_entity_imposition, null=True)

    # Identifiant de l'entity
    entity_id = models.IntegerField(null=True)
    # ------------------------------------------------------

    # Libellé de l'avis (Par défaut = libellé de la taxe)
    libelle = models.TextField(max_length=512, blank=False)
    """
	Paiement (Mise à jour après a cr"ation de l'avis)
	Mis à jour après la création de l'objet.
	"""
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, null=True)  # Banque ou Mobile Money'

    # Référence de paiement (numéro du boredereau) (UNIQUE pour chaque agence)
    ref_paiement = models.CharField(max_length=15, null=True)
    date_paiement = models.DateTimeField(null=True)

    """
	Mis a jour après paiement 
	"""
    fichier_paiement = models.FileField(upload_to=path_bordereau_ai_file, null=True)  # le scan du bordereau de paiement

    # --------------------------------------------------------
    # ----------------- TRAÇABILITÉ -------------------------
    # --------------------------------------------------------
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)  # Mis à jour à chaque modification
    date_validate = models.DateTimeField(null=True)  # Mis à jour à partir du rapprochement
    date_print = models.DateTimeField(null=True)  # Mise à jour après impression

    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_created')
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_updated', null=True)
    user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='%(class)s_requests_validate', null=True)
    user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='%(class)s_requests_print', null=True)

    # -------------------------------------------------------
    # ------------------- NOTE ET REPONSE -------------------
    # -------------------------------------------------------
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

    # Si le payement est effectué totalement
    @property
    def is_payed(self):
        return (
                           self.montant_total == self.taxe_montant) and self.ref_paiement and self.date_paiement and self.fichier_paiement and self.agence

    class Meta:
        # 'agence', 'ref_paiement' doivent être 'UNIQUE'
        index_together = unique_together = [['agence', 'ref_paiement']]

        ordering = ('-id',)

    def __str__(self):
        return self.reference

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.' + self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'avis_imposition_list'

# ----------------------------------------------------------------------------
# ----------------------- GESTION DES NOTES D' IMPOSITION --------------------
# ----------------------------------------------------------------------------

def path_bordereau_ni_file(instance, filename):
    """
	Path des bordereaux (fichier importé)
	"""
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.BORDEREAU_NI_FOLDER)

def path_bordereau_ni_file_externe(instance, filename):
    """
	Path des  bordereaux (fichier importé)
	"""
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.BORDEREAU_NI_FOLDER_EXTERNE)

class NoteImposition(models.Model):
    """
	Modele Note d'imposition :
	Ce modèle correspond à un modèle de facture qui sera imprimée sous forme d'une quittance.
	Chaque note d'imposition fait l'objet d'un paiement d'une taxe sur activité.
	"""
    # Référence de la note d'imposition (chronologique)
    reference = models.CharField(max_length=25, blank=False, unique=True)  # Référence de la note d'imposition

    # Contribuable (Ceci évite de chercher le contribuable dans l'entity qui risque d'alourdir la requette)
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE, null=True)

    # ------------------------------------------------------
    # Référence de l'Entity Modèle (voir parametrage.enum)
    entity = models.PositiveSmallIntegerField(choices=choix_entity_imposition, null=True)

    # Identifiant de l'entity
    entity_id = models.IntegerField(null=True)
    # ------------------------------------------------------

    # Période de paiement
    periode = models.ForeignKey(Periode, on_delete=models.CASCADE)

    # Année de paiement (Très important pour la gestion des périodes)
    annee = models.PositiveSmallIntegerField(
        default=timezone.now().year,
        validators=[
            MinValueValidator(2014),
            MaxValueValidator(9999)
        ]
    )

    # Libellé de la note (Par défaut = libellé de la taxe)
    libelle = models.TextField(max_length=1024, blank=False)

    # Taxe à payer (parametre taxe). Pour les activités, les taxes sont parametrées donc il suffit de les référencer ici
    taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

    # Montant total de la taxe (parametre taxe)
    taxe_montant = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))])

    # Montant payé (Mis à jour à partir du modèle NoteImpositionPaiement) qui est le Montant total de la taxe (parametre)
    # Cette technique permet facilement de voir le statut de paiement d'une note (payé, payé partiellement, etc. )
    taxe_montant_paye = models.DecimalField(decimal_places=2, max_digits=10,validators=[MinValueValidator(Decimal('0'))], default=0)
    montant_taxe = models.DecimalField(decimal_places=0, max_digits=10, validators=[MinValueValidator(Decimal('0'))],default=0)
    montant_restant = models.DecimalField(decimal_places=0, max_digits=10, validators=[MinValueValidator(Decimal('0'))],default=0)
    montant_penalite = models.DecimalField(decimal_places=0, max_digits=10,validators=[MinValueValidator(Decimal('0'))], default=0)

    etat = models.BooleanField(default=True)

    # Si le payement est effectué totalement
    @property
    def is_payed(self):
        return (self.taxe_montant == self.taxe_montant_paye) and (
                    self.taxe_montant_paye > 0) and self.date_validate and self.user_validate

    # --------------------------------------------------------
    # --------------- CONTROLE D'IMPRESSION -----------------
    # --------------------------------------------------------
    # Numero de la carte physique à resaisir au moment de l'impression pour controler l'authenticité de la carte
    numero_carte_physique = models.CharField(max_length=10, blank=True, null=True)

    # Nombre d'impressions (Voir global_variables (PRINT, MAX_NUMBER))
    nombre_impression = models.PositiveSmallIntegerField(default=0)

    # --------------------------------------------------------
    # ----------------- TRAÇABILITÉ -------------------------
    # --------------------------------------------------------
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)
    date_validate = models.DateTimeField(null=True)  # Mise à jour si tous les paiemens sont effectués (sans rapprochement)
    date_print = models.DateTimeField(null=True)  # Mise à jour après impression
    date_penalite = models.DateField(null=True)  # Mise à jour de la date de penalite

    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_updated', null=True)
    user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_validate', null=True)
    user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_print', null=True)
    user_penalite = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_penalite', null=True)

    # Si la note est validée
    @property
    def is_valid(self):
        return self.date_validate and self.user_validate

    # -------------------------------------------------------
    # - TRACABILITE DE LA SUPPRESSION DE LA NOTE D'IMPOSION -
    # -------------------------------------------------------
    date_delete = models.DateTimeField(null=True)
    user_delete = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_delete', null=True)
    motif_delete = models.TextField(max_length=1024, blank=True, null=True)

    @property
    def is_deleted(self):
        """
		Si la note est supprimée
		"""
        return self.date_delete and self.user_delete

    # -------------------------------------------------------
    # ------------------- PAIEMENT EXTERNE-------------------
    # -------------------------------------------------------
    # Certaines notes sont payée à l'exterieur de la mairie même (cas des transports municipaux)
    # le scan du bordereau de paiement externe (ou autre preuve de paiement)
    paiement_externe_file = models.FileField(upload_to=path_bordereau_ni_file_externe, null=True)

    @property
    def is_payed_externe(self):
        """
		Si la note est supprimée
		"""
        return (self.taxe_montant == self.taxe_montant_paye == 0) and self.date_validate and self.user_validate \
               and self.entity == ENTITY_VEHICULE_ACTIVITE

    class Meta:
        ordering = ('-id',)

        # 'entity', 'entity_id', 'periode', 'annee' doivent être 'UNIQUE'
        index_together = unique_together = [['entity', 'entity_id', 'periode', 'annee']]

    def __int__(self):
        return self.id

    def __str__(self):
        return self.reference

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.' + self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'note_imposition'

class AvisImpositionPaiement(models.Model):
	"""
	Modele Suivi de Paiement des Notes d'imposition
	"""
	avis_imposition = models.ForeignKey(AvisImposition, on_delete=models.CASCADE)

	"""
	Ce modèle permet de suivre les tranches de paiement d'une note d'imposition.
	La note d'imposition pourrait être payé partiellement (en plusieurs tranches de paiement)
	"""
	agence = models.ForeignKey(Agence, on_delete=models.CASCADE)  # Banque ou Mobile Money'
	ref_paiement = models.CharField(max_length=20)  # référence de paiement (ref boredereau)
	date_paiement = models.DateTimeField()

	# Montant tranche payé
	montant = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))])

	# Montant excedant = montant à rajouter au prochain paiement
	montant_excedant = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))], default=0)

	# Mis a jour après paiement (UNIQUE pour chaque agence)
	fichier_paiement = models.FileField(upload_to=path_bordereau_ni_file, null=True)  # le scan du bordereau de paiement

	# -------------------------------------------------------
	# ------------------- NOTE ET REPONSE -------------------
	# -------------------------------------------------------
	# Note envoyée par un autre user ou lui même
	note = models.CharField(max_length=255, blank=True, null=True)
	user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_note', null=True)
	date_note = models.DateTimeField(null=True)

	# Réponse de la note par l'user de création
	reponse_note = models.CharField(max_length=255, blank=True, null=True)

	# Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
	demande_annulation_validation = models.BooleanField(default=False)

	# Traçabilité de l'annulation
	date_cancel = models.DateTimeField(null=True)
	user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_cancel', null=True)

	# Traçabilité
	date_create = models.DateTimeField(auto_now_add=True)
	date_update = models.DateTimeField(null=True)
	date_validate = models.DateTimeField(null=True)  # Mise à jour à partir du rapprochement (rapproché = validé)

	user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
	user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_updated', null=True)
	user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_validate', null=True)

	class Meta:
		# 'agence', 'ref_paiement' doivent être 'UNIQUE'
		index_together = unique_together = [['agence', 'ref_paiement']]

		ordering = ('-id',)

	def __str__(self):
		return self.ref_paiement

	def class_name(self):
		"""utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
		return self.__module__ + '.' + self.__class__.__name__

	def view_list_name(self):
		"""utilisé pour la avis"""
		return 'avis_imposition_paiement_list'

class NoteImpositionPaiement(models.Model):
	"""
	Modele Suivi de Paiement des Notes d'imposition
	"""
	note_imposition = models.ForeignKey(NoteImposition, on_delete=models.CASCADE)

	"""
	Ce modèle permet de suivre les tranches de paiement d'une note d'imposition.
	La note d'imposition pourrait être payé partiellement (en plusieurs tranches de paiement)
	"""
	agence = models.ForeignKey(Agence, on_delete=models.CASCADE)  # Banque ou Mobile Money'
	ref_paiement = models.CharField(max_length=20)  # référence de paiement (ref boredereau)
	date_paiement = models.DateTimeField()

	# Montant tranche payé
	montant_tranche = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))])

	# Montant excedant = montant à rajouter au prochain paiement
	montant_excedant = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))], default=0)

	# Mis a jour après paiement (UNIQUE pour chaque agence)
	fichier_paiement = models.FileField(upload_to=path_bordereau_ni_file, null=True)  # le scan du bordereau de paiement

	# -------------------------------------------------------
	# ------------------- NOTE ET REPONSE -------------------
	# -------------------------------------------------------
	# Note envoyée par un autre user ou lui même
	note = models.CharField(max_length=255, blank=True, null=True)
	user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_note', null=True)
	date_note = models.DateTimeField(null=True)

	# Réponse de la note par l'user de création
	reponse_note = models.CharField(max_length=255, blank=True, null=True)

	# Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
	demande_annulation_validation = models.BooleanField(default=False)

	# Traçabilité de l'annulation
	date_cancel = models.DateTimeField(null=True)
	user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_cancel', null=True)

	# Traçabilité
	date_create = models.DateTimeField(auto_now_add=True)
	date_update = models.DateTimeField(null=True)
	date_validate = models.DateTimeField(null=True)  # Mise à jour à partir du rapprochement (rapproché = validé)

	user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
	user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_updated', null=True)
	user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_validate', null=True)

	class Meta:
		# 'agence', 'ref_paiement' doivent être 'UNIQUE'
		index_together = unique_together = [['agence', 'ref_paiement']]

		ordering = ('-id',)

	def __str__(self):
		return self.ref_paiement

	def class_name(self):
		"""utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
		return self.__module__ + '.' + self.__class__.__name__

	def view_list_name(self):
		"""utilisé pour la note"""
		return 'note_imposition_paiement_list'

class NoteImpositionDelete(models.Model):
	"""
	Modele Note d'imposition :
	Ce modèle correspond à un modèle de facture qui sera imprimée sous forme d'une quittance.
	Chaque note d'imposition fait l'objet d'un paiement d'une taxe sur activité.
	"""
	# Référence de la note d'imposition (chronologique)
	reference = models.CharField(max_length=25, blank=False, unique=True)  # Référence de la note d'imposition

	# Contribuable (Ceci évite de chercher le contribuable dans l'entity qui risque d'alourdir la requette)
	contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE, null=True)

	# ------------------------------------------------------
	# Référence de l'Entity Modèle (voir parametrage.enum)
	entity = models.PositiveSmallIntegerField(choices=choix_entity_imposition, null=True)

	# Identifiant de l'entity
	entity_id = models.IntegerField(null=True)
	# ------------------------------------------------------

	# Période de paiement
	periode = models.ForeignKey(Periode, on_delete=models.CASCADE)

	# Année de paiement (Très important pour la gestion des périodes)
	annee = models.PositiveSmallIntegerField(
		default=timezone.now().year,
		validators=[
			MinValueValidator(2014),
			MaxValueValidator(9999)
		]
	)

	# Libellé de la note (Par défaut = libellé de la taxe)
	libelle = models.TextField(max_length=1024, blank=False)

	# Taxe à payer (parametre taxe). Pour les activités, les taxes sont parametrées donc il suffit de les référencer ici
	taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

	# Montant total de la taxe (parametre taxe)
	taxe_montant = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0'))])

	# Montant payé (Mis à jour à partir du modèle NoteImpositionPaiement) qui est le Montant total de la taxe (parametre)
	# Cette technique permet facilement de voir le statut de paiement d'une note (payé, payé partiellement, etc. )
	taxe_montant_paye = models.DecimalField(decimal_places=2, max_digits=10,validators=[MinValueValidator(Decimal('0'))], default=0.00)

	etat = models.BooleanField(default=True)

	# Si le payement est effectué totalement
	@property
	def is_payed(self):
		return (self.taxe_montant == self.taxe_montant_paye) and (
					self.taxe_montant_paye > 0) and self.date_validate and self.user_validate

	# --------------------------------------------------------
	# --------------- CONTROLE D'IMPRESSION -----------------
	# --------------------------------------------------------
	# Numero de la carte physique à resaisir au moment de l'impression pour controler l'authenticité de la carte
	numero_carte_physique = models.CharField(max_length=10, blank=True, null=True)

	# Nombre d'impressions (Voir global_variables (PRINT, MAX_NUMBER))
	nombre_impression = models.PositiveSmallIntegerField(default=0)

	# --------------------------------------------------------
	# ----------------- TRAÇABILITÉ -------------------------
	# --------------------------------------------------------
	date_create = models.DateTimeField(auto_now_add=True)
	date_update = models.DateTimeField(null=True)
	date_validate = models.DateTimeField(
		null=True)  # Mise à jour si tous les paiemens sont effectués (sans rapprochement)
	date_print = models.DateTimeField(null=True)  # Mise à jour après impression

	user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_created')
	user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_updated', null=True)
	user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_validate', null=True)
	user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_print', null=True)

	# Si la note est validée
	@property
	def is_valid(self):
		return self.date_validate and self.user_validate

	# -------------------------------------------------------
	# - TRACABILITE DE LA SUPPRESSION DE LA NOTE D'IMPOSION -
	# -------------------------------------------------------
	date_delete = models.DateTimeField(null=True)
	user_delete = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_requests_delete', null=True)
	motif_delete = models.TextField(max_length=1024, blank=True, null=True)

	@property
	def is_deleted(self):
		"""
		Si la note est supprimée
		"""
		return self.date_delete and self.user_delete

	# -------------------------------------------------------
	# ------------------- PAIEMENT EXTERNE-------------------
	# -------------------------------------------------------
	# Certaines notes sont payée à l'exterieur de la mairie même (cas des transports municipaux)
	# le scan du bordereau de paiement externe (ou autre preuve de paiement)
	paiement_externe_file = models.FileField(upload_to=path_bordereau_ni_file_externe, null=True)

	@property
	def is_payed_externe(self):
		"""
		Si la note est supprimée
		"""
		return (self.taxe_montant == self.taxe_montant_paye == 0) and self.date_validate and self.user_validate \
			   and self.entity == ENTITY_VEHICULE_ACTIVITE

	class Meta:
		ordering = ('-id',)
		# 'entity', 'entity_id', 'periode', 'annee' doivent être 'UNIQUE'
		index_together = unique_together = [['entity', 'entity_id', 'periode', 'annee']]

	def __str__(self):
		return self.reference

	def class_name(self):
		"""utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
		return self.__module__ + '.' + self.__class__.__name__

	def view_list_name(self):
		"""utilisé pour la note"""
		return 'note_imposition'

class UpdateFileUpload(models.Model):
	update_file_info = models.FileField(upload_to=path_update_ni_info_file, null=True)
	nbr_update = models.IntegerField(null=True)
	ni_id = models.IntegerField(null=True)
	status = models.IntegerField(default=0)
	commentaire = models.TextField(null=True)

	class Meta:
		ordering = ('-id',)

	def __int__(self):
		return self.id