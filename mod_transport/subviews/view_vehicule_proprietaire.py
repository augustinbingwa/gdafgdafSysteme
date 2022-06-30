from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_transport.models import VehiculeProprietaire
from mod_transport.forms import * 
from mod_transport.templates import *

from mod_helpers.models import Chrono
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_validators import *

from mod_finance.models import *
from mod_crm.models import *

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#--- CRUD : Carte de Propriétaire de véhicule sans carte rose ---
#----------------------------------------------------------------
def get_list_by_criteria(request):
    """
    Renvoie la liste avec criteria
    """
    total = VehiculeProprietaire.objects.count

    # Initialier les variables locales, sesions via variables POST
    vp_numero_carte = SessionHelpers.init_variables(request, 'vp_numero_carte')
    vp_modele = SessionHelpers.init_variables(request, 'vp_modele')
    vp_plaque = SessionHelpers.init_variables(request, 'vp_plaque')
    vp_chassis = SessionHelpers.init_variables(request, 'vp_chassis')
    vp_matricule = SessionHelpers.init_variables(request, 'vp_matricule')
    vp_nom = SessionHelpers.init_variables(request, 'vp_nom')
    vp_user_create = SessionHelpers.init_variables(request, 'vp_user_create')
    vp_status = SessionHelpers.init_variables(request, 'vp_status')

    # Initialier les variables locales, sesions via variables POST pour la période
    du = SessionHelpers.init_variables(request, 'vp_du')
    au = SessionHelpers.init_variables(request, 'vp_au')

    # Définir les parametres de recherche
    query = SessionHelpers.get_query(None, Q(numero_carte__icontains=vp_numero_carte))
    query = SessionHelpers.get_query(query, Q(vehicule__modele__nom__icontains=vp_modele))
    query = SessionHelpers.get_query(query, Q(vehicule__plaque__icontains=vp_plaque))
    query = SessionHelpers.get_query(query, Q(vehicule__chassis__icontains=vp_chassis))
    query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=vp_matricule))
    query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=vp_nom))
    query = SessionHelpers.get_query(query, Q(user_create__username__icontains=vp_user_create))

    if vp_status=='1': #Valide
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
    elif vp_status=='2': #En attente
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))

    # Charger la liste
    if query:
        lst = VehiculeProprietaire.objects.filter(query)
    else:
        lst = VehiculeProprietaire.objects.all()

    # Si période valide
    if is_date_fr_valid(du) and is_date_fr_valid(au):
        du = date_picker_to_date_string(du)
        au = date_picker_to_date_string(au, True)
    
        #if is_date_valid(du) and is_date_valid(au):
        lst = lst.filter(date_validate__range=[du, au]).order_by('-date_validate')

    # Renvoyer le résultat de la requete filtrée avec paginator
    return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total

