from django import template
from django.utils.safestring import mark_safe
from django.db.models import Q

from mod_transport.models import *
from mod_finance.models import *

from mod_helpers.hlp_global_variables import GlobalVariablesHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_parametrage.enums import *

import datetime

register = template.Library()

#------------------------------------------------------------
@register.filter()
def get_info_vehicule(value):
    """
    Renvoie l'information du véhicule
    """
    info = ''
    if value :
        obj = Vehicule.objects.get(id = value.id)
        if obj:
            info = str(obj) + ' - ' + obj.sous_categorie.nom

    return info

#------------------------------------------------------------
@register.filter()
def vehicule_bool(value):
    """
    :param value: boolean
    :return: Oui/Non
    """
    res = "Non"
    if value:
        res = "Oui"

    return res
#------------------------------------------------------------
@register.filter()
def vehicule_localite(value):
    """
    :param value: boolean
    :return: Locale/Etrangère
    """
    res = "Etrangère"
    if value:
        res = "Locale"

    return res

#------------------------------------------------------------
@register.filter()
def vehicule_bool_safe(value):
    """
    :param value: boolean
    :return: Oui/Non
    """
    res = "<span class='badge badge-danger'>Non</span>"
    if value:
        res = "<span class='badge badge-primary'>Oui</span>"

    return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def vehicule_actif(obj):
    """
    :param value: boolean
    :return: Oui/Non
    """
    if not obj.sous_categorie.has_plaque and not obj.remunere:
        res = "<span class='badge badge-secondary'>Privé</span>"
    else:
        res = "<span class='badge badge-danger'>Non</span>"
        if obj.actif:
            res = "<span class='badge badge-primary'>Oui</span>"

    return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def filter_status_validate(obj, stationnement=False):
    """
    Filter : pour le status des véhicule, activité véhicule, ...
    """
    objToRet= "<span class='badge badge-danger'>Brouillon</span>"
      
    if not isinstance(obj, Vehicule) and obj.date_ecriture:
        # VehiculeActivite, VehiculeProprietaire, Droit de stationnement (si stationnement=True)
        if stationnement:
            note = EntityHelpers.get_last_note_imposition_stationnement(obj)
        else:
            note = EntityHelpers.get_last_note_imposition(obj)
        
        if note:
            periode = str(note.periode.get_element_display()) + '-' +str(note.annee)
            objToRet = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span><br><span class='badge badge-info'>Générée: " + periode + "</span>"
        else:    
            objToRet = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span><br><span class='badge badge-info'>Générée: " + obj.date_ecriture.strftime("%d/%m/%Y") + "</span>"
    else:
        if obj.date_validate:    
            objToRet = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span>"
            if not isinstance(obj, Vehicule):
                if not obj.date_ecriture:
                    objToRet =  "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span><br><span class='badge badge-danger'>Non générée</span>"
        else:
            # Cas Véhicule
            if isinstance(obj, Vehicule):
                if obj.fichier_carterose:
                    objToRet = "<span class='badge badge-warning'>En attente</span>"
                else:
                    objToRet = "<span class='badge badge-warning'>Carte rose !!!</span>"
           
            # Cas Véhicule Activité
            elif isinstance(obj, VehiculeActivite):
                if obj.fichier_carterose and obj.fichier_autorisation:
                    objToRet = "<span class='badge badge-warning'>En attente</span>"
                else:
                    objToRet = "<span class='badge badge-warning'>Autorisation !!!</span>"

    return mark_safe(objToRet)


#------------------------------------------------------------
@register.filter()
def filter_status_transfert(obj):
    """
    Filter : pour le status des véhicule, activité véhicule, ...
    """
    objToRet= "<span class='badge badge-danger'>Brouillon</span>"
    obj_v = Vehicule.objects.get(id=obj.vehicule_id)
      
    if isinstance(obj, VehiculeTransfert) and obj.date_transfert and obj_v.fichier_carterose:
            objToRet = "<span class='badge badge-success'>Transférer le : " + obj.date_transfert.strftime("%d/%m/%Y") + "</span>"
    else: 
        objToRet = "<span class='badge badge-danger'>Brouillon</span><br><span class='badge badge-danger'>Veilleur atacher le carte rose</span>"

    return mark_safe(objToRet)

