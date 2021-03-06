from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Sum #taxe_montant__gte=F('montant_total')

from mod_parametrage.enums import *
from mod_crm.models import *
from mod_activite.models import *
from mod_transport.models import *
from mod_finance.models import *
from mod_foncier.models import *
import calendar

from mod_helpers.hlp_global_variables import GlobalVariablesHelpers
from mod_helpers.hlp_accroissement import AccroissementHelpers

register = template.Library()

@register.filter()
def get_reference_object(obj):
    """
    Renvoyer la référence de l'activité
    """
    res = ''
    if isinstance(obj, NoteImposition):
        if obj.entity==ENTITY_ACTIVITE_STANDARD:
            o = Standard.objects.get(id=obj.entity_id)
            if o:
                res = o.numero_activite
        elif obj.entity==ENTITY_ACTIVITE_MARCHE:
            o = Marche.objects.get(id=obj.entity_id)
            if o:
                res = o.numero_activite
        elif obj.entity==ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
            o = AllocationEspacePublique.objects.get(id=obj.entity_id)
            if o:
                res = o.numero_allocation
        elif obj.entity==ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
            o = AllocationPanneauPublicitaire.objects.get(id=obj.entity_id)
            if o:
                res = o.numero_allocation
        elif obj.entity==ENTITY_PUBLICITE_MUR_CLOTURE:
            o = PubliciteMurCloture.objects.get(id=obj.entity_id)
            if o:
                res = o.numero_allocation
        elif obj.entity==ENTITY_ALLOCATION_PLACE_MARCHE:
            o = AllocationPlaceMarche.objects.get(id=obj.entity_id)
            if o:
                res = o.droit_place_marche.nom_marche + ' n°' + str(o.droit_place_marche.numero_place)
        elif obj.entity==ENTITY_VEHICULE_ACTIVITE :
            o = VehiculeActivite.objects.get(id=obj.entity_id)
            if o:
                res = o.numero_activite
        elif obj.entity==ENTITY_DROIT_STATIONNEMENT :
            o = VehiculeActivite.objects.get(id=obj.entity_id)
            if o:
                res = o.numero_activite
        elif obj.entity==ENTITY_VEHICULE_PROPRIETE :
            o = VehiculeProprietaire.objects.get(id=obj.entity_id)
            if o:
                res = o.numero_carte

    elif isinstance(obj, Standard) or isinstance(obj, Marche):
        res = obj.numero_activite
    elif isinstance(obj, AllocationEspacePublique):
        res = obj.numero_allocation        
    elif isinstance(obj, AllocationPanneauPublicitaire):
        res = obj.numero_allocation
    elif isinstance(obj, PubliciteMurCloture):
        res = obj.numero_allocation
    elif isinstance(obj, AllocationPlaceMarche):
        res = obj.droit_place_marche.nom_marche + ' n°' + str(obj.droit_place_marche.numero_place)
    elif isinstance(obj, VehiculeActivite): # et Stationnement
        res = obj.numero_activite
    elif isinstance(obj, VehiculeProprietaire):
        res = obj.numero_carte
    
    return res 

#------------------------------------------------------------
@register.filter()
def get_note_reference(pk):
    """
    Renvoyer le numero de reference de la note d'imposition
    """
    try:
        obj = NoteImposition.objects.get(pk=pk)
        return obj.reference
    except:
        pass
    
    return ''

#------------------------------------------------------------
@register.filter()
def get_caution_montant(caution_montant):
    """
    Afficher la caution de l'allocation de place dans le marche
    """
    res = ''
    if caution_montant>0:
        res = "<br><span class='badge badge-info'>Dont caution: " + intcomma(caution_montant) + "</span>"

    return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_entity_model(entity, taxe_filter):
    if not entity and int(taxe_filter)==0:
        return 'Autres'
    elif not entity and int(taxe_filter)==1:
            return 'Administratif'
    elif entity == ENTITY_VEHICULE_PROPRIETE:
        return 'Carte de propriété'
    elif entity == ENTITY_VEHICULE_PROPRIETE_DUPLICATA: 
        return 'Duplicata propriété'
    elif entity == ENTITY_VEHICULE_ACTIVITE:
        return "Carte professionnelle"
    elif entity == ENTITY_VEHICULE_ACTIVITE_DUPLICATA:
        return "Duplicata professionnel"

    return ''
#------------------------------------------------------------
@register.filter()
def ai_status_paiement(obj):
    """
    Filter : pour le status de paiement d'un avis d'imposition
    """
    status = "<span class='badge badge-danger'>Non validé</span><br><span class='badge badge-danger'>Non payé</span>"
    
    if obj.date_paiement and obj.fichier_paiement and obj.date_validate:
        status = "<span class='badge badge-info'>Valiée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span><br><span class='badge badge-success'>Payé</span>"
    elif obj.date_paiement and obj.fichier_paiement and not obj.date_validate:
        status = "<span class='badge badge-danger'>Non validé</span><br><span class='badge badge-success'>Payé</span>"
    elif obj.date_paiement and not obj.fichier_paiement and not obj.date_validate:
        status = "<span class='badge badge-danger'>Non validé</span><br><span class='badge badge-warning'>Bordereau !!!</span>"
    
    return mark_safe(status)