#----------------------------------------------------------------
def get_context(request):
    """
    Renvoie les info du context
    """
    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    # Charger la liste
    lst, total = get_list_by_criteria(request)

    # Sauvegader le context
    context = {
        'total': total,
        'lst': lst,

        'vp_numero_carte': request.session['vp_numero_carte'],
        'vp_modele': request.session['vp_modele'],
        'vp_plaque': request.session['vp_plaque'],
        'vp_chassis': request.session['vp_chassis'],
        'vp_matricule': request.session['vp_matricule'],
        'vp_nom': request.session['vp_nom'],
        'vp_user_create': request.session['vp_user_create'],
        'vp_status': request.session['vp_status'],

        'vp_du': request.session['vp_du'],
        'vp_au': request.session['vp_au'],

        'lst_notification':lst_notification,
        'user' : User.objects.get(pk=request.user.id),
    }

    return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def vehicule_proprietaire_list(request):
    """
    Liste des cartes de propriétaire des véhicules
    """
    # Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
    request.session['url_list'] = request.get_full_path()

    return render(request, VehiculeProprietaireTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_update(request, pk):
    """
    Modification des informations de la carte de propriétaire
    """
    obj = get_object_or_404(VehiculeProprietaire, pk=pk)
    if request.method == 'POST':
        form = VehiculeProprietaireForm(request.POST, instance=obj)
    else:
        form = VehiculeProprietaireForm(instance=obj) 

    return save_vehicule_proprietaire_form(request, form, VehiculeProprietaireTemplate.update, 'update')

#----------------------------------------------------------------
def save_vehicule_proprietaire_form(request, form, template_name, action):
    """
    Sauvegarde des informations de la carte de propriétaire
    """
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            msg = OperationsHelpers.execute_action(request, action, form, CHRONO_CARTE_PROPRIETE, 'numero_carte')
            if msg:
                return ErrorsHelpers.show_message(request, msg)

            data['form_is_valid'] = True
            data['html_content_list'] = render_to_string(VehiculeProprietaireTemplate.list, context=get_context(request))
            data['url_redirect'] = request.session['url_list']
        else:
            return ErrorsHelpers.show(request, form)
    
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    
    return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def vehicule_proprietaire_ecriture(request):
    """
    Valider les informations du véhicule
    TRANSACTION : Créer l'avis et note d'imposition
    """
    # Load l'Objet VehiculeProprietaire
    ID = request.POST["id"]
    obj = get_object_or_404(VehiculeProprietaire, pk=ID)

    # get current user 
    user = User.objects.get(pk=request.user.id) 

    # get current datetime 
    dateTimeNow = datetime.datetime.now()

    try:
        with transaction.atomic():
            #---------------------------------------------------------------------
            # 1 - Générer l'écriture de l'objet principal
            OperationsHelpers.execute_action_ecriture(request, obj)

            if obj.vehicule.sous_categorie.ai_cout_carte_propriete.tarif>0:
                #---------------------------------------------------------------------
                # 2 - Créer et Valider l'avis d'imposition pour le coût de la carte de propriétaire
                # Générer le nouveau numéro chrono
                new_chrono = ChronoHelpers.get_new_num(CHRONO_AVIS_IMPOSITION)
                obj_chrono = Chrono.objects.get(prefixe = CHRONO_AVIS_IMPOSITION)
                obj_chrono.last_chrono = new_chrono 
                obj_chrono.save();
                
                # Créer le l'objet AvisImposition
                ai = AvisImposition()

                # Référence de l'avis d'imposition (chronologique)
                ai.reference = new_chrono
                
                # Contribuable
                ai.contribuable = obj.contribuable
        
                # Cout de la carte, Objet taxe (Type : Avis d'imposition)
                ai.taxe = obj.vehicule.sous_categorie.ai_cout_carte_propriete
                
                # ai.taxe_montant : Tarif de la taxe (Type : Avis d'imposition) (Formule : tarif * nombre_copie), nombre copie = 1
                ai.montant_total = ai.taxe_montant = obj.vehicule.sous_categorie.ai_cout_carte_propriete.tarif
                
                # Entity Modèle : 'VehiculeProprietaire'
                ai.entity = ENTITY_VEHICULE_PROPRIETE
                
                # Identifiant de l'entity : 'VehiculeProprietaire'
                ai.entity_id = obj.id

                # Libellé
                ai.libelle = 'Carte de propriété n°' + obj.numero_carte + ', Vélo/vélo-moteur n°: ' + obj.vehicule.plaque + ' - ' + obj.vehicule.sous_categorie.nom
                
                # Traçabilité (date_create est créée depuis le model)
                ai.user_create = user
                
                # Sauvegarder l'avis d'imposition (coût de la carte de propriété)
                ai.save()

            if obj.vehicule.sous_categorie.taxe_proprietaire:
                #---------------------------------------------------------------------
                # 3 - Créer et Valider la note d'imposition (taxe sur le proriétaire)
                # Générer le nouveau numéro chrono
                new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                obj_chrono = Chrono.objects.get(prefixe = CHRONO_NOTE_IMPOSITION)
                obj_chrono.last_chrono = new_chrono 
                obj_chrono.save();

                # Créer l'objet Note d'imposition
                ni = NoteImposition()
                
                # Référence de la note d'imposition (chronologique)
                ni.reference = new_chrono
                
                # Contribuable
                ni.contribuable = obj.contribuable

                # Entity Modèle : 'VehiculeProprietaire'
                ni.entity = ENTITY_VEHICULE_PROPRIETE
                
                # Identifiant de l'entity : 'VehiculeProprietaire'
                ni.entity_id = obj.id
                
                # Période de paiement
                ni.periode = PeriodeHelpers.getCurrentPeriode(obj.vehicule.sous_categorie.taxe_proprietaire.periode_type)

                # Année de paiement (Très important pour la gestion des périodes)
                ni.annee = dateTimeNow.year
                
                 # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                ni.taxe = obj.vehicule.sous_categorie.taxe_proprietaire

                # Montant total de la taxe à payer (parametre taxe)
                ni.taxe_montant = obj.vehicule.sous_categorie.taxe_proprietaire.tarif

                # Traçabilité (date_create est créée depuis le model)
                ni.date_update = dateTimeNow
                ni.date_validate = dateTimeNow
                
                ni.user_create = user
                ni.user_update = user
                ni.user_validate = user
                
                # Sauvegarder la note d'imposition (taxe sur le propriétaire)
                ni.save()
            else:
                return ErrorsHelpers.show_message(request, "Erreur, le montant de la note d'imposition doit être positif")
    except IntegrityError as e:
        return ErrorsHelpers.show_message(request, "Erreur de génération de l'écriture " + str(e))

    data = dict()
    data['url_redirect'] = request.session['url_list']
    data['html_content_list'] = render_to_string(VehiculeProprietaireTemplate.list, context=get_context(request))

    return JsonResponse(data)

#----------------------------------------------------------------
#---------- PRINT : Impression de la carte de propriété ---------
#----------------------------------------------------------------

@login_required(login_url="login/")
def vehicule_proprietaire_print(request, pk):
    """
    Mise à jour du numero_carte_physique du modèle VehiculeProprietaire avant impression
    """
    obj = get_object_or_404(VehiculeProprietaire, pk=pk)
    if request.method == 'POST':
        form = VehiculeProprietairePrintForm(request.POST, instance=obj)
    else:
        form = VehiculeProprietairePrintForm(instance=obj) 

    return save_vehicule_proprietaire_form(request, form, VehiculeProprietaireTemplate.print, 'update') # 'update' : Mise à jour !!! IMPORTANT !!!

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_print_authorization(request, pk):
    """
    Demander d'autorisation d'impression de la carte (car le nombre MAX_NUMBER est atteint)
    """
    obj = get_object_or_404(VehiculeProprietaire, pk=pk)
    if request.method == 'POST':
        form = VehiculeProprietairePrintAuthorizationForm(request.POST, instance=obj)
    else:
        form = VehiculeProprietairePrintAuthorizationForm(instance=obj) 

    return save_vehicule_proprietaire_form(request, form, VehiculeProprietaireTemplate.print_authorization, 'update') # 'update' : Mise à jour !!! IMPORTANT !!!

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def vehicule_proprietaire_print_confirm(request, pk):
    """
    Confirmer l'impression de la carte de proprietaire du véhicule
    """
    data = dict()
    success = 'true'
    message = ''

    try:
        obj = get_object_or_404(VehiculeProprietaire, pk=pk)
        obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
        if obj and obj_gv and obj.nombre_impression >= int(obj_gv.valeur):
            success = 'false'
            message = "Ereur d'impression, vous n'avez que 3 essais d'impression. <br> Veuillez demander l'autorisation d'impression auprès de votre supérieur."
    except IntegrityError as e:    
        success = 'false'
        message = "Erreur inattendu, " + str(e)

    data['success'] = success
    data['html_form'] = message

    return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_print_pdf(request, pk):
    """
    Impression de la carte de proprietaire des véhicules sans carte rose (après cnofirmation)
    """
    # Nom du fichier template html
    filename = 'carte_proprietaire'

    obj = VehiculeProprietaire.objects.get(pk=pk)

    obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
    if obj.nombre_impression >= int(obj_gv.valeur):
        # Empecher le download du PDF
        return vehicule_proprietaire_print_confirm(request, pk)
    else:
        if obj and obj.date_validate: # + Payement effectué
            # Action save print
            obj.nombre_impression += 1 

            OperationsHelpers.execute_action_print(request, obj)   
        
            try:
                # personne physique:
                obj_pp = PersonnePhysique.objects.get(pk=obj.contribuable.id)
                if obj_pp:
                    # photo d'identité
                    photo_url = 'file://' + settings.MEDIA_ROOT + '/' + obj_pp.photo_file.name    
            except:
                photo_url = ''

            # Definir le context
            context = {'obj': obj, 'qr_options': ReportHelpers.get_qr_options(), 'qr_data':get_qr_data(obj), 'photo_url':photo_url}

            # Generate PDF
            return ReportHelpers.Render(request, filename, context) 

        return ErrorsHelpers.show_message(request, "Erreur d'impression de la carte de propriétaire")

#----------------------------------------------------------------
def get_qr_data(obj):
    """
    Composition des données du qr code
    """
    if isinstance(obj, VehiculeProprietaire):
        return 'ID-card: {} \nMatricule: {} \nNom: {} \nMarque: {} \nPlaque: {} \nChassis: {} \nCatégorie: {} \nValidé: {}'.format(
            obj.numero_carte, 
            obj.contribuable.matricule,
            obj.contribuable.nom,
            obj.vehicule.modele.nom,
            obj.vehicule.plaque,
            obj.vehicule.chassis,
            obj.vehicule.sous_categorie.nom,
            obj.date_validate.strftime('%Y-%m-%d %H:%M:%S'))

    return 'GDAF'