#------------------------------------------------------------
@register.filter()
def filter_value_none(value):
    """
    Filter : pour la vaeur nulle, afficher vide
    """
    if value is None or value == 'None':
        return ''

    return value

#------------------------------------------------------------
@register.filter()
def is_ai_payed(obj):
    """
    Filter : SI l'avis d'imposition est déjà payé 
    obj : l'objet qui possède la propriété (nombre_impression)
    """
    entity = 0

    if isinstance(obj, VehiculeProprietaire):
        entity = ENTITY_VEHICULE_PROPRIETAIRE
    elif isinstance(obj, VehiculeProprietaireDuplicata):
        entity = ENTITY_VEHICULE_PROPRIETAIRE_DUPLICATA
    elif isinstance(obj, VehiculeActivite):
        entity = ENTITY_VEHICULE_ACTIVITE
    elif isinstance(obj, VehiculeActiviteDuplicata):
        entity = ENTITY_VEHICULE_ACTIVITE_DUPLICATA

    if entity > 0:
        ai = AvisImposition.objects.get(entity=entity, entity_id=obj.id)
        if ai:
            return ai.is_payed

    return False

#------------------------------------------------------------
@register.filter()
def is_ni_payed(obj):
    """
    Filter : SI la note d'imposition est déjà payé 
    obj : l'objet qui possède la propriété (nombre_impression)
    """
    entity = 0
    
    if isinstance(obj, VehiculeProprietaire):
        entity = ENTITY_VEHICULE_PROPRIETE
    elif isinstance(obj, VehiculeActivite):
        entity = ENTITY_VEHICULE_ACTIVITE
        
    if entity > 0:
        ni = NoteImposition.objects.get(entity=entity, entity_id=obj.id)
        if ni:
            return ni.is_payed

    return False

#------------------------------------------------------------
@register.filter()
def ai_filter_status_payed(obj):
    """
    Filter : pour le status de payement
    """
    if obj.date_validate:
        if is_ai_payed(obj):
            objToRet =  "<br> <span class='badge badge-success'>Avis payé</span>"
        else:
            objToRet =  "<br> <span class='badge badge-danger'>Avis impayée</span>"
    else:
        objToRet = ""

    return mark_safe(objToRet)

#------------------------------------------------------------
@register.filter()
def ni_filter_status_payed(obj):
    """
    Filter : pour le status de payement
    """
    if obj.date_validate:
        if is_ni_payed(obj):
            objToRet =  "<br> <span class='badge badge-success'>Note payée</span>"
        else:
            objToRet =  "<br> <span class='badge badge-danger'>Note impayée</span>"
    else:
        objToRet = ""
        
    return mark_safe(objToRet)

#------------------------------------------------------------
@register.filter()
def show_note(note):
    if note:
        note = "<i title='" + note + "' class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>"
    else:
        note = ''
    
    return mark_safe(note)  

#------------------------------------------------------------
@register.filter()
def show_me(obj, current_user):
    """
    Filtere : Colorie l'icone commentaire (note)
    """
    note = ''
    if obj.note:
        if obj.demande_annulation_validation:
            note = "<i class='fa fa-commenting' aria-hidden='true' style='color:red;'></i>&nbsp;" # Danger (Demande dd'annulation de validatio d'un objet)
        else:
            note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>&nbsp;" # Warning
    else:
        note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#808080'></i>&nbsp;" # info

    res = "<span class='text-muted'>" + note + str(obj.user_create) + "</span>"
    if obj.user_create == current_user:
        res= "<span class='text-primary'>" + note + str(obj.user_create) + "</span>"
    
    res += "<br><span class='text-muted'><small>" + obj.date_create.strftime("%d/%m/%Y %H:%M") + "</small></span>"

    return mark_safe(res)