#------------------------------------------------------------
@register.filter()
def ni_status_paiement(obj):
    """
    Filter : pour le status de paiement d'une note d'imposition
    """
    status = "<span class='badge badge-secondary'>Non validée</span> <br> <span class='badge badge-danger'>Non payé</span>"

    # Si la note est validée alors
    if obj.date_validate:
        if obj.taxe_montant == obj.taxe_montant_paye:
            paiement = NoteImpositionPaiement.objects.filter(note_imposition=obj).first()
            if paiement:
                status = "<span class='badge badge-info'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span>"
                if paiement.date_validate:
               	    status += "<br> <span class='badge badge-success'>Payée: " + paiement.date_validate.strftime("%d/%m/%Y") + "</span>"
            elif obj.taxe_montant == obj.taxe_montant_paye == 0 and obj.entity==ENTITY_VEHICULE_ACTIVITE:
                # PAIEMENT EXTERNE
                status = "<span class='badge badge-info'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span> <br> <span class='badge badge-success'>Payée <strong>ZERO</strong></span>"
                if not obj.paiement_externe_file:
                    status += "&nbsp;<span class='badge badge-warning'>Fichier attaché!!!</span>"
            else:
                # ERROR = QUELQU'UN A MODIFIÉ À LA MAIN LE MONTANT DE LA BASE !!!
                status = "<span class='badge badge-warning'>ERREUR !!!</span>"
        elif obj.taxe_montant_paye > 0:
            status = "<span class='badge badge-info'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span> <br> <span class='badge badge-warning'>Reste à payer</span> &nbsp; <strong>" + str(
                intcomma(obj.taxe_montant - obj.taxe_montant_paye)) + "</strong>"
        else:
            status = "<span class='badge badge-info'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span> <br> <span class='badge badge-danger'>Non payée</span>"        

    return mark_safe(status)

#------------------------------------------------------------
@register.filter()
def ni_get_paiement_object(obj_note):
    """
    Renvoie un objet paiement à partir d'une note d'iosition
    """
    if obj_note and isinstance(obj_note, NoteImposition):
        if obj_note.is_payed:
            return  NoteImpositionPaiement.objects.filter(note_imposition__id=obj_note.id).first()
    
    return None

#------------------------------------------------------------
@register.filter()
def ni_status_paiement_details(value):
    """
    Filter : si le status de paiementde details est valié ou en mode brouillon
    """
    status = "<span class='badge badge-warning'>Brouillon</span>"
    if value.date_validate:
        status = "<span class='badge badge-success'>Validé</span>"
    elif value.fichier_paiement:
        status = "<span class='badge badge-warning'>En attente</span>"
    else:
        status = "<span class='badge badge-warning'>Bordereau !!!</span>"

    return mark_safe(status)

#------------------------------------------------------------
@register.filter()
def taxe_filter(value):
    """
    Filter : taxe (voir parametrage.enum : choix_taxe_filter 
    """
    if value:
        return choix_taxe_filter[int(value)][1]

    return 'Autre'

#------------------------------------------------------------
@register.filter()
def taxe_filter_ni(value):
    """
    Filter : taxe (voir parametrage.enum : choix_profil_ni 
    """
    if value:
        return choix_profil_ni[int(value)][1]

    return 'Autre'

#------------------------------------------------------------
@register.filter()
def get_activite_reference(value, obj=None):
    """
    Filter : prendre la référence de l'activité
    """
    if value:
        if isinstance(obj, BaseActivite):
            obj = BaseActivite.objects.get(pk=value)
            if (obj):
                return obj.numero_activite

    return ''

#------------------------------------------------------------
@register.filter()
def get_foncier_expertise_reference(value):
    """
    Filter : prendre la référence de l'activité
    """
    if value:
        obj = FoncierExpertise.objects.get(pk=value)
        if obj:
            return obj.parcelle.numero_parcelle

    return ''

#------------------------------------------------------------
@register.filter()
def parser_libelle_foncier(libelle):
    """
    Parser le libelle car c'est trop long. (.) est deja definit statiquement dans FoncierExpertise.ecriture
    """
    if libelle:
        libelle = libelle.split('.')[0]

    return libelle

#------------------------------------------------------------
@register.filter()
def ni_is_valid(value):
    """
    Filter : si la note d'imposition est valide ou non
    """
    status = ""
    if value:
        obj = NoteImposition.objects.get(pk=value)
        if (obj):
            if obj.date_validate:
                status = "disabled"

    return mark_safe(status)

#------------------------------------------------------------
@register.filter()
def get_activite_adresse(value):
    """
    Filter : lire l'adresse de l'activité
    value : id activité
    type_activite : Standard : 1, Marche : 2, Transport : 3
    """
    adresse = ''
    if value:
        try:
            obj = Standard.objects.get(pk=value)
            if (obj):
                adresse = obj.adresse_activite.zone.nom + ' - ' + obj.adresse_activite.nom + ' - ' + obj.numero_rueavenue.nom
        except ObjectDoesNotExist:
            try:
                obj = Marche.objects.get(pk=value)
                if (obj):
                    adresse = 'Marché de ' + obj.nom_marche.nom_marche + ' - n°' + obj.numero_emplacement
            except ObjectDoesNotExist:
                pass

    return adresse

#------------------------------------------------------------
@register.filter()
def get_beneficiaire(value, obj):
    """
    Renvoi le nom du bénéficiaire sinon le nom et maitricule contribuable
    """
    if isinstance(obj, Contribuable):
        if obj:
            return obj.nom + ' - ' + obj.matricule

    return value

#------------------------------------------------------------
@register.tag
def est_paye():
    """
    Renvoi le titre de l'état à imprimé
    """
    return 'self.name'

    if isinstance(self, VehiculeProprietaire):
        query = Q(taxe__categorie_taxe__type_impot = 1) & Q(entity = ENTITY_VEHICULE_PROPRIETE) & Q(entity_id=self.id)
        ni = NoteImposition.objects.filter(q)[0]
        if ni and ni.est_paye():
            return True

    return False

#------------------------------------------------------------
@register.filter()
def show_note(note):
    res = ''
    if note:
        res = "<i title='" + note + "' class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>"
    
    return mark_safe(res)  

