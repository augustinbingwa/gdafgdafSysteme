from mod_parametrage import enums
from mod_helpers.hlp_entity import EntityHelpers
from mod_finance.models import NoteImposition, AvisImposition

from mod_transport.models import VehiculeActivite, VehiculeProprietaire
from mod_activite.models import (
    Standard,
    Marche,
    AllocationEspacePublique,
    AllocationPlaceMarche,
    AllocationPanneauPublicitaire,
    PubliciteMurCloture,
)
from mod_transport.models import VehiculeProprietaire, VehiculeActivite
from mod_foncier.models import FoncierExpertise

# from gdaf import models


def get_ni_title(obj):
    res = "Note d'imposition pour "
    if isinstance(obj, NoteImposition) :
        if obj.entity == enums.ENTITY_ACTIVITE_STANDARD:
            res += "Activité Standard"
        elif obj.entity == enums.ENTITY_ACTIVITE_MARCHE:
            res += "Activité dans le marché"
        elif obj.entity == enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
            res += "Allocation de l'espace public"
        elif obj.entity == enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
            res += "Allocation du panneau publicitaire"
        elif obj.entity == enums.ENTITY_PUBLICITE_MUR_CLOTURE:
            o = PubliciteMurCloture.objects.get(id=obj.entity_id)
            if o:
                type_publicite = ""
                if o.type_publicite == enums.MUR:
                    type_publicite = " le mur"
                else:
                    type_publicite = " la clôture"
                res += "Publicité sur " + type_publicite
        elif obj.entity == enums.ENTITY_ALLOCATION_PLACE_MARCHE:
            res += "Allocation de place dans le marché"
        elif obj.entity == enums.ENTITY_VEHICULE_ACTIVITE:
            res += "Carte municipale de transport"
        elif obj.entity == enums.ENTITY_DROIT_STATIONNEMENT:
            res += "Droit de stationnement"
        elif obj.entity == enums.ENTITY_VEHICULE_PROPRIETE:
            res += "Carte de propriété"
        elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
            res += "Impôt Foncie"

    res = res.lower().capitalize()

    # res += "<br><span class='is-muted'>Réf-%s</span>" % obj.reference

    return res

def get_ai_title(obj):
    res = "Avis d'imposition pour "
    if isinstance(obj, AvisImposition):
        print(obj.entity)
        if obj.entity == enums.ENTITY_ACTIVITE_STANDARD:
            res += "Activité Standard"
        elif obj.entity == enums.ENTITY_ACTIVITE_MARCHE:
            res += "Activité dans le marché"
        elif obj.entity == enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
            res += "Allocation de l'espace public"
        elif obj.entity == enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
            res += "Allocation du panneau publicitaire"
        elif obj.entity == enums.ENTITY_PUBLICITE_MUR_CLOTURE:
            o = PubliciteMurCloture.objects.get(id=obj.entity_id)
            if o:
                type_publicite = ""
                if o.type_publicite == enums.MUR:
                    type_publicite = " le mur"
                else:
                    type_publicite = " la clôture"
                res += "Publicité sur " + type_publicite
        elif obj.entity == enums.ENTITY_ALLOCATION_PLACE_MARCHE:
            res += "Allocation de place dans le marché"
        elif obj.entity == enums.ENTITY_VEHICULE_ACTIVITE:
            res += "Carte municipale de transport"
        elif obj.entity == enums.ENTITY_DROIT_STATIONNEMENT:
            res += "Droit de stationnement"
        elif obj.entity == enums.ENTITY_VEHICULE_PROPRIETE:
            res += "Carte de propriété"
        elif obj.entity == enums.ENTITY_VISITE_SITE_TOURISTIQUE:
            res += "Visite Site Touristique"
        elif obj.entity == enums.ENTITY_ATTESTATION:
            res += "Attestaion"
        elif obj.entity == enums.ENTITY_ACTE:
            res += "Acte"

    res = res.lower().capitalize()

    # res += "<br><span class='is-muted'>Réf-%s</span>" % obj.reference

    return res