# ------------------------------------------------------------
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

    res = "<span class='text-muted'>" + note + str(obj.user_arret) + "</span>"
    if obj.user_arret == current_user:
        res = "<span class='text-primary'>" + note + str(obj.user_arret) + "</span>"

    res += "<br><span class='text-muted'><small>" + obj.date_arret.strftime("%d/%m/%Y %H:%M") + "</small></span>"

    return mark_safe(res)

#------------------------------------------------------------

# ------------------------------------------------------------
@register.filter()
def show_me_tr(obj, current_user):
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

    res = "<span class='text-muted'>" + note + str(obj.user_transfert) + "</span>"
    if obj.user_transfert == current_user:
        res = "<span class='text-primary'>" + note + str(obj.user_transfert) + "</span>"

    if obj.date_transfert:
        res += "<br><span class='text-muted'><small>" + obj.date_transfert.strftime("%d/%m/%Y %H:%M") + "</small></span>"

    return mark_safe(res)

#------------------------------------------------------------

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

    if obj and isinstance(obj, Vehicule):
        nombre = Vehicule.objects.filter(user_create=user).count()
        nombre_valid = Vehicule.objects.filter(user_create=user, date_validate__isnull=False).count()

    elif obj and isinstance(obj, VehiculeActivite):
        nombre = VehiculeActivite.objects.filter(user_create=user).count()
        nombre_valid = VehiculeActivite.objects.filter(user_create=user, date_validate__isnull=False).count()

    elif obj and isinstance(obj, VehiculeProprietaire):
        nombre = VehiculeProprietaire.objects.filter(user_create=user).count()
        nombre_valid = VehiculeProprietaire.objects.filter(user_create=user, date_validate__isnull=False).count()

    elif obj and isinstance(obj, VehiculeActiviteDuplicata):
        nombre = VehiculeActiviteDuplicata.objects.filter(user_create=user).count()
        nombre_valid = VehiculeActiviteDuplicata.objects.filter(user_create=user, date_validate__isnull=False).count()

    elif obj and isinstance(obj, VehiculeProprietaireDuplicata):
        nombre = VehiculeProprietaireDuplicata.objects.filter(user_create=user).count()
        nombre_valid = VehiculeProprietaireDuplicata.objects.filter(user_create=user, date_validate__isnull=False).count()

    if nombre>0:
        if nombre_valid==1:
            res_valid = " dont <strong style='color:#000;'>" + str(nombre_valid) + '</strong> a été validé'
        elif nombre_valid>1:
            res_valid = " dont <strong style='color:#000;'>" + str(nombre_valid) + '</strong> ont été validés'
        else:
            res_valid = ''
        res = "<label class='fa fa-check text-muted'>&nbsp; <em style='color:#4588B3;'>"+ str(user).capitalize() +"</em>, vous avez créé <strong style='color:#000;'>" + str(nombre) + "</strong> éléments" + res_valid + "</label>"
    else:
        res = ''

    return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def show_compte_propre(sous_categorie, compte_propre):
    res = sous_categorie
    if compte_propre:
        res += "<br><span class='badge badge-danger'>compte propre</span>"

    return mark_safe(res)

#------------------------------------------------------------
#-------------------------- PRINT ---------------------------
#------------------------------------------------------------
@register.filter()
def is_print_number_achieved(obj):
    """
    Filter : Connaitre SI le nombre d'impressions effectuées est atteint 
    obj : l'objet qui possède la propriété (nombre_impression)
    """
    obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
    nbr_print = 0

    if isinstance(obj, VehiculeProprietaire):
        nbr_print = obj.nombre_impression
    elif isinstance(obj, VehiculeProprietaireDuplicata):
        nbr_print = obj.nombre_impression
    elif isinstance(obj, VehiculeActivite):
        nbr_print = obj.nombre_impression
    elif isinstance(obj, VehiculeActiviteDuplicata):
        nbr_print = obj.nombre_impression
            
    if obj_gv and nbr_print >= int(obj_gv.valeur):
        return True
    
    return False