#------------------------------------------------------------
@register.filter()
def show_me(obj, current_user):
    """
    Filtere : Colorie l'icone commentaire (note)
    """
    note = ''

    if not isinstance(obj, NoteImposition): # La Note d'impostion n'a pas de Notification
        if obj.note:
            if obj.demande_annulation_validation:
                note = "<i class='fa fa-commenting' aria-hidden='true' style='color:red;'></i>&nbsp;" # Danger (Demande dd'annulation de validatio d'un objet)
            else:
                note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>&nbsp;" # Warning
        else:
            note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#808080'></i>&nbsp;" # info

    res = "<span class='text-dark'>" + note + str(obj.user_create) + "</span>"
    if obj.user_create == current_user:
        res= "<span class='text-primary'>" + note + str(obj.user_create) + "</span>"

    res += "<br><span class='text-muted'><small>" + obj.date_create.strftime("%d/%m/%Y %H:%M") + "</small></span>"

    return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def has_any_note_not_payed(obj_entity, is_stationnement=False):
    """
    Si l'objet entity a au moins une note non payée
    """
    entity = 0
    if isinstance(obj_entity, Standard):
        entity = ENTITY_ACTIVITE_STANDARD
    elif isinstance(obj_entity, Marche):
        entity = ENTITY_ACTIVITE_MARCHE
    elif isinstance(obj_entity, AllocationEspacePublique):
        entity = ENTITY_ALLOCATION_ESPACE_PUBLIQUE
    elif isinstance(obj_entity, AllocationPanneauPublicitaire):
        entity = ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE
    elif isinstance(obj_entity, PubliciteMurCloture):
        entity = ENTITY_PUBLICITE_MUR_CLOTURE
    elif isinstance(obj_entity, AllocationPlaceMarche):
        entity = ENTITY_ALLOCATION_PLACE_MARCHE
    elif isinstance(obj_entity, VehiculeActivite) and is_stationnement:
        entity = ENTITY_DROIT_STATIONNEMENT
    elif isinstance(obj_entity, VehiculeActivite):
        entity = ENTITY_VEHICULE_ACTIVITE
    elif isinstance(obj_entity, VehiculeProprietaire):
        entity = ENTITY_VEHICULE_PROPRIETE

    ni_lst = NoteImposition.objects.filter(entity=entity, entity_id=obj_entity.id).order_by('id')
    for ni in ni_lst:
        if not ni.is_payed:
            return True

    return False

#------------------------------------------------------------
@register.filter()
def show_any_note_not_payed(obj_entity, is_stationnement=False):
    """
    Si l'objet entity a au moins une note non payée
    """
    entity = 0
    res = ""

    if isinstance(obj_entity, Standard):
        entity = ENTITY_ACTIVITE_STANDARD
    elif isinstance(obj_entity, Marche):
        entity = ENTITY_ACTIVITE_MARCHE
    elif isinstance(obj_entity, AllocationEspacePublique):
        entity = ENTITY_ALLOCATION_ESPACE_PUBLIQUE
    elif isinstance(obj_entity, AllocationPanneauPublicitaire):
        entity = ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE
    elif isinstance(obj_entity, PubliciteMurCloture):
        entity = ENTITY_PUBLICITE_MUR_CLOTURE
    elif isinstance(obj_entity, AllocationPlaceMarche):
        entity = ENTITY_ALLOCATION_PLACE_MARCHE
    elif isinstance(obj_entity, VehiculeActivite) and is_stationnement:
        entity = ENTITY_DROIT_STATIONNEMENT
    elif isinstance(obj_entity, VehiculeActivite):
        entity = ENTITY_VEHICULE_ACTIVITE
    elif isinstance(obj_entity, VehiculeProprietaire):
        entity = ENTITY_VEHICULE_PROPRIETE

    ni_lst = NoteImposition.objects.filter(entity=entity, entity_id=obj_entity.id).order_by('id')
    for ni in ni_lst:
        if not ni.is_payed:
            res = "<i class='fa fa-thumbs-down' style='font-size:32px;color:red'></i><span class='bg bg-dark text-white'>&nbsp;Veuillez, s'il vout plaît, payer la note n°<em class='text-danger'><strong>" \
            + ni.reference + "</strong></em> avant de générer cette nouvelle période, Merci.&nbsp;</span>"
            return mark_safe(res)

    return res

#------------------------------------------------------------
#---- PAIEMENT EXTERNE ACTIVITE DE TRANSPORT MUNICIPALE -----
#------------------------------------------------------------
@register.filter()
def ni_status_paiement_externe(obj):
    """
    Filter : pour le status de paiement externe d'une note d'imposition
    CAS DES ACTIVITES MUNICIPALES (TRANSPORT)
    """
    status = ''
    if isinstance(obj, NoteImposition) and obj.date_validate:
        if (obj.entity==ENTITY_VEHICULE_ACTIVITE) and obj.taxe_montant == obj.taxe_montant_paye == 0:
            status = "<span class='badge badge-warning'>&nbsp;Activité EXTERNE&nbsp;</span>"

    return mark_safe(status)

#------------------------------------------------------------
#-------------------------- PRINT ---------------------------
#------------------------------------------------------------
@register.filter()
def get_print_quota(value):
    """
    Nombre d'essai max (quota)
    """
    quota = GlobalVariablesHelpers.get_global_variables('PRINT', 'MAX_NUMBER').valeur

    return 'Effectué : ' + str(value) + ' / Quota : ' + quota