def get_libelle_note_imposition(obj):
    """
    Renvoyer le libellé de la note d'imposition virtuellement
    """
    res = ""
    if isinstance(obj, NoteImposition):
        if obj.entity == enums.ENTITY_ACTIVITE_STANDARD:
            o = Standard.objects.get(id=obj.entity_id)
            if o:
                res = (
                    "Activité Standard n°"
                    + o.numero_activite
                    + ", "
                    + o.taxe.libelle.capitalize()
                )
        elif obj.entity == enums.ENTITY_ACTIVITE_MARCHE:
            o = Marche.objects.get(id=obj.entity_id)
            if o:
                res = (
                    "Activité dans le marché n°"
                    + o.numero_activite
                    + " de "
                    + o.allocation_place_marche.droit_place_marche.nom_marche.nom
                    + ", place n°"
                    + o.allocation_place_marche.droit_place_marche.numero_place
                    + " ("
                    + o.taxe.libelle.capitalize()
                    + ")"
                )
        elif obj.entity == enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
            o = AllocationEspacePublique.objects.get(id=obj.entity_id)
            if o:
                res = "Allocation de l'espace public n°" + o.numero_allocation
        elif obj.entity == enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
            o = AllocationPanneauPublicitaire.objects.get(id=obj.entity_id)
            if o:
                res = "Allocation du panneau publicitaire n°" + o.numero_allocation
        elif obj.entity == enums.ENTITY_PUBLICITE_MUR_CLOTURE:
            o = PubliciteMurCloture.objects.get(id=obj.entity_id)
            if o:
                type_publicite = ""
                if o.type_publicite == enums.MUR:
                    type_publicite = " le mur"
                else:
                    type_publicite = " la clôture"
                res = "Publicité sur " + type_publicite + " n°" + o.numero_allocation
        elif obj.entity == enums.ENTITY_ALLOCATION_PLACE_MARCHE:
            o = AllocationPlaceMarche.objects.get(id=obj.entity_id)
            if o:
                res = (
                    "Allocation de place dans le marché n°"
                    + o.droit_place_marche.numero_place
                    + " de "
                    + o.droit_place_marche.nom_marche.nom
                )
        elif obj.entity == enums.ENTITY_VEHICULE_ACTIVITE:
            o = VehiculeActivite.objects.get(id=obj.entity_id)
            if o:
                res = (
                    "Carte municipale de transport n°"
                    + o.numero_activite
                    + ", plaque n°: "
                    + o.vehicule.plaque
                    + " - "
                    + o.vehicule.sous_categorie.nom
                )
        elif obj.entity == enums.ENTITY_DROIT_STATIONNEMENT:
            o = VehiculeActivite.objects.get(id=obj.entity_id)
            if o:
                res = (
                    "Droit de stationnement n°"
                    + o.numero_activite
                    + ", plaque n°: "
                    + o.vehicule.plaque
                    + " - "
                    + o.vehicule.sous_categorie.nom
                )
        elif obj.entity == enums.ENTITY_VEHICULE_PROPRIETE:
            o = VehiculeProprietaire.objects.get(id=obj.entity_id)
            if o:
                res = (
                    "Carte de propriété n°"
                    + o.numero_carte
                    + ", Vélo/vélo-moteur n°"
                    + o.vehicule.plaque
                    + " - "
                    + o.vehicule.sous_categorie.nom
                )

    return res


def get_entity_obj(obj):

    # return EntityHelpers.get_entity(obj)
    obj_entity = None

    if obj.entity == enums.ENTITY_ACTIVITE_STANDARD:
        obj_entity = Standard.objects.get(id=obj.entity_id)
    if obj.entity == enums.ENTITY_ACTIVITE_MARCHE:
        obj_entity = Marche.objects.get(id=obj.entity_id)
    if obj.entity == enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
        obj_entity = AllocationEspacePublique.objects.get(id=obj.entity_id)
    if obj.entity == enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
        obj_entity = AllocationPanneauPublicitaire.objects.get(id=obj.entity_id)
    if obj.entity == enums.ENTITY_PUBLICITE_MUR_CLOTURE:
        obj_entity = PubliciteMurCloture.objects.get(id=obj.entity_id)
    if obj.entity == enums.ENTITY_ALLOCATION_PLACE_MARCHE:
        obj_entity = AllocationPlaceMarche.objects.get(id=obj.entity_id)
    # if obj.entity == enums.ENTITY_BATIMENTS_MUNICIPAUX:
    # obj_entity = BatimentMunicipaux.objects.get(id=obj.entity_id)

    # Transport
    if obj.entity == enums.ENTITY_VEHICULE_PROPRIETE:
        obj_entity = VehiculeProprietaire.objects.get(id=obj.entity_id)
    elif obj.entity == enums.ENTITY_VEHICULE_ACTIVITE:
        obj_entity = VehiculeActivite.objects.get(id=obj.entity_id)
    elif obj.entity == enums.ENTITY_DROIT_STATIONNEMENT:
        obj_entity = VehiculeActivite.objects.get(id=obj.entity_id)
    elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
        obj_entity = FoncierExpertise.objects.get(id=obj.entity_id)

    # Impot foncier
    elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
        obj_entity = FoncierExpertise.objects.get(id=obj.entity_id)

    return obj_entity


