from django import template
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db.models import Q, F, Sum  # taxe_montant__gte=F('montant_total')

from mod_activite.models import *
from mod_transport.models import *
from mod_finance.models import *
from mod_foncier.models import FoncierParcellePublique
from mod_parametrage.enums import *

from mod_helpers.hlp_global_variables import GlobalVariablesHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.hlp_accroissement import AccroissementHelpers

from datetime import datetime
import datetime, re

register = template.Library()


# ------------------------------------------------------------
@register.filter()
def filter_status_validate(obj):
    """
	Filter : pour le status des activités
	obj : Activité
	"""
    res = "<span class='badge badge-warning'>Brouillon</span>"

    if obj.date_ecriture:
        note = EntityHelpers.get_last_note_imposition(obj)
        if note:
            periode = str(note.annee)
            res = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime(
                "%d/%m/%Y") + "</span><br><span class='badge badge-info'>Générée: " + periode + "</span>"
        else:
            res = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime(
                "%d/%m/%Y") + "</span><br><span class='badge badge-info'>Générée</span>"
    else:
        if obj.date_validate:
            res = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime(
                "%d/%m/%Y") + "</span><br><span class='badge badge-warning'>Non générée</span>"
        else:
            # Ca Standard
            if isinstance(obj, Standard):
                if not obj.fichier_autorisation:
                    objToRet = "<span class='badge badge-warning'>Pièce jointe!!!</span>"
                else:
                    res = "<span class='badge badge-warning'>En attente</span>"

            # Ca Publicité Panneau publicitaire
            if isinstance(obj, AllocationEspacePublique) or isinstance(obj,
                                                                       AllocationPanneauPublicitaire) or isinstance(obj,
                                                                                                                    PubliciteMurCloture):
                if not obj.fichier_lettre_exp_tmp:
                    objToRet = "<span class='badge badge-warning'>Pièce jointe!!!</span>"
                else:
                    res = "<span class='badge badge-warning'>En attente</span>"
            else:
                res = "<span class='badge badge-warning'>En attente</span>"

    return mark_safe(res)


# ------------------------------------------------------------
@register.filter()
def filter_duplicata(value):
    """
	Filter : pour le status des activités
	"""
    res = "Non"

    if (value):
        res = "Oui"

    return res


# ------------------------------------------------------------
@register.filter()
def filter_status_arreter(date_arret):
    """
	Filter : pour le status des activités
	"""
    res = "<span class='badge badge-warning'>Ouverte</span>"

    if (date_arret):
        res = "<span class='badge badge-success'>Clôturée le <br>" + format(date_arret, '%d/%m/%Y') + " </span>"

    return mark_safe(res)


# ------------------------------------------------------------
@register.filter()
def filter_report_photo(contribuableId):
    """
	Filter : pour la photo dans les reports
	"""
    res = ""
    obj_physique = PersonnePhysique.objects.get(pk=contribuableId)

    if (obj_physique):
        res = obj_physique.photo_file

    return res


# ------------------------------------------------------------
@register.filter()
def filter_report_cin(contribuableId):
    """
	Filter : pour la photo dans les reports
	"""
    res = ""
    obj_physique = PersonnePhysique.objects.get(pk=contribuableId)
    if (obj_physique):
        res = obj_physique.identite_numero

    return res


# ------------------------------------------------------------
@register.filter()
def filter_report_date(value):
    """
	Filter : pour la date du jour
	"""
    dateTimeNow = datetime.now()

    return dateTimeNow


# ------------------------------------------------------------
@register.filter()
def filter_value_none(value):
    """
	Filter : pour la vaeur nulle, afficher vide
	"""
    if value is None:
        return ''
    return value


# ------------------------------------------------------------
@register.filter()
def filter_report_none(value):
    """
	Filter : pour la photo dans les reports
	"""
    if value is None:
        return ''
    return value


# ------------------------------------------------------------
@register.filter()
def get_reference_parcelle(numero_parcelle):
    """
	Renvoie la référence de la parcelle publuque alloué
	"""

    obj = FoncierParcellePublique.objects.filter(numero_parcelle=numero_parcelle)

    if obj:
        obj = obj[0]  # Lit le premier objet trouvé
        rue = ''
        if obj.numero_rueavenue:
            rue = ' - (Rue-Avenue: ' + obj.numero_rueavenue.nom + ')'

        adresse_precise = ''
        if obj.adresse_precise:
            adresse_precise = ' (' + obj.adresse_precise + ')'

        return obj.numero_parcelle + ' - ' + obj.adresse.zone.commune.nom + ' - ' + obj.adresse.zone.nom + ' - ' + obj.adresse.nom + adresse_precise + rue

    return numero_parcelle


