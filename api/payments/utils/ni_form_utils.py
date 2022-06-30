import logging
from datetime import datetime

from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Q

from mod_parametrage import enums  # , models
from mod_finance.models import NoteImposition, Periode
from mod_helpers.models import Chrono

from .ni_periode import get_next_period


logger = logging.getLogger(__name__)


def get_next_periode_by_note(note, check_year=False):
    """
    Lire la période suivante d'une note d'imposition
    """
    next_periode = None
    is_next_year = False

    # obj_note = (
    #     NoteImposition.objects.filter(entity=note.entity, entity_id=note.entity_id)
    #     .order_by("-id")
    #     .first()
    # )
    obj_note = note
    if isinstance(obj_note, NoteImposition):
        current_periode = obj_note.periode

        periode_obj = Periode.objects.get(id=current_periode.id)
        lst = Periode.objects.filter(periode_type=periode_obj.periode_type).order_by(
            "element"
        )

        if check_year:
            next_periode, is_next_year = get_next_period(
                current_periode, check_year=True
            )
        else:
            next_periode = get_next_period(current_periode)

        if next_periode is None:
            next_periode = Periode.objects.get(element=current_periode.element)

    if check_year:
        return next_periode, is_next_year
    else:
        return next_periode


def get_taxe_montant(entity, obj_entity):
    if entity in [enums.ENTITY_ACTIVITE_STANDARD, enums.ENTITY_ACTIVITE_MARCHE]:
        return obj_entity.taxe.tarif
    elif entity in [enums.ENTITY_ALLOCATION_PLACE_MARCHE]:
        return obj_entity.droit_place_marche.cout_place
    elif entity in [
        enums.ENTITY_ALLOCATION_ESPACE_PUBLIQUE,
        enums.ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE,
        enums.ENTITY_PUBLICITE_MUR_CLOTURE,
    ]:
        return obj_entity.superficie * obj_entity.taxe.tarif
    elif entity in [enums.ENTITY_VEHICULE_ACTIVITE]:
        return obj_entity.vehicule.sous_categorie.taxe_activite.tarif
    elif entity in [enums.ENTITY_DROIT_STATIONNEMENT]:
        return obj_entity.vehicule.sous_categorie.taxe_stationnement.tarif
    elif entity in [enums.ENTITY_VEHICULE_PROPRIETE]:
        return obj_entity.vehicule.sous_categorie.taxe_proprietaire.tarif


def get_num_without_chrono(prefixe):
    res = ""
    obj = Chrono.objects.get(prefixe=prefixe)
    if obj:
        res = obj.prefixe
        if obj.annee:
            res += datetime.now().strftime("%Y")
        if obj.mois:
            res += datetime.now().strftime("%m")

    return res


def save_last_chrono(obj_chrono, chrono):
    if obj_chrono:
        obj_chrono.last_chrono = chrono
        obj_chrono.save()


# Renvoie le nouveau numéro
def get_new_reference(prefixe):
    obj = Chrono.objects.get(prefixe=prefixe)
    if obj:
        # 1 - Si nouveau mois (comparer le mois en cours avec le dernier mois du last chrono)
        if obj.annee and obj.mois:
            # Get info last chrono
            nombre = obj.nombre
            annee_mois = obj.last_chrono[len(prefixe) : -nombre]
            annee = annee_mois[0:4]
            mois = annee_mois[-2:]

            # Get info periode
            annee_new = datetime.now().strftime("%Y")
            mois_new = datetime.now().strftime("%m")

            # Comparer le mois
            if mois != mois_new:
                chrono = get_num_without_chrono(prefixe)  # chrono : AI201801
                chrono = chrono + str(1).zfill(obj.nombre)  # AI201801000000001

                save_last_chrono(obj, chrono)

                return chrono

        # 2 - Generer new chrono à base de last chrono
        chrono = obj.last_chrono.rstrip()
        if (chrono) != "":
            chrono = chrono[-obj.nombre :]  # chrono : 0000000001
            chrono = int(chrono) + 1  # chrono : 2
            chrono = str(chrono).zfill(
                obj.nombre
            )  # remplir zero devant, chrono : 000000002

            the_chrono = obj.last_chrono[: -obj.nombre] + chrono
            save_last_chrono(obj, the_chrono)

            return the_chrono  # nouveau chrono : AI2018010000000002
        else:
            chrono = get_num_without_chrono(prefixe)  # chrono : AI201801
            chrono = chrono + str(1).zfill(obj.nombre)  # AI201801000000001

            save_last_chrono(obj, chrono)
            return chrono

    return None