#------------------------------------------------------------
@register.filter()
def get_prochaine_periode_transport(note_imposition):
    """
    Renvoyer la période de paiement suivante
    note_imposition.entity = ENTITY_VEHICULE_ACTIVITE (11) et ENTITY_DROIT_STATIONNEMENT (12)
    """
    res =''

    if isinstance(note_imposition, NoteImposition):
        periode = PeriodeHelpers.getNextPeriode(note_imposition.periode)

        if periode.periode_type.categorie == MENSUELLE:
            if periode.element==NOVEMBRE:
                month = str(JANVIER).zfill(2) # Mettre le mois en string (JANVIER)
            elif periode.element==DECEMBRE:
                month = str(FEVRIER).zfill(2) # Mettre le mois en string (FEVRIER)
            else:
                month = str(periode.element+1).zfill(2) # Mettre le mois en string

        elif periode.periode_type.categorie == TRIMSTRIELLE:
            month = str(PeriodeHelpers.getFirstMonthTrimestre(periode)).zfill(2) # Mettre le mois en string
            
        elif periode.periode_type.categorie == SEMESTRIELLE:
            month = str(PeriodeHelpers.getFirstMonthSemestriel(periode)).zfill(2) # Mettre le mois en string            
        elif periode.periode_type.categorie == ANNUELLE:
            month = '01'

        year = PeriodeHelpers.getYearFromNextPeriode(note_imposition.periode, note_imposition.annee)

        if note_imposition.entity == ENTITY_VEHICULE_ACTIVITE:
            res = GlobalVariablesHelpers.get_global_variables("ACTIVITE_TRANSPORT", "DATE_LIMIT_PAIE_ACTIVITE_TRANSPORT").valeur + '/' + month + '/' + str(year)

        elif note_imposition.entity == ENTITY_DROIT_STATIONNEMENT:
            res = GlobalVariablesHelpers.get_global_variables("STATIONNEMENT", "DATE_LIMIT_PAIE_STATIONNEMENT").valeur + '/' + month + '/' + str(year)

    return res

#------------------------------------------------------------
#----------------------- TRABLEAU DE BORD -------------------
#------------------------------------------------------------
@register.filter()
def nombre_vehicule(value, type=None):
    """
	Filter : renvoie le nombre nombre des véhicules enregistrés sur le système
	"""
    nombre = value
    if type==0:
        # Privés
        nombre = Vehicule.objects.filter(remunere=False).count()
    elif type==1:
        # En activités
        nombre = Vehicule.objects.filter(remunere=True).count()
    else:
        # Tous les véhicules
        nombre = Vehicule.objects.count()

    return nombre

@register.filter()
def nombre_carte(value, type=None):
    """
    Filter : renvoie le nombre nombre des cartes enregistrées sur le système
    """
    nombre = 0
    valide = 0
    if type==0:
        # Cartes de propriété
        nombre = VehiculeProprietaire.objects.filter().count()
        valide = VehiculeProprietaire.objects.filter(date_validate__isnull=False).count()
    elif type==1:
        # Cartes Professionnelles
        nombre = VehiculeActivite.objects.filter().count()
        valide = VehiculeProprietaire.objects.filter(date_validate__isnull=False).count()
    else:
        #Cartes délivrées
        nombre = VehiculeProprietaire.objects.filter().count()
        nombre += VehiculeActivite.objects.filter(date_validate__isnull=False).count()
        valide = VehiculeProprietaire.objects.filter(date_validate__isnull=False).count()

    res = str(valide) + ' / ' + str(nombre)

    return mark_safe(res)

@register.filter()
def nombre_carte_duplicata(value, type=None):
    """
    Filter : renvoie le nombre nombre des duplicata des cartes enregistrées sur le système
    """
    nombre = value
    if type==0:
        # Cartes de propriété
        nombre = VehiculeProprietaireDuplicata.objects.filter(date_validate__isnull=False).count()
    elif type==1:
        # Cartes Professionnelles
        nombre = VehiculeActiviteDuplicata.objects.filter(date_validate__isnull=False).count()
    else:
        #Cartes délivrées
        nombre = VehiculeProprietaireDuplicata.objects.filter(date_validate__isnull=False).count()
        nombre += VehiculeActiviteDuplicata.objects.filter(date_validate__isnull=False).count()

    return nombre