# ------------------------------------------------------------
@register.filter()
def show_type_publicite(value):
    """
	Afficher en différente couleur les types de publicité
	"""
    objToRet = "<span class='text text-primary'>Mur</span>"
    if value == 1:
        objToRet = "<span class='text text-success'>Clôture</span>"

    return mark_safe(objToRet)


# ------------------------------------------------------------
@register.filter()
def show_note(note):
    if note:
        note = "<i title='" + note + "' class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>"
    else:
        note = ''

    return mark_safe(note)


# ------------------------------------------------------------
@register.filter()
def show_me(obj, current_user):
    """
	Filtere : Colorie l'icone commentaire (note)
	"""
    note = ''
    if obj.note:
        if obj.demande_annulation_validation:
            note = "<i class='fa fa-commenting' aria-hidden='true' style='color:red;'></i>&nbsp;"  # Danger (Demande dd'annulation de validatio d'un objet)
        else:
            note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>&nbsp;"  # Warning
    else:
        note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#808080'></i>&nbsp;"  # info

    res = "<span class='text-dark'>" + note + str(obj.user_create) + "</span>"
    if obj.user_create == current_user:
        res = "<span class='text-primary'>" + note + str(obj.user_create) + "</span>"

    res += "<br><span class='text-muted'><small>" + obj.date_create.strftime("%d/%m/%Y %H:%M") + "</small></span>"

    return mark_safe(res)


# ------------------------------------------------------------
@register.filter()
def show_user_art(obj, current_user):
    """
    Filtere : Colorie l'icone commentaire (note)
    """
    if not obj.date_arret:
        res = "<span class='badge badge-warning'>Cette activite n'est pas encore arrêter</span>"
    else:
        res = "<span class='text-muted'>" +str(obj.user_arret) + "</span>"
        if obj.user_arret == current_user:
            res = "<span class='text-primary'>" + str(obj.user_arret) + "</span>"

        res += "<br><span class='text-muted'><small>" + obj.date_arret.strftime("%d/%m/%Y %H:%M") + "</small></span>"

    return mark_safe(res)

@register.filter()
def show_mee(obj, current_user):
    """
    Filtere : Colorie l'icone commentaire (note)
    """
    note = ''
    if obj.note:
        if obj.demande_annulation_validation:
            note = "<i class='fa fa-commenting' aria-hidden='true' style='color:red;'></i>&nbsp;"  # Danger (Demande dd'annulation de validatio d'un objet)
        else:
            note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>&nbsp;"  # Warning
    else:
        note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#808080'></i>&nbsp;"  # info

    res = "<span class='text-muted'>" + note + str(obj.user_create) + "</span>"
    if obj.user_create == current_user:
        res = "<span class='text-primary'>" + note + str(obj.user_create) + "</span>"

    res += "<br><span class='text-muted'><small>" + obj.date_create.strftime("%d/%m/%Y %H:%M") + "</small></span>"

    return mark_safe(res)


# ------------------------------------------------------------
@register.filter()
def is_ni_payed(obj):
    """
	Filter : SI la note d'imposition est déjà payé
	obj : l'objet qui possède la propriété (nombre_impression)
	"""
    entity = 0

    if isinstance(obj, Standard):
        entity = ENTITY_ACTIVITE_STANDARD
    elif isinstance(obj, Marche):
        entity = ENTITY_ACTIVITE_MARCHE

    if entity > 0:
        ni = NoteImposition.objects.filter(entity=entity, entity_id=obj.id).first()
        if ni:
            return ni.is_payed

    return False