def generate_next_note(user, note_actuelle, obj_entity, annee):
    logger.debug("Creating next note ...")

    nouvelle_periode, is_next_year = get_next_periode_by_note(
        note_actuelle, check_year=True
    )  # OU periode = self.cleaned_data.get('periode')
    taxe_montant_calc = get_taxe_montant(note_actuelle.entity, obj_entity)
    nouvelle_reference = get_new_reference(enums.CHRONO_NOTE_IMPOSITION)

    if not annee:
        annee = note_actuelle.annee

    if is_next_year:
        # THis means the next note is in next year
        # This is a check to do for next year notes
        annee += 1

    error_messages = []

    # Si Année < année écriture de l'objet alors refuser
    if annee < obj_entity.date_ecriture.year:
        error_messages.append("L'année " + str(annee) + " n'est plus valide")

    if obj_entity.id != note_actuelle.entity_id:
        error_messages.append("Entité invalide.")

    # Tester si l'objet a été déjà générée pour cette période
    query = (
        Q(periode__exact=nouvelle_periode)
        & Q(annee__exact=annee)
        & Q(entity__exact=enums.ENTITY_ACTIVITE_STANDARD)
        & Q(entity_id__exact=obj_entity.id)
    )  # UNICITE
    if NoteImposition.objects.filter(query).exists():
        error_messages.append(
            "La taxe de cette activité a été déjà payée pour la période ("
            + nouvelle_periode.get_element_display()
            + " "
            + str(annee)
            + ")"
        )

    # Tester s'il y a des notes pour les periodes qui suivent dans la meme annee
    if NoteImposition.objects.filter(
        Q(periode__exact=nouvelle_periode) & Q(annee__exact=annee)
    ).exists():
        pass

    # Si invalide montant calculE
    if not taxe_montant_calc or not nouvelle_reference or not user:
        error_messages.append(
            "Montant de taxe, nouvelle reference ou utilisateur non trouvé(e)."
        )
        logger.debug(
            "User: %s, Reference: %s, Montant: %s."
            % (user, nouvelle_reference, taxe_montant_calc)
        )

    if len(error_messages):
        logger.error(_(" & ".join(error_messages)))
        return None

    # Construction de l'object
    nouvelle_note = NoteImposition(
        reference=nouvelle_reference,
        contribuable=note_actuelle.contribuable,
        entity=note_actuelle.entity,
        entity_id=note_actuelle.entity_id,
        periode=nouvelle_periode,
        annee=annee,
        libelle=note_actuelle.libelle,
        taxe=note_actuelle.taxe,
        taxe_montant=taxe_montant_calc,
        taxe_montant_paye=0,
        numero_carte_physique=note_actuelle.numero_carte_physique,
    )

    # Traçabilité
    dateTimeNow = timezone.now()
    nouvelle_note.user_create = user
    nouvelle_note.date_update = dateTimeNow
    nouvelle_note.user_update = user
    nouvelle_note.date_validate = dateTimeNow
    nouvelle_note.user_validate = user

    nouvelle_note.save()

    return nouvelle_note


def bulk_generate_consecutive_notes(user, note_, obj_entity, annee_selectionnee):
    periode, is_next_year = get_next_periode_by_note(note_, check_year=True)
    if is_next_year:
        next_year_check = annee_selectionnee + 1
    else:
        next_year_check = annee_selectionnee

    # On genere juste pour les notes payees qui
    # n'ont pas de periode suivante
    if (
        note_.taxe_montant_paye == note_.taxe_montant
        and not NoteImposition.objects.filter(
            annee=next_year_check,
            periode=periode,
            entity=note_.entity,
            entity_id=note_.entity_id,
        ).exists()
    ):
        print(annee_selectionnee, note_.periode)
        # Generate new note
        next_note_ = generate_next_note(user, note_, obj_entity, annee_selectionnee)
        if next_note_:
            note_ = next_note_
            bulk_generate_consecutive_notes(user, note_, obj_entity, annee_selectionnee)