#------------------------------------------------------------
@register.filter()
def get_titre_reporting(obj):
    """
    Renvoi le titre de l'état à imprimé
    """
    res = ''
    if isinstance(obj, NoteImposition) or isinstance(obj, AvisImposition):
        if obj.entity==ENTITY_ACTIVITE_STANDARD:
            res = 'Activité Standard'
        elif obj.entity==ENTITY_ACTIVITE_MARCHE:
            res = 'Activité dans le marché'
        elif obj.entity==ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
            res = "Allocation de l'espace public"
        elif obj.entity==ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
            res = "Allocation du panneau publicitaire"
        elif obj.entity==ENTITY_PUBLICITE_MUR_CLOTURE:
            o = PubliciteMurCloture.objects.get(id=obj.entity_id)
            if o:
                type_publicite = ''
                if o.type_publicite == MUR:
                    type_publicite = ' le mur'
                else:
                    type_publicite = ' la clôture'
                res = "Publicité sur " + type_publicite
        elif obj.entity==ENTITY_ALLOCATION_PLACE_MARCHE:
            res = 'Allocation de place dans le marché'
        elif obj.entity==ENTITY_VEHICULE_ACTIVITE :
            res = 'Carte municipale de transport'
        elif obj.entity==ENTITY_DROIT_STATIONNEMENT :
            res = 'Droit de stationnement'
        elif obj.entity==ENTITY_VEHICULE_PROPRIETE :
            res = 'Carte de propriété'

    return res.lower().capitalize()

#------------------------------------------------------------
@register.filter()
def get_libelle_note_imposition(obj):
    """
    Renvoyer le libellé de la note d'imposition virtuellement 
    """
    res = ''
    if isinstance(obj, NoteImposition):
        if obj.entity==ENTITY_ACTIVITE_STANDARD:
            o = Standard.objects.get(id=obj.entity_id)
            if o:
                res = 'Activité Standard n°' + o.numero_activite + ', ' + o.taxe.libelle.capitalize()
        elif obj.entity==ENTITY_ACTIVITE_MARCHE:
            o = Marche.objects.get(id=obj.entity_id)
            if o:
                res = 'Activité dans le marché n°' + o.numero_activite + ' de ' + o.allocation_place_marche.droit_place_marche.nom_marche.nom + ', place n°' + o.allocation_place_marche.droit_place_marche.numero_place + ' (' + o.taxe.libelle.capitalize() + ')'
        elif obj.entity==ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
            o = AllocationEspacePublique.objects.get(id=obj.entity_id)
            if o:
                res = "Allocation de l'espace public n°" + o.numero_allocation
        elif obj.entity==ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
            o = AllocationPanneauPublicitaire.objects.get(id=obj.entity_id)
            if o:
                res = "Allocation du panneau publicitaire n°" + o.numero_allocation
        elif obj.entity==ENTITY_PUBLICITE_MUR_CLOTURE:
            o = PubliciteMurCloture.objects.get(id=obj.entity_id)
            if o:
                type_publicite = ''
                if o.type_publicite == MUR:
                    type_publicite = ' le mur'
                else:
                    type_publicite = ' la clôture'
                res = "Publicité sur " + type_publicite + " n°" + o.numero_allocation
        elif obj.entity==ENTITY_ALLOCATION_PLACE_MARCHE:
            o = AllocationPlaceMarche.objects.get(id=obj.entity_id)
            if o:
                res = 'Allocation de place dans le marché n°' + o.droit_place_marche.numero_place  + ' de ' + o.droit_place_marche.nom_marche.nom
        elif obj.entity==ENTITY_VEHICULE_ACTIVITE :
            o = VehiculeActivite.objects.get(id=obj.entity_id)
            if o:
                res = 'Carte municipale de transport n°' + o.numero_activite + ', plaque n°: ' + o.vehicule.plaque + ' - ' + o.vehicule.sous_categorie.nom
        elif obj.entity==ENTITY_DROIT_STATIONNEMENT :
            o = VehiculeActivite.objects.get(id=obj.entity_id)
            if o:
                res = 'Droit de stationnement n°' + o.numero_activite + ', plaque n°: ' + o.vehicule.plaque + ' - ' + o.vehicule.sous_categorie.nom
        elif obj.entity==ENTITY_VEHICULE_PROPRIETE :
            o = VehiculeProprietaire.objects.get(id=obj.entity_id)
            if o:
                res = 'Carte de propriété n°' + o.numero_carte + ', Vélo/vélo-moteur n°' + o.vehicule.plaque + ' - ' + o.vehicule.sous_categorie.nom

    return res

#------------------------------------------------------------
@register.filter()
def get_mairie_identification(value):
    """
    Renvoi le titre de l'état à imprimé
    """
    identification_mairie = 'NIF: ' + GlobalVariablesHelpers.get_global_variables('MAIRIE', 'NIF').valeur
    identification_mairie += ', ' + GlobalVariablesHelpers.get_global_variables('MAIRIE', 'ADRESSE').valeur
    identification_mairie += ', ' + GlobalVariablesHelpers.get_global_variables('MAIRIE', 'CONTACT').valeur

    return identification_mairie

#------------------------------------------------------------
@register.filter()
def get_entity_label(value):
    """
    Filter : renvoie le libellé de l'entity modèle (numero de carte, ref de l'activité, etc.)
    value = obj_entity
    """
    res = ''
    if isinstance(value, Standard) or isinstance(value, Marche) or isinstance(value, VehiculeProprietaire) or isinstance(value, VehiculeActivite): #(Activité Standard)
        res = 'Numéro de carte'

    return res