# ------------------------------------------------------------
@register.filter()
def nombre_enreg_by_user(lst, user):
    """
	Renvoie le nombre d'enregistrements par utilisateur
	"""
    nombre = 0
    nombre_valid = 0

    obj = None
    if lst:
        obj = lst[0]

    if obj:
        if isinstance(obj, Standard):
            nombre = Standard.objects.filter(user_create=user).count()
            nombre_valid = Standard.objects.filter(user_create=user, date_validate__isnull=False).count()

        if isinstance(obj, Marche):
            nombre = Marche.objects.filter(user_create=user).count()
            nombre_valid = Marche.objects.filter(user_create=user, date_validate__isnull=False).count()

        if isinstance(obj, ActiviteExceptionnelle):
            nombre = ActiviteExceptionnelle.objects.filter(user_create=user).count()
            nombre_valid = ActiviteExceptionnelle.objects.filter(user_create=user, date_validate__isnull=False).count()

        if isinstance(obj, AllocationPlaceMarche):
            nombre = AllocationPlaceMarche.objects.filter(user_create=user).count()
            nombre_valid = AllocationPlaceMarche.objects.filter(user_create=user, date_validate__isnull=False).count()

        if isinstance(obj, AllocationEspacePublique):
            nombre = AllocationEspacePublique.objects.filter(user_create=user).count()
            nombre_valid = AllocationEspacePublique.objects.filter(user_create=user,
                                                                   date_validate__isnull=False).count()

        if isinstance(obj, AllocationPanneauPublicitaire):
            nombre = AllocationPanneauPublicitaire.objects.filter(user_create=user).count()
            nombre_valid = AllocationPanneauPublicitaire.objects.filter(user_create=user,
                                                                        date_validate__isnull=False).count()

        if isinstance(obj, PubliciteMurCloture):
            nombre = PubliciteMurCloture.objects.filter(user_create=user).count()
            nombre_valid = PubliciteMurCloture.objects.filter(user_create=user, date_validate__isnull=False).count()

        if isinstance(obj, VisiteSiteTouristique):
            nombre = VisiteSiteTouristique.objects.filter(user_create=user).count()
            nombre_valid = VisiteSiteTouristique.objects.filter(user_create=user, date_validate__isnull=False).count()

    if nombre > 0:
        if nombre_valid == 1:
            res_valid = " dont <strong style='color:#000;'>" + str(nombre_valid) + '</strong> a été validé'
        elif nombre_valid > 1:
            res_valid = " dont <strong style='color:#000;'>" + str(nombre_valid) + '</strong> ont été validés'
        else:
            res_valid = ''
        res = "<label class='fa fa-check text-muted'>&nbsp; <em style='color:#4588B3;'>" + str(
            user).capitalize() + "</em>, vous avez créé <strong style='color:#000;'>" + str(
            nombre) + "</strong> éléments" + res_valid + "</label>"
    else:
        res = ''

    return mark_safe(res)


# ------------------------------------------------------------
# -------------------------- PRINT ---------------------------
# ------------------------------------------------------------
@register.filter()
def is_print_number_achieved(obj):
    """
	Filter : Connaitre SI le nombre d'impressions effectuées est atteint
	obj : l'objet qui possède la propriété (nombre_impression)
	"""
    obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
    nbr_print = 0

    if isinstance(obj, Standard):
        nbr_print = obj.nombre_impression
    elif isinstance(obj, Marche):
        nbr_print = obj.nombre_impression

    # Duplicata ????????????????????????

    if obj_gv and nbr_print >= int(obj_gv.valeur):
        return True

    return False


# ------------------------------------------------------------
# ---------------------- TABLEAU DE BORD ---------------------
# ------------------------------------------------------------
@register.filter()
def nombre_activite(value):
    """
	Filter : renvoie le nombre total des activités standard enregistrées dans le système
	"""
    nombre = 0

    if value == 1:
        # ACTIVITE STANDARD
        nombre = Standard.objects.filter(date_validate__isnull=False).count()
    elif value == 2:
        # ACTIVITE MARCHE
        nombre = Marche.objects.filter(date_validate__isnull=False).count()

    return nombre


# ------------------------------------------------------------
@register.filter()
def standard_get_number_by_user(status, user):
    """
    Renvoie le nombre de données saisies par utilisateur (SAISIE, VALIDE, GENERE, PAYE)
    1 : Saisies
    2 : Validées
    3 : Générées
    4 : Payées
    enum.entity = ENTITY_ACTIVITE_STANDARD
    """
    nombre = 0
    if isinstance(user, User):
        if status == 1:
            nombre = Standard.objects.filter(user_create=user).count()
        elif status == 2:
            nombre = Standard.objects.filter(user_validate=user).count()
        elif status == 3:
            nombre = Standard.objects.filter(user_ecriture=user).count()
        elif status == 4:
            query = Q(taxe_montant_paye__gte=F('taxe_montant')) & Q(date_validate__isnull=False) & Q(user_validate=user)
            query &= Q(entity=ENTITY_ACTIVITE_STANDARD)
            nombre = NoteImposition.objects.filter(query).count()

    return nombre


# ------------------------------------------------------------
@register.filter()
def marche_get_number_by_user(status, user):
    """
    Renvoie le nombre de données saisies par utilisateur (SAISIE, VALIDE, GENERE, PAYE)
    1 : Saisies
    2 : Validées
    3 : Générées
    4 : Payée
    enum.entity = ENTITY_ACTIVITE_MARCHE
    """
    nombre = 0
    if isinstance(user, User):
        if status == 1:
            nombre = Marche.objects.filter(user_create=user).count()
        elif status == 2:
            nombre = Marche.objects.filter(user_validate=user).count()
        elif status == 3:
            nombre = Marche.objects.filter(user_ecriture=user).count()
        elif status == 4:
            query = Q(taxe_montant_paye__gte=F('taxe_montant')) & Q(date_validate__isnull=False) & Q(user_validate=user)
            query &= Q(entity=ENTITY_ACTIVITE_MARCHE)
            nombre = NoteImposition.objects.filter(query).count()

    return nombre


