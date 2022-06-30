from django.db.models import Q

from mod_parametrage import enums  # , models
from mod_transport.models import VehiculeActivite
from mod_foncier.models import FoncierExpertise
from mod_activite.models import (
    BaseActivite,
    Marche,
    AllocationPlaceMarche,
    AllocationPanneauPublicitaire,
    AllocationEspacePublique,
    PubliciteMurCloture,
)
import datetime

def get_note_imposition_lookup(ni_type, serializer_data, note_imposition, contribuable):
    lookup_query = Q()
    detected_invalid_data = False
    not_ni_contribuable_check = not note_imposition and not contribuable

    # Calculer le montant de l'impot (terrain non bati et construction)
    # somme_taxe, tnb, tb = get_montant_note(obj)

    # Si accroissement existe
    # taux_accroisement = obj.has_accroissement
    # MONTANT_DU = accroissement = 0
    # if somme_taxe>0 and taux_accroisement>0:
    #     accroissement = (somme_taxe * taux_accroisement) / 100

    # MONTANT_DU = somme_taxe + accroissement

    # Note Imposition
    if ni_type == "note_imposition":
        note_imposition = serializer_data.get("note_imposition", None)

        lookup_query = Q(reference__iexact=note_imposition)

        if not note_imposition:
            # Run invalid
            detected_invalid_data = True

    # Transport
    elif ni_type == "transport":
        lookup_query = lookup_query & (
            Q(entity=enums.ENTITY_DROIT_STATIONNEMENT)
            | Q(entity=enums.ENTITY_VEHICULE_PROPRIETE)
            | Q(entity=enums.ENTITY_VEHICULE_ACTIVITE)
        )

        plaque = serializer_data.get("plaque", None)
        numero_carte = serializer_data.get("numero_carte", None)

        vehicule_activite = VehiculeActivite.objects.filter(
            Q(numero_activite__iexact=numero_carte) | Q(vehicule__plaque__iexact=plaque)
        ).first()

        if vehicule_activite and (plaque or numero_carte):
            lookup_query = lookup_query & (Q(entity_id=vehicule_activite.id))
        elif (plaque or numero_carte) or (not_ni_contribuable_check):
            # Run invalid
            detected_invalid_data = True

    # Foncier
    elif ni_type == "foncier":
        numero_parcelle = serializer_data.get("numero_parcelle", None)
        lookup_query = lookup_query & Q(entity=enums.ENTITY_IMPOT_FONCIER)

        foncier_exp = FoncierExpertise.objects.filter(
            parcelle__numero_parcelle__iexact=numero_parcelle
        ).first()

        # print("fparccc : ", foncier_exp)

        if foncier_exp and numero_parcelle:
            lookup_query = lookup_query & (Q(entity_id=foncier_exp.id))
        elif numero_parcelle or not_ni_contribuable_check:
            # Run invalid
            detected_invalid_data = True

    # ActivitE Professionnelle
    elif ni_type == "activites-professionnelles":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ACTIVITE_STANDARD)

        numero_activite = serializer_data.get("numero_activite", None)
        activite = BaseActivite.objects.filter(
            numero_activite__iexact=numero_activite
        ).first()
        if activite and numero_activite:
            lookup_query = lookup_query & Q(entity_id=activite.id)
        elif numero_activite or not_ni_contribuable_check:
            # Run invalid
            detected_invalid_data = True

    # ActivitE Marche
    elif ni_type == "activite-marches":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ACTIVITE_MARCHE)

        numero_activite = serializer_data.get("numero_activite", None)

        marche = Marche.objects.filter(
            Q(numero_activite__iexact=numero_activite)
        ).first()

        if marche and numero_activite:
            lookup_query = lookup_query & Q(entity_id=marche.id)
        elif numero_activite or not_ni_contribuable_check:
            # RUn Invalid
            detected_invalid_data = True

    # Places Marche
    elif ni_type == "place-marches":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ALLOCATION_PLACE_MARCHE)

        numero_place = serializer_data.get("numero_place", None)

        allocation = AllocationPlaceMarche.objects.filter(
            Q(droit_place_marche__numero_place__iexact=numero_place)
        ).first()

        if allocation and numero_place:
            lookup_query = lookup_query & Q(entity_id=allocation.id)
        elif numero_place or not_ni_contribuable_check:
            # RUn Invalid
            detected_invalid_data = True

    # Espaces Publiques
    elif ni_type == "espaces-publiques":
        numero_parcelle = serializer_data.get("numero_parcelle", None)
        reference_allocation = serializer_data.get("reference_allocation", None)
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE)

        allocation = AllocationEspacePublique.objects.filter(
            Q(parcelle_publique__numero_parcelle__iexact=numero_parcelle)
            | Q(numero_allocation__iexact=reference_allocation)
        ).first()

        if allocation and (reference_allocation or numero_parcelle):
            lookup_query = lookup_query & (Q(entity_id=allocation.id))
        elif (reference_allocation or numero_parcelle) or (not_ni_contribuable_check):
            # Run invalid
            detected_invalid_data = True

    # Panneaux publicitaires
    elif ni_type == "panneau-publicitaire":
        numero_parcelle = serializer_data.get("numero_parcelle", None)
        reference_allocation = serializer_data.get("numero_allocation", None)
        lookup_query = lookup_query & Q(
            entity=enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE
        )

        allocation = AllocationPanneauPublicitaire.objects.filter(
            Q(parcelle_publique__numero_parcelle__iexact=numero_parcelle)
            | Q(numero_allocation__iexact=reference_allocation)
        ).first()

        if allocation and (reference_allocation or numero_parcelle):
            lookup_query = lookup_query & (Q(entity_id=allocation.id))
        elif (reference_allocation or numero_parcelle) or (not_ni_contribuable_check):
            # Run invalid
            detected_invalid_data = True

    # Panneaux publicitaires
    elif ni_type == "publicite-mur-cloture":
        reference_juridique = serializer_data.get("reference_juridique", None)
        reference_allocation = serializer_data.get("numero_allocation", None)
        lookup_query = lookup_query & Q(entity=enums.ENTITY_PUBLICITE_MUR_CLOTURE)
        allocation = PubliciteMurCloture.objects.filter(
            Q(numero_allocation__iexact=reference_allocation)
            | Q(reference_juridique__iexact=reference_juridique)
        ).first()

        if allocation and (reference_allocation or reference_juridique):
            lookup_query = lookup_query & (Q(entity_id=allocation.id))
        elif (reference_allocation or reference_juridique) or (
            not_ni_contribuable_check
        ):
            # Run invalid
            detected_invalid_data = True

    else:
        detected_invalid_data = True

    return lookup_query, detected_invalid_data