#------------------------------------------------------------
@register.filter()
def get_entity_adresse_title(value):
    """
    Afficher le title de l'adresse pour l'entity spécifié
    """
    res = ''
    if isinstance(value, Standard): # (Activité Standard) 
        res = 'Adresse activité'
    elif isinstance(value, PubliciteMurCloture): # (Mur et Cloture)
        res = 'Adresse publicité'
    elif isinstance(value, AllocationEspacePublique): #(Allocation espace publique)
        res = 'Adresse espace'
    elif isinstance(value, AllocationPanneauPublicitaire): #(Panneau publicitaire)
        res = 'Adresse espace'

    return res

#------------------------------------------------------------
@register.filter
def get_entity_adresse_value(value):
    """
    Afficher la valeur de l'adresse pour l'entity spécifié
    """
    res = ''
    adresse_precise = ''
    if isinstance(value, Standard): #(Activité Standard)
        if value.numero_police:
            res = str(value.adresse) + ', ' +  str(value.numero_rueavenue) + ' n°' + value.numero_police
        else:
            res += str(value.adresse) + ', ' +  str(value.numero_rueavenue)
        
        # Allocation espace publique
        if value.type_espace == PUBLIQUE:
            res += ', ' + value.allocation_espace_publique.numero_allocation + ', ' + value.allocation_espace_publique.parcelle_publique.numero_parcelle
    
    elif isinstance(value, PubliciteMurCloture): #(Mur et Cloture)
        res = str(value.adresse) + ', ' +  str(value.numero_rueavenue)

    elif isinstance(value, AllocationEspacePublique) or isinstance(value, AllocationPanneauPublicitaire): #(Allocation espace publique) ou  (Panneau publicitaire)
        if value.parcelle_publique.adresse_precise:
            adresse_precise = '('+value.parcelle_publique.adresse_precise+')'
        res = str(value.parcelle_publique.adresse) + ', ' +  str(value.parcelle_publique.numero_rueavenue) + adresse_precise + ', espace n°' + value.parcelle_publique.numero_parcelle
    
    if res:
        res = ': ' + res
    else:
        res = ''

    return res

#------------------------------------------------------------
@register.filter()
def get_entity_reference(value):
    """
    Filter : renvoie la référence de l'entity modèle (numero de carte, ref de l'activité, etc.)
    """
    res = None
    if isinstance(value, Standard): #(Activité Standard)
        res = value.numero_activite
    elif isinstance(value, Marche): #(Activité Marché)
        res = value.numero_activite
    elif isinstance(value, VehiculeProprietaire):
        res = value.numero_carte
    elif isinstance(value, VehiculeActivite): #(VehiculeActivite et Droit de stationnement)
        res = value.numero_activite

    if res is None:
        res = ''
    else:
        res = ': ' + res

    return res

#------------------------------------------------------------
@register.filter()
def is_print_number_achieved(obj):
    """
    Filter : Connaitre SI le nombre d'impressions effectuées est atteint 
    obj : l'objet qui possède la propriété (nombre_impression)
    """
    obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
    nbr_print = 0

    if isinstance(obj, NoteImposition):
        nbr_print = obj.nombre_impression
            
    if obj_gv and nbr_print >= int(obj_gv.valeur):
        return True
    
    return False

#------------------------------------------------------------
@register.filter()
def nombre_enreg_by_user(lst, user, entity_filter=0):
    """
    Renvoie le nombre d'enregistrements par utilisateur
    """
    nombre = 0
    nombre_valid = 0

    obj = None
    if lst:
        obj = lst[0]
    
    if obj:
        if isinstance(obj, AvisImposition):
            nombre = AvisImposition.objects.filter(user_create=user).count()
            nombre_valid = AvisImposition.objects.filter(user_create=user, date_validate__isnull=False).count()
        
        if isinstance(obj, NoteImposition):
            nombre = NoteImposition.objects.filter(user_create=user).count()
            nombre_valid = NoteImposition.objects.filter(user_create=user, date_validate__isnull=False).count()

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
def is_ni_vehicule_activite_payed(obj_note):
    """
    Si une note Activité de Transport/Municipale n'est pas encore payée alors Empecher l'impression de la quittance de stationement
    -> Il faut payer L'activité municipale avant d'imprimer la quittance de stationnement
    SAUF PAIEMENT EXTERNE = ENTITY_DROIT_STATIONNEMENT
    """
    res = True
    if isinstance(obj_note, NoteImposition):
        lst = NoteImposition.objects.filter(entity=ENTITY_VEHICULE_ACTIVITE, entity_id=obj_note.entity_id).order_by('id')
        for obj in lst:
            if not obj.is_payed_externe and not obj.is_payed:
                return False

    return res

#------------------------------------------------------------
@register.filter()
def ni_date_limit_paiement(value):
    """
    Renvoie la date limite de paiement
    """
    return GlobalVariablesHelpers.get_global_variables('NI', 'DATE_LIMITE_PAIEMENT').valeur

@register.filter()
def ni_date_limit_paiement_note(value,obj):
    """
    Renvoie la date limite de paiement
    """
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    # res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
    if obj.annee < current_year:
        day = calendar.monthrange(current_year, current_month)[1]
        date_paiement = str(day)+'/'+str(current_month)+'/'+str(current_year)
    else:
        date_paiement = GlobalVariablesHelpers.get_global_variables('NI', 'DATE_LIMITE_PAIEMENT').valeur

    return date_paiement


#------------------------------------------------------------
@register.filter()
def ni_penalite_paiement_premier_mois(value):
    """
    Pénalité pour retard de paiement à la date limite
    """
    return GlobalVariablesHelpers.get_global_variables('PENALITE', 'VALEUR_PREMIER_MOIS').valeur

#------------------------------------------------------------
@register.filter()
def ni_penalite_paiement_autres_mois(value):
    """
    Pénalité pour retard de paiement mensuel
    """
    return GlobalVariablesHelpers.get_global_variables('PENALITE', 'VALEUR_AUTRES_MOIS').valeur