# ------------------------------------------------------------
@register.filter()
def standard_get_total_user(status):
    """
    Renvoie le total de données saisies de tous les utilisateurs (SAISIE, VALIDE, GENERE, PAYE)
    1 : Saisies
    2 : Validées
    3 : Générées
    4 : Payées
    enum.entity = ENTITY_ACTIVITE_STANDARD
    """
    total = 0
    if status == 1:
        total = Standard.objects.count()
    elif status == 2:
        total = Standard.objects.filter(date_validate__isnull=False).count()
    elif status == 3:
        total = Standard.objects.filter(date_ecriture__isnull=False).count()
    elif status == 4:
        query = Q(taxe_montant_paye__gte=F('taxe_montant')) & Q(date_validate__isnull=False)
        query &= Q(entity=ENTITY_ACTIVITE_STANDARD)
        total = NoteImposition.objects.filter(query).count()

    return total


# ------------------------------------------------------------
@register.filter()
def marche_get_total_user(status):
    """
    Renvoie le total de données saisies de tous les utilisateurs (SAISIE, VALIDE, GENERE, PAYE)
    1 : Saisies
    2 : Validées
    3 : Générées
    4 : Payées
    enum.entity = ENTITY_ACTIVITE_MARCHE
    """
    total = 0
    if status == 1:
        total = Marche.objects.count()
    elif status == 2:
        total = Marche.objects.filter(date_validate__isnull=False).count()
    elif status == 3:
        total = Marche.objects.filter(date_ecriture__isnull=False).count()
    elif status == 4:
        query = Q(taxe_montant_paye__gte=F('taxe_montant')) & Q(date_validate__isnull=False)
        query &= Q(entity=ENTITY_ACTIVITE_MARCHE)
        total = NoteImposition.objects.filter(query).count()

    return total


# ------------------------------------------------------------
# ---------------------- ACCROISSEMENT -----------------------
# ------------------------------------------------------------
@register.filter()
def has_accroissement(obj):
    '''
	'''
    # return AccroissementHelpers.has_accroissement(obj.annee_declaration, obj.date_note_imposition):
    return 0


@register.filter()
def get_info_accroissement(obj):
    """
    Renvoie l'info concernant l'accroissement
    """
    res = ''
    if isinstance(obj, Standard) or isinstance(obj, Marche) or isinstance(obj, AllocationEspacePublique) or isinstance(
            obj, AllocationPanneauPublicitaire) or isinstance(obj, PubliciteMurCloture):
        taux_accroisement = 0  # obj.has_accroissement
        accroissement = 0
        MONTANT_DU = 0

        '''
        if taux_accroisement>0:
            total, tnb, tb = get_montant_note(obj)
            accroissement = (total * taux_accroisement) / 100
            MONTANT_DU = accroissement + total
            res = "<span class='text-primary'>Vous avez un accroissement de <em class='text-danger'>" + str(taux_accroisement) + "%</em>, dû au retard de déclaration de l'impôt foncier. Le montant total <em class='text-danger'>À PAYER</em> s'élève à <em class='bg bg-warning text-dark'>&nbsp;<strong>" + str(intcomma(int(MONTANT_DU))) + ".Bif</strong>&nbsp;&nbsp;</em> dont la valeur de l'accroissement est de <em class='text-danger'>" + intcomma(int(accroissement)) + " Bif</em>.</span>"
        '''
        res = "<span class='text-primary'>Vous avez un accroissement de <em class='text-danger'>" + str(
            taux_accroisement) + "%</em>, dû au retard de déclaration de l'impôt foncier. Le montant total <em class='text-danger'>À PAYER</em> s'élève à <em class='bg bg-warning text-dark'>&nbsp;<strong>" + str(
            intcomma(int(
                MONTANT_DU))) + ".Bif</strong>&nbsp;&nbsp;</em> dont la valeur de l'accroissement est de <em class='text-danger'>" + intcomma(
            int(accroissement)) + " Bif</em>.</span>"

    return mark_safe(res)


@register.filter()
def getDate(date):
    dateGet = str(date)
    match_str = re.search(r'\d{4}-\d{2}-\d{2}', dateGet)
    datecheck = None
    if date != None:
        res = datetime.datetime.strptime(match_str.group(), '%Y-%m-%d').date()
        return res
    else:
        return datecheck


@register.filter()
def getDateReverse(date):
    datecheck = None
    if date != None:
        datecheck = datetime.datetime.strptime(date, '%m/%d/%Y')
        return datecheck
    else:
        return datecheck