def get_last_note(note_imposition):
    # Note Imposition
    laste_note_not_payed = False
    get_note = None
    obj = None
    datetimeNow = datetime.datetime.now()
    # verifier si  "note_imposition" n'est pas vide
    if len(note_imposition)>0:
        obj = NoteImposition.objects.get(reference=note_imposition)
    else:
        return laste_note_not_payed, get_note

    # rechercher de NI non paye foncier
    if obj.entity == enums.ENTITY_IMPOT_FONCIER:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_IMPOT_FONCIER,
            contribuable_id = obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant and note.annee < datetimeNow.year:
                laste_note_not_payed = True
                get_note = note.reference
        return laste_note_not_payed,get_note

    # rechercher de NI non paye transport droit stationnement
    if obj.entity == enums.ENTITY_DROIT_STATIONNEMENT:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_DROIT_STATIONNEMENT,
            contribuable_id = obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant:
                if note.annee < datetimeNow.year:
                    laste_note_not_payed = True
                    get_note = note.reference
                else:
                    if note.peride_id < int(datetimeNow.month):
                        laste_note_not_payed = True
                        get_note = note.reference
        return laste_note_not_payed,get_note

    # rechercher de NI non paye transport vehicule propriete
    if obj.entity == enums.ENTITY_VEHICULE_PROPRIETE:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_VEHICULE_PROPRIETE,
            contribuable_id = obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant and note.annee < datetimeNow.year:
                laste_note_not_payed = True
                get_note = note.reference
        return laste_note_not_payed,get_note

    # rechercher de NI non paye transport vehicule acivite
    if obj.entity == enums.ENTITY_VEHICULE_ACTIVITE:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_VEHICULE_ACTIVITE,
            contribuable_id=obj.contribuable_id
        ).order_by('id').ferst()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant:
                if note.annee < datetimeNow.year:
                    laste_note_not_payed = True
                    get_note = note.reference
                else:
                    periode = 0
                    if 1 <= int(datetimeNow.month)<4:
                        periode = 13
                    elif 3 < int(datetimeNow.month)<7:
                        periode = 14
                    elif 6 < int(datetimeNow.month)<10:
                        periode = 15
                    elif 9<int(datetimeNow.month)<13:
                        periode = 16

                    if note.peride_id < periode:
                        laste_note_not_payed = True
                        get_note = note.reference
        return laste_note_not_payed, get_note

    # rechercher de NI non paye Activite Professionnelle
    if obj.entity == enums.ENTITY_ACTIVITE_STANDARD:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_ACTIVITE_STANDARD,
            contribuable_id=obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant and note.annee < datetimeNow.year:
                laste_note_not_payed = True
                get_note = note.reference
        return laste_note_not_payed, get_note

    # rechercher de NI non paye Activite dans le Marche
    if obj.entity == enums.ENTITY_ACTIVITE_MARCHE:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_ACTIVITE_MARCHE,
            contribuable_id=obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant and note.annee < datetimeNow.year:
                laste_note_not_payed = True
                get_note = note.reference
        return laste_note_not_payed, get_note

    # rechercher de NI non paye allocation place marche
    if obj.entity == enums.ENTITY_ALLOCATION_PLACE_MARCHE:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_ALLOCATION_PLACE_MARCHE,
            contribuable_id=obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant:
                if note.annee < datetimeNow.year:
                    laste_note_not_payed = True
                    get_note = note.reference
                else:
                    if note.peride_id < int(datetimeNow.month):
                        laste_note_not_payed = True
                        get_note = note.reference
        return laste_note_not_payed, get_note

    # rechercher de NI non paye allocation espace publique
    if obj.entity == enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE,
            contribuable_id=obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant and note.annee < datetimeNow.year:
                laste_note_not_payed = True
                get_note = note.reference
        return laste_note_not_payed, get_note

    # rechercher de NI non paye allocation panneau publicitaire
    if obj.entity == enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE,
            contribuable_id=obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant and note.annee < datetimeNow.year:
                laste_note_not_payed = True
                get_note = note.reference
        return laste_note_not_payed, get_note

    # rechercher de NI non paye publicité sur mur cloture
    if obj.entity == enums.ENTITY_PUBLICITE_MUR_CLOTURE:
        check_last_note = NoteImposition.objects.filter(
            entity=enums.ENTITY_PUBLICITE_MUR_CLOTURE,
            contribuable_id=obj.contribuable_id
        ).order_by('id').first()
        for note in check_last_note:
            if note.taxe_montant_paye < note.taxe_montant and note.annee < datetimeNow.year:
                laste_note_not_payed = True
                get_note = note.reference
        return laste_note_not_payed, get_note