#------------------------------------------------------------
#------ DROIT DE STATIONNEMENT : QUITTANCE PRINT ERROR ------
#------------------------------------------------------------
@register.filter()
def get_ni_vehicule_activite(obj_note):
    """
    Si une note Activité Trasport/Municipale n'est pas encore payée Empecher l'impression de la quittance de stationement
    -> Il faut payer L'activité municipale avant d'imprimer la quittance de stationnement
    """
    res = ''
    if isinstance(obj_note, NoteImposition):
        lst = NoteImposition.objects.filter(entity=ENTITY_VEHICULE_ACTIVITE, entity_id=obj_note.entity_id).order_by('id')
        if lst:
            res = get_note_reference(lst[0].pk)

    return res

#------------------------------------------------------------
@register.filter()
def get_obj_vehicule_activite_by_note(obj_note):
    """
    Si une note Activité Trasport/Municipale n'est pas encore payée Empecher l'impression de la quittance de stationement
    -> Il faut payer L'activité municipale avant d'imprimer la quittance de stationnement
    """
    res = ''
    if isinstance(obj_note, NoteImposition):
        lst = NoteImposition.objects.filter(entity=ENTITY_VEHICULE_ACTIVITE, entity_id=obj_note.entity_id).order_by('id')
        if lst:
            obj = VehiculeActivite.objects.get(id=lst[0].entity_id)
            if obj:
                res = obj.numero_activite

    return res

#------------------------------------------------------------
#---------------------- ACCROISSEMENT -----------------------
#------------------------------------------------------------
@register.filter()
def get_accroissement_label(obj_note, obj_entity):
    """
    Renvoyer la valeur de l'accroissement
    obj_note : note d'imposition déjà créée
    """
    res = ''

    # SAUF VEHICULE ACTIVITE, PROPRIETAIRE et ALLOCATION PLACE DANS LE MARCHE
    if isinstance(obj_entity, VehiculeActivite) or isinstance(obj_entity, VehiculeProprietaire) or isinstance(obj_entity, AllocationPlaceMarche):
        return mark_safe(res)

    if isinstance(obj_note, NoteImposition):
        value = AccroissementHelpers.has_accroissement(obj_note.annee, obj_note.date_validate)
        if value>0:
            acc = obj_note.taxe_montant * value / 100
            MONTANT_DU = obj_entity.taxe.tarif
            res = ' dont <strong>' + str(intcomma(MONTANT_DU)) + ' Bif</strong> avec un accroissement de <strong>' + str(intcomma(acc)) + ' Bif</strong> (Taux = <strong>' + str(value) + '%</strong>)'

    return mark_safe(res)

#------------------------------------------------------------
#--------------------- SOLDE DE DEPART ----------------------
#------------------------------------------------------------
@register.filter()
def get_solde_depart_label(obj_note, obj_entity):
    """
    Renvoyer la valeur de solde de depart
    obj_note : note d'imposition déjà créée
    """
    res = ''

    # SAUF VEHICULE PROPRIETAIRE et ALLOCATION PLACE DANS LE MARCHE
    if isinstance(obj_entity, VehiculeProprietaire) or isinstance(obj_entity, AllocationPlaceMarche):
        return mark_safe(res)

    if isinstance(obj_note, NoteImposition):
        acc = AccroissementHelpers.has_accroissement(obj_note.annee, obj_note.date_validate)
        value = obj_entity.solde_depart
        if value>0:
            if acc>0:
                res = ' et un solde de départ de <strong>' + str(intcomma(value)) + ' Bif</strong>'
            else:
                MONTANT_DU = obj_entity.taxe.tarif  # ???????????????????????? les autres pub et alloc
                res = ' dont <strong>' + str(intcomma(MONTANT_DU)) + ' Bif</strong> avec un solde de départ de <strong>' + str(intcomma(value)) + ' Bif</strong>'

    return mark_safe(res)

#------------------------------------------------------------
#---------------------- TRABLEAU DE BORD --------------------
#------------------------------------------------------------
@register.filter()
def nombre_ai_total(value):
    """
    Filter : renvoie le nombre total des avis d'impositions enregistrés sur le système
    """
    obj = AvisImposition.objects.all().count()
    if obj:
        return obj

    return value

#------------------------------------------------------------
@register.filter()
def nombre_ni_total(value):
    """
    Filter : renvoie le nombre total des notes d'impositions enregistrés dans le système
    """
    obj = NoteImposition.objects.all().count()
    if obj:
        return obj

    return value

#------------------------------------------------------------
@register.filter()
def nombre_ai_payement(entity_const, is_payed=True):
    """
    Filter : renvoie le nombre total des avis d'impositions payes selon un entity

    ENTITY_ACTIVITE_EXCEPTIONNELLE = 3          # ActiviteExceptionnel (Dans AvisImposition uniquement)
    ENTITY_VISITE_SITE_TOURISTIQUE = 4          # VisiteSiteTouristique (Dans AvisImposition uniquement)
    
    ENTITY_VEHICULE_ACTIVITE = 11               # VehiculeActivite (carte)
    ENTITY_VEHICULE_PROPRIETE = 13              # VehiculeProprietaire (carte)

    ENTITY_ACTIVITE_STANDARD_DUPLICATA = 14     # StandardDuplicata (Dans AvisImposition uniquement)
    ENTITY_ACTIVITE_MARCHE_DUPLICATA = 15       # MarcheDuplicata (Dans AvisImposition uniquement)
    
    ENTITY_VEHICULE_ACTIVITE_DUPLICATA = 16     # VehiculeActiviteDuplicata (Dans AvisImposition uniquement)
    ENTITY_VEHICULE_PROPRIETE_DUPLICATA = 17    # VehiculeProprietaireDuplicata (Dans AvisImposition uniquement)
    """
    nombre = 0

    if entity_const==0:
        return nombre

    query = Q(entity=entity_const)

    if is_payed:
        # PAYEES
        query &= Q(date_validate__isnull=False)
    else:
        # NON PAYEES
        query &= Q(date_validate__isnull=True)

    nombre = AvisImposition.objects.filter(query).count()

    return nombre

