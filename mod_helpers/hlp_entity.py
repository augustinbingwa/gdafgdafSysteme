from .models import *

from mod_activite.models import *
from mod_foncier.models import *
from mod_transport.models import *
from mod_finance.models import NoteImposition

from mod_parametrage.enums import *


class EntityHelpers:
    """
    ENTITY_ACTIVITE_STANDARD = 1				# BaseActivite (réf: Standard)
    ENTITY_ACTIVITE_MARCHE = 2					# BaseActivite (réf: Marché)
    ENTITY_ACTIVITE_EXCEPTIONNELLE = 3			# ActiviteExceptionnel (Dans AvisImposition uniquement)
    ENTITY_VISITE_SITE_TOURISTIQUE = 4			# VisiteSiteTouristique (Dans AvisImposition uniquement)
    ENTITY_ALLOCATION_ESPACE_PUBLIQUE = 5		# AllocationEspacePublique
    ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE = 6	# AllocationPanneauPublicitaire
    ENTITY_PUBLICITE_MUR_CLOTURE = 7			# PubliciteMurCloture
    ENTITY_ALLOCATION_PLACE_MARCHE = 8			# Allocation de Place dans le Marche
    ENTITY_BATIMENTS_MUNICIPAUX = 9				# ??????????????????
    ENTITY_IMPOT_FONCIER = 10					# Impôt foncier (FoncierExpertise)
    ENTITY_VEHICULE_ACTIVITE = 11				# VehiculeActivite
    ENTITY_DROIT_STATIONNEMENT = 12				# VehiculeActivite (!!! Important !!!) : Il depend de l'activité
    ENTITY_VEHICULE_PROPRIETE = 13				# VehiculeProprietaire
    ENTITY_ACTIVITE_STANDARD_DUPLICATA = 14     # StandardDuplicata (Dans AvisImposition uniquement)
    ENTITY_ACTIVITE_MARCHE_DUPLICATA = 15       # MarcheDuplicata (Dans AvisImposition uniquement)
    ENTITY_VEHICULE_ACTIVITE_DUPLICATA = 16		# VehiculeActiviteDuplicata (Dans AvisImposition uniquement)
    ENTITY_VEHICULE_PROPRIETE_DUPLICATA = 17	# VehiculeProprietaireDuplicata (Dans AvisImposition uniquement)
    """

    def get_entity_class_name(obj):
        if obj:
            return obj.__class__.__name__

        return None

    def get_entity(obj):
        if isinstance(obj, Standard):
            return ENTITY_ACTIVITE_STANDARD

        elif isinstance(obj, Marche):
            return ENTITY_ACTIVITE_MARCHE

        elif isinstance(obj, ActiviteExceptionnelle):
            return ENTITY_ACTIVITE_EXCEPTIONNELLE

        elif isinstance(obj, VisiteSiteTouristique):
            return ENTITY_VISITE_SITE_TOURISTIQUE

        elif isinstance(obj, AllocationEspacePublique):
            return ENTITY_ALLOCATION_ESPACE_PUBLIQUE

        elif isinstance(obj, AllocationPanneauPublicitaire):
            return ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE

        elif isinstance(obj, PubliciteMurCloture):
            return ENTITY_PUBLICITE_MUR_CLOTURE

        elif isinstance(obj, AllocationPlaceMarche):
            return ENTITY_ALLOCATION_PLACE_MARCHE

        elif isinstance(obj, FoncierExpertise):
            return ENTITY_IMPOT_FONCIER

        elif isinstance(obj, VehiculeActivite):
            return ENTITY_VEHICULE_ACTIVITE

        elif isinstance(obj, VehiculeActivite):
            return ENTITY_DROIT_STATIONNEMENT

        elif isinstance(obj, VehiculeProprietaire):
            return ENTITY_VEHICULE_PROPRIETE

            """
			elif isinstance(obj, ????):
				return ENTITY_ACTIVITE_STANDARD_DUPLICATA
			elif isinstance(obj, ????):
				return ENTITY_ACTIVITE_MARCHE_DUPLICATA
			"""

        elif isinstance(obj, VehiculeActiviteDuplicata):
            return ENTITY_VEHICULE_ACTIVITE_DUPLICATA

        elif isinstance(obj, VehiculeProprietaireDuplicata):
            return ENTITY_VEHICULE_PROPRIETE_DUPLICATA

        return 0

    def get_last_note_imposition(obj):
        """
        Renvoie la dernière note d'imposition de l'objet en cours
        """
        entity = EntityHelpers.get_entity(obj)
        note = NoteImposition.objects.filter(entity=entity, entity_id=obj.id).order_by(
            "-id"
        )
        if note:
            note = note.first()

        return note

    def get_last_note_imposition_stationnement(obj):
        """
        Renvoie la dernière note d'imposition de l'objet en cours spécifiquement pour les droits de stationnement
        """
        entity = ENTITY_DROIT_STATIONNEMENT
        note = NoteImposition.objects.filter(entity=entity, entity_id=obj.id).order_by(
            "-id"
        )
        if note:
            note = note.first()

        return note