def get_avis_imposition_lookup(ni_type, serializer_data,avis_imposition, contribuable):
    lookup_query = Q()
    detected_invalid_data = False
    not_ai_contribuable_check = not avis_imposition and not contribuable

    # Avis Imposition
    if ni_type == "avis_imposition":
        avis_imposition = serializer_data.get("avis_imposition", None)

        lookup_query = Q(reference__iexact=avis_imposition)

        if not avis_imposition:
            detected_invalid_data = True

    # Attestation
    elif ni_type == "attestation":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ATTESTATION)

    # Acte
    elif ni_type == "acte":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ACTE)

    # Activite Exceptionnel
    elif ni_type == "activiteexceptionnel":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ACTIVITE_EXCEPTIONNELLE)

    # Standard Duplicata
    elif ni_type == "standardduplicata":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ACTIVITE_STANDARD_DUPLICATA)

    # VisiteSite Touristique
    elif ni_type == "visitesitetouristique":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_VISITE_SITE_TOURISTIQUE)

    # Marche Duplicata
    elif ni_type == "marcheduplicata":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_ACTIVITE_MARCHE_DUPLICATA)

    # Vehicule Activite Duplicata
    elif ni_type == "vehiculeactiviteduplicata":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_VEHICULE_ACTIVITE_DUPLICATA)

    # Vehicule Proprietaire Duplicata
    elif ni_type == "vehiculeproprietaireduplicata":
        lookup_query = lookup_query & Q(entity=enums.ENTITY_VEHICULE_PROPRIETE_DUPLICATA)

    else:
        detected_invalid_data = True

    return lookup_query, detected_invalid_data