#------------------------------------------------------------
@register.filter()
def nombre_ni_payement(entity_const, is_payed=True):
    """
    Filter : renvoie le nombre total des notes d'impositions PAYES OU NON par ENTITY
    
    ENTITY_ACTIVITE_STANDARD = 1                # BaseActivite (réf: Standard)
    ENTITY_ACTIVITE_MARCHE = 2                  # BaseActivite (réf: Marché)
    ENTITY_ALLOCATION_ESPACE_PUBLIQUE = 5       # AllocationEspacePublique
    ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE = 6  # AllocationPanneauPublicitaire
    ENTITY_PUBLICITE_MUR_CLOTURE = 7            # PubliciteMurCloture
    ENTITY_ALLOCATION_PLACE_MARCHE = 8          # Allocation de Place dans le Marche
    ENTITY_IMPOT_FONCIER = 10                   # Impôt foncier (FoncierExpertise)
    ENTITY_VEHICULE_ACTIVITE = 11               # VehiculeActivite
    ENTITY_DROIT_STATIONNEMENT = 12             # VehiculeActivite (!!! Important !!!) : Il depend de l'activité
    ENTITY_VEHICULE_PROPRIETE = 13              # VehiculeProprietaire
    """
    nombre = 0

    if entity_const==0:
        return nombre

    query = Q(entity=entity_const)
        
    if is_payed:
        # PAYEES
        query &= Q(taxe_montant_paye__gte = F("taxe_montant"))
    else:
        # NON PAYEES
        query &= Q(taxe_montant_paye__lt = F("taxe_montant"))
    
    nombre = NoteImposition.objects.filter(query).count()

    return nombre

#------------------------------------------------------------ 
#--------------------- AVIS D'IMPOSITON ---------------------
#------------------------------------------------------------ 
@register.filter()
def ai_recette_entity_not_payed(entity_const):
    """
    Total des recettes des avis d'imposition par ENTITY : NON PAYES

    ENTITY_ACTIVITE_EXCEPTIONNELLE = 3          # ActiviteExceptionnel (Dans AvisImposition uniquement)
    ENTITY_VISITE_SITE_TOURISTIQUE = 4          # VisiteSiteTouristique (Dans AvisImposition uniquement)
    
    ENTITY_VEHICULE_ACTIVITE = 11               # VehiculeActivite (carte)
    ENTITY_VEHICULE_PROPRIETE = 13              # VehiculeProprietaire (carte)

    ENTITY_ACTIVITE_STANDARD_DUPLICATA = 14     # StandardDuplicata (Dans AvisImposition uniquement)
    ENTITY_ACTIVITE_MARCHE_DUPLICATA = 15       # MarcheDuplicata (Dans AvisImposition uniquement)
    
    ENTITY_VEHICULE_ACTIVITE_DUPLICATA = 16     # VehiculeActiviteDuplicata (Dans AvisImposition uniquement)
    ENTITY_VEHICULE_PROPRIETE_DUPLICATA = 17    # VehiculeProprietaireDuplicata (Dans AvisImposition uniquement)
    """
    if entity_const==0:
        return 0

    query = Q(entity=entity_const) & Q(date_paiement__isnull=True)

    queryset = AvisImposition.objects.filter(query).aggregate(somme=Sum('montant_total'))
    somme = queryset.get('somme', 0)
    if not somme:
        return 0

    return int(somme)

#------------------------------------------------------------ 
@register.filter()
def ai_recette_entity_payed(entity_const):
    """
    Total des recettes des avis d'imposition par ENTITY : PAYES

    ENTITY_ACTIVITE_EXCEPTIONNELLE = 3          # ActiviteExceptionnel (Dans AvisImposition uniquement)
    ENTITY_VISITE_SITE_TOURISTIQUE = 4          # VisiteSiteTouristique (Dans AvisImposition uniquement)
    
    ENTITY_VEHICULE_ACTIVITE = 11               # VehiculeActivite (carte)
    ENTITY_VEHICULE_PROPRIETE = 13              # VehiculeProprietaire (carte)

    ENTITY_ACTIVITE_STANDARD_DUPLICATA = 14     # StandardDuplicata (Dans AvisImposition uniquement)
    ENTITY_ACTIVITE_MARCHE_DUPLICATA = 15       # MarcheDuplicata (Dans AvisImposition uniquement)
    
    ENTITY_VEHICULE_ACTIVITE_DUPLICATA = 16     # VehiculeActiviteDuplicata (Dans AvisImposition uniquement)
    ENTITY_VEHICULE_PROPRIETE_DUPLICATA = 17    # VehiculeProprietaireDuplicata (Dans AvisImposition uniquement)
    """
    if entity_const==0:
        return 0

    query = Q(entity=entity_const) & Q(date_paiement__isnull=False)

    queryset = AvisImposition.objects.filter(query).aggregate(somme=Sum('montant_total'))
    somme = queryset.get('somme', 0)
    if not somme:
        return 0

    return int(somme)