def get_entity_reference(obj):
    """
    Filter : renvoie la référence de l'entity modèle (numero de carte, ref de l'activité, etc.)
    """
    value = get_entity_obj(obj)

    res = None
    if isinstance(value, Standard):  # (Activité Standard)
        res = value.numero_activite
    elif isinstance(value, Marche):  # (Activité Marché)
        res = value.numero_activite
    elif isinstance(value, VehiculeProprietaire):
        res = value.numero_carte
    elif isinstance(
        value, VehiculeActivite
    ):  # (VehiculeActivite et Droit de stationnement)
        res = value.numero_activite

    if res is None:
        res = ""

    return res


def get_entity_label(obj):
    """
    Filter : renvoie le libellé de l'entity modèle (numero de carte, ref de l'activité, etc.)
    value = obj_entity
    """
    value = get_entity_obj(obj)
    res = ""
    if (
        isinstance(value, Standard)
        or isinstance(value, Marche)
        or isinstance(value, VehiculeProprietaire)
        or isinstance(value, VehiculeActivite)
    ):  # (Activité Standard)
        res = "Numéro de carte"

    return res


def get_ni_type(obj):
    ni_type_string = None

    if obj.entity == enums.ENTITY_ACTIVITE_STANDARD:
        ni_type_string = "activites-professionnelles"
    if obj.entity == enums.ENTITY_ACTIVITE_MARCHE:
        ni_type_string = "activite-marches"
    if obj.entity == enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
        ni_type_string = "espaces-publiques"
    if obj.entity == enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
        ni_type_string = "panneau-publicitaire"
    if obj.entity == enums.ENTITY_PUBLICITE_MUR_CLOTURE:
        ni_type_string = "publicite-mur-cloture"
    if obj.entity == enums.ENTITY_ALLOCATION_PLACE_MARCHE:
        ni_type_string = "place-marches"
    if obj.entity == enums.ENTITY_VISITE_SITE_TOURISTIQUE:
        ni_type_string = "Visite-site-touristique"
    # if obj.entity == enums.ENTITY_BATIMENTS_MUNICIPAUX:
    # ni_type_string = BatimentMunicipaux.objects.get(id=obj.entity_id)

    # Transport
    if obj.entity == enums.ENTITY_VEHICULE_PROPRIETE:
        ni_type_string = "transport"
    elif obj.entity == enums.ENTITY_VEHICULE_ACTIVITE:
        ni_type_string = "transport"
    elif obj.entity == enums.ENTITY_DROIT_STATIONNEMENT:
        ni_type_string = "transport"
    elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
        ni_type_string = "foncier"

    # Impot foncier
    elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
        ni_type_string = "foncier"

    # Avis pour les documments
    if obj.entity == enums.ENTITY_ATTESTATION:
        ni_type_string = "attestion"

    elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
        ni_type_string = "acte"

    return ni_type_string

def get_ai_type(obj):
    ni_type_string = None

    if obj.entity == enums.ENTITY_ACTIVITE_STANDARD:
        ni_type_string = "activites-professionnelles"
    if obj.entity == enums.ENTITY_ACTIVITE_MARCHE:
        ni_type_string = "activite-marches"
    if obj.entity == enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
        ni_type_string = "espaces-publiques"
    if obj.entity == enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
        ni_type_string = "panneau-publicitaire"
    if obj.entity == enums.ENTITY_PUBLICITE_MUR_CLOTURE:
        ni_type_string = "publicite-mur-cloture"
    if obj.entity == enums.ENTITY_ALLOCATION_PLACE_MARCHE:
        ni_type_string = "place-marches"
    if obj.entity == enums.ENTITY_VISITE_SITE_TOURISTIQUE:
        ni_type_string = "Visite-site-touristique"
    # if obj.entity == enums.ENTITY_BATIMENTS_MUNICIPAUX:
    # ni_type_string = BatimentMunicipaux.objects.get(id=obj.entity_id)

    # Transport
    if obj.entity == enums.ENTITY_VEHICULE_PROPRIETE:
        ni_type_string = "transport"
    elif obj.entity == enums.ENTITY_VEHICULE_ACTIVITE:
        ni_type_string = "transport"
    elif obj.entity == enums.ENTITY_DROIT_STATIONNEMENT:
        ni_type_string = "transport"
    elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
        ni_type_string = "foncier"

    # Impot foncier
    elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
        ni_type_string = "foncier"

    # Avis pour les documments
    if obj.entity == enums.ENTITY_ATTESTATION:
        ni_type_string = "attestion"

    elif obj.entity == enums.ENTITY_IMPOT_FONCIER:
        ni_type_string = "acte"

    return ni_type_string