#------------------------------------------------------------ 
#--------------------- NOTES D'IMPOSITON --------------------
#------------------------------------------------------------ 
@register.filter()
def ni_recette_entity_payed(entity_const):
    """
    Total des recettes des notes d'imposition de transport par ENTITY PAYES

    ENTITY_ACTIVITE_STANDARD = 1                # BaseActivite (réf: Standard)
    ENTITY_ACTIVITE_MARCHE = 2                  # BaseActivite (réf: Marché)
    ENTITY_ALLOCATION_ESPACE_PUBLIQUE = 5       # AllocationEspacePublique
    ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE = 6  # AllocationPanneauPublicitaire
    ENTITY_PUBLICITE_MUR_CLOTURE = 7            # PubliciteMurCloture
    ENTITY_ALLOCATION_PLACE_MARCHE = 8          # Allocation de Place dans le Marche
    ENTITY_IMPOT_FONCIER = 10                   # Impôt foncier (FoncierExpertise)
    ENTITY_VEHICULE_ACTIVITE = 11               # VehiculeActivite
    ENTITY_DROIT_STATIONNEMENT = 12             # VehiculeActivite (!!! Important !!!) : Il depend de l'activité
    ENTITY_VEHICULE_PROPRIETE = 13              # VehiculeProprietaire
    """
    if entity_const==0:
        return 0

    query = Q(entity=entity_const) & Q(taxe_montant_paye__gte=0)

    queryset = NoteImposition.objects.filter(query).aggregate(somme=Sum('taxe_montant_paye'))
    somme = queryset.get('somme', 0)
    if not somme:
        return 0

    return int(somme)

#------------------------------------------------------------ 
@register.filter()
def ni_recette_entity_not_payed(entity_const):
    """
    Total des recettes des notes d'imposition par ENTITY NON PAYES

    ENTITY_ACTIVITE_STANDARD = 1                # BaseActivite (réf: Standard)
    ENTITY_ACTIVITE_MARCHE = 2                  # BaseActivite (réf: Marché)
    ENTITY_ALLOCATION_ESPACE_PUBLIQUE = 5       # AllocationEspacePublique
    ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE = 6  # AllocationPanneauPublicitaire
    ENTITY_PUBLICITE_MUR_CLOTURE = 7            # PubliciteMurCloture
    ENTITY_ALLOCATION_PLACE_MARCHE = 8          # Allocation de Place dans le Marche
    ENTITY_IMPOT_FONCIER = 10                   # Impôt foncier (FoncierExpertise)
    ENTITY_VEHICULE_ACTIVITE = 11               # VehiculeActivite
    ENTITY_DROIT_STATIONNEMENT = 12             # VehiculeActivite (!!! Important !!!) : Il depend de l'activité
    ENTITY_VEHICULE_PROPRIETE = 13              # VehiculeProprietaire
    """
    if entity_const==0:
        return 0
    
    query = Q(entity=entity_const) & Q(taxe_montant_paye__lte=0)

    queryset = NoteImposition.objects.filter(query).aggregate(somme=Sum('taxe_montant'))
    somme = queryset.get('somme', 0)
    if not somme:
        return 0

    return int(somme)

#------------------------------------------------------------
@register.filter()
def nombre_ai_transport(value):
    """
    Filter : renvoie le nombre total des avis d'impositions des transports enregistrés sur le système
    ENTITY_VEHICULE_ACTIVITE = 6
    ENTITY_DROIT_STATIONNEMENT = 7
    ENTITY_VEHICULE_PROPRIETE = 8
    """
    nombre = 0

    if value==0:
        # Cartes de propriété
        query = Q(entity=ENTITY_VEHICULE_PROPRIETE)
    elif value==1:
        # Cartes de propriété Duplicata
        query = Q(entity=ENTITY_VEHICULE_PROPRIETE_DUPLICATA) 
    elif value==2:
        # Cartes Professionnelles
        query = Q(entity=ENTITY_VEHICULE_ACTIVITE) 
    elif value==3:
        # Cartes Professionnelles Duplicata
        query = Q(entity=ENTITY_VEHICULE_ACTIVITE_DUPLICATA) 
    else:
        # Tous les avis d'imposition de transport
        query = Q(entity=ENTITY_VEHICULE_PROPRIETE) | Q(entity=ENTITY_VEHICULE_PROPRIETE_DUPLICATA) | Q(entity=ENTITY_VEHICULE_ACTIVITE) | Q(entity=ENTITY_VEHICULE_ACTIVITE_DUPLICATA) 
        
    nombre = AvisImposition.objects.filter(query).count()

    return nombre

#------------------------------------------------------------
@register.filter()
def nombre_ni_transport(value):
    """
    Filter : renvoie le nombre total des notes d'impositions de transport enregistrés dans le système
    """
    nombre = 0
    if value==0:
        # taxes sur la propriété
        query = Q(entity=ENTITY_VEHICULE_PROPRIETE) 
    elif value==1:
        # Taxes sur activités de transport rémunéré
        query = Q(entity=ENTITY_VEHICULE_ACTIVITE)
    elif value==2:
        # Droit de stationnement
        query = Q(entity=ENTITY_DROIT_STATIONNEMENT) 
    else:
        # Tous les notes d'imposition de transport
        query = Q(entity=ENTITY_VEHICULE_ACTIVITE) | Q(entity=ENTITY_VEHICULE_PROPRIETE) | Q(entity=ENTITY_DROIT_STATIONNEMENT) 
        
    nombre = NoteImposition.objects.filter(query).count()

    return nombre

#-------------------------------------------------------------
@register.filter()
def get_numero_bordereau(obj_note_paie):
    """
    Renvoyer l'adresse complete 
    Numero parcelle + COMMUNE - ZONE - QUARTIER, rueavenue, police
    """
    res = ''
    if isinstance(obj_note_paie, NoteImpositionPaiement):
        res = obj_note_paie.id

    return res