from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_helpers.models import Chrono
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_validators import *

from mod_transport.models import VehiculeActivite ,Vehicule, VehiculeActiviteArret
from mod_transport.forms import *
from mod_transport.templates import *

from mod_crm.models import *

from mod_finance.models import AvisImposition, NoteImposition, Periode

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#--------------------- CRUD Véhicule Actvité  -------------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
    """
    Renvoie la liste avec criteria
    """
    total = VehiculeActivite.objects.count

    # Initialier les variables locales, sesions via variables POST
    va_numero_activite = SessionHelpers.init_variables(request, 'va_numero_activite')
    va_sous_categorie = SessionHelpers.init_variables(request, 'va_sous_categorie')
    va_modele = SessionHelpers.init_variables(request, 'va_modele')
    va_plaque = SessionHelpers.init_variables(request, 'va_plaque')
    va_chassis = SessionHelpers.init_variables(request, 'va_chassis')
    va_matricule = SessionHelpers.init_variables(request, 'va_matricule')
    va_nom = SessionHelpers.init_variables(request, 'va_nom')
    va_user_create = SessionHelpers.init_variables(request, 'va_user_create')
    va_status = SessionHelpers.init_variables(request, 'va_status')

    # Initialier les variables locales, sesions via variables POST pour la période
    du = SessionHelpers.init_variables(request, 'va_du')
    au = SessionHelpers.init_variables(request, 'va_au')

    # Définir les parametres de recherche
    query = SessionHelpers.get_query(None, Q(numero_activite__icontains=va_numero_activite))
    #query = SessionHelpers.get_query(query, Q(sous_categorie=va_sous_categorie)) #Premier parametre à None
    query = SessionHelpers.get_query(query, Q(vehicule__modele__nom__icontains=va_modele))
    query = SessionHelpers.get_query(query, Q(vehicule__plaque__icontains=va_plaque))
    query = SessionHelpers.get_query(query, Q(vehicule__chassis__icontains=va_chassis))
    query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=va_matricule))
    query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=va_nom))
    query = SessionHelpers.get_query(query, Q(user_create__username__icontains=va_user_create))
   
    if va_status=='1': #Valide
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
    elif va_status=='2': #En attente
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
    elif va_status=='3': #Brouillon
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & (Q(fichier_carterose__exact='') | Q(fichier_autorisation__exact='')))

    # Charger la liste
    if query:
        lst = VehiculeActivite.objects.filter(query)
        if va_status=='2':
            lst = lst.exclude(fichier_carterose__exact='').exclude(fichier_autorisation__exact='')
    else:
        lst = VehiculeActivite.objects.all()
        if va_status=='2':
            lst = lst.exclude(fichier_carterose__exact='').exclude(fichier_autorisation__exact='')

    # Si période valide
    if is_date_fr_valid(du) and is_date_fr_valid(au):
        du = date_picker_to_date_string(du)
        au = date_picker_to_date_string(au, True)
    
        #if is_date_valid(du) and is_date_valid(au):
        lst = lst.filter(date_validate__range=[du, au]).order_by('-date_validate')

    # Renvoyer le résultat de la requete filtrée avec paginator
    return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total

#------------------------------------------------------------
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

        'va_numero_activite': request.session['va_numero_activite'], 
        'va_sous_categorie': request.session['va_sous_categorie'], 
        'va_modele': request.session['va_modele'],
        'va_plaque': request.session['va_plaque'],
        'va_chassis': request.session['va_chassis'],
        'va_matricule': request.session['va_matricule'],
        'va_nom': request.session['va_nom'],
        'va_user_create': request.session['va_user_create'],
        'va_status': request.session['va_status'],

        'va_du': request.session['va_du'],
        'va_au': request.session['va_au'],
        
        'lst_notification':lst_notification,
        'user' : User.objects.get(pk=request.user.id),
    }
    
    return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def vehicule_activite_list(request):
    """
    Liste des activités des véhicules
    """
    # Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
    request.session['url_list'] = request.get_full_path()

    return render(request, VehiculeActiviteTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_activite_create(request):
    """
    Créer/Ajouter une activité d'un véhicule
    """
    if request.method == 'POST':
        form = VehiculeActiviteForm(request.POST)
    else:
        form = VehiculeActiviteForm()

    return save_vehicule_activite_form(request, form, VehiculeActiviteTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_activite_update(request, pk):
    """
    Modification de l'information de l'activité du véhicule
    """
    obj = get_object_or_404(VehiculeActivite, pk=pk)
    if request.method == 'POST':
        form = VehiculeActiviteForm(request.POST, instance=obj)
    else:
        form = VehiculeActiviteForm(instance=obj)
    
    return save_vehicule_activite_form(request, form, VehiculeActiviteTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_activite_delete(request, pk):
    """
    Suppression d'une activité d'un véhicule
    """
    obj = get_object_or_404(VehiculeActivite, pk=pk)
    data = dict()
    if request.method == 'POST':
        obj.delete()

        data['form_is_valid'] = True
        data['html_content_list'] = render_to_string(VehiculeActiviteTemplate.list, context=get_context(request))
        data['url_redirect'] = request.session['url_list']
    else:
        context = {'obj': obj}
        data['html_form'] = render_to_string(VehiculeActiviteTemplate.delete, context, request=request)
    
    return JsonResponse(data)

#----------------------------------------------------------------
def save_vehicule_activite_form(request, form, template_name, action):
    """
    Sauvegarde des informations d'une activité du véhicule
    """
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            msg = OperationsHelpers.execute_action(request, action, form, CHRONO_ACTIVITE_TRANSPORT, 'numero_activite')
            if msg:
                return ErrorsHelpers.show_message(request, msg)

            data['form_is_valid'] = True
            data['html_content_list'] = render_to_string(VehiculeActiviteTemplate.list, context=get_context(request))
            data['url_redirect'] = request.session['url_list']
        else:
            return ErrorsHelpers.show(request, form)

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def vehicule_activite_validate(request):
    """
    Valider les informations de l'activité du véh obj = get_object_or_404(VehiculeActivite, pk=ID)icule
    TRANSACTION :
    - Vehicule activité,
    - Véhicule, 
    """
    # Load l'Objet VehiculeActivite
    ID = request.POST["id"]
    obj = get_object_or_404(VehiculeActivite, pk=ID)
 
    # get current user 
    user = User.objects.get(pk=request.user.id) 

    # get current datetime 
    dateTimeNow = datetime.datetime.now()
    
    try:
        with transaction.atomic():
            if obj.note and obj.date_note:
                arc = NoteArchive()
                arc.entity = EntityHelpers.get_entity_class_name(obj) # Npm de l'entité classe
                arc.entity_id = obj.id
                arc.note = obj.note
                arc.user_note = obj.user_note
                arc.date_note = obj.date_note
                arc.reponse_note = obj.reponse_note
                arc.demande_annulation_validation = obj.demande_annulation_validation
                arc.date_cancel = obj.date_cancel
                arc.user_cancel = obj.user_cancel
                arc.user_create = User.objects.get(pk=request.user.id)
                arc.save()

                # 2 Effacer la trace de la notification
                obj.note = None
                obj.user_note = None
                obj.date_note = None
                obj.reponse_note = None
                obj.demande_annulation_validation = False
                obj.date_cancel = None
                obj.user_cancel = None

            #---------------------------------------------------------------------
            # 1 - Valider l'info du VéhiculeActivite
            OperationsHelpers.execute_action_validate(request, obj)

            #---------------------------------------------------------------------
            # 2 - Mettre à jour l'info du Vehicule en transaction (chassi, contribuable, actif)
            obj_vehicule = Vehicule.objects.get(id=obj.vehicule.id)
            
            obj_vehicule.chassis = obj.chassis
            obj_vehicule.contribuable = obj.contribuable
            obj_vehicule.actif = True

            # Sauvegarder l'objet véhicule
            obj_vehicule.save()

    except IntegrityError as e:
        return ErrorsHelpers.show_message(request, 'Erreur de validation ' + str(e))

    data = dict()
    data['url_redirect'] = request.session['url_list']
    data['html_content_list'] = render_to_string(VehiculeActiviteTemplate.list, context=get_context(request))

    return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def vehicule_activite_ecriture(request):
    """
    Valider les informations de l'activité du véhicule
    TRANSACTION :
    - Note d'imposition : Taxe sur activité,
    - Note d'imposition : Droit de stationnement,
    - Avis d'imposition : Coût de la carte professionelle
    """
    # Load l'Objet VehiculeActivite
    ID = request.POST["id"]
    obj = get_object_or_404(VehiculeActivite, pk=ID)
 
    # Mise en garde : L'objet doit être validé
    if not obj.date_validate:
        return ErrorsHelpers.show_message(request, "Erreur, Vous devez valider cet objet avant de générer les écritures")

    # Mise en garde L'écriture a été déjà générée 
    if obj.date_ecriture:
        return ErrorsHelpers.show_message(request, "Erreur fatale, une écriture a été déjà générée pour cette objet")

    # get current user 
    user = User.objects.get(pk=request.user.id) 

    # get current datetime 
    dateTimeNow = datetime.datetime.now()
    
    try:
        with transaction.atomic():
            #---------------------------------------------------------------------
            #1 - Générer l'écriture de l'objet principal
            OperationsHelpers.execute_action_ecriture(request, obj)

            # Pour les véhicules qui n'exerce pas d'activité sous son propre compte
            if not obj.vehicule.compte_propre:
                if obj.vehicule.sous_categorie.ai_cout_carte_professionnelle.tarif>0:
                    #---------------------------------------------------------------------
                    # 2 - Créer et Valider l'avis d'imposition pour le coût de la carte d'activité professionnelle
                    # Générer le nouveau numéro chrono
                    new_chrono = ChronoHelpers.get_new_num(CHRONO_AVIS_IMPOSITION)
                    obj_chrono = Chrono.objects.get(prefixe = CHRONO_AVIS_IMPOSITION)
                    obj_chrono.last_chrono = new_chrono 
                    obj_chrono.save();
                    
                    # Créer l'objet AvisImposition
                    ai = AvisImposition()

                    # Référence de l'avis d'imposition (chronologique)
                    ai.reference = new_chrono
                    
                    # Contribuable
                    ai.contribuable = obj.contribuable
            
                    # Cout de la carte, Objet taxe (Type : Avis d'imposition)
                    ai.taxe = obj.vehicule.sous_categorie.ai_cout_carte_professionnelle
                    
                    # ai.taxe_montant : Tarif de la taxe (Type : Avis d'imposition) (Formule : tarif * nombre_copie), nombre copie = 1
                    ai.montant_total = ai.taxe_montant = obj.vehicule.sous_categorie.ai_cout_carte_professionnelle.tarif
                    
                    # Entity Modèle : 'VehiculeProprietaire'
                    ai.entity = ENTITY_VEHICULE_ACTIVITE
                    
                    # Identifiant de l'entity : 'VehiculeActivite'
                    ai.entity_id = obj.id

                    # Libellé
                    ai.libelle = 'Carte municipale de transport n°' + obj.numero_activite + ', plaque n°: ' + obj.vehicule.plaque + ' - ' + obj.vehicule.sous_categorie.nom
                    
                    # Traçabilité (date_create est créée depuis le model)
                    ai.user_create = user
                    
                    # Sauvegarder l'avis d'imposition (coût de la carte d'activité)
                    ai.save()

                if obj.vehicule.sous_categorie.taxe_activite.tarif>0:
                    #---------------------------------------------------------------------
                    # 3 - Créer et Valider la note d'imposition (taxe sur l'activité de transport municipal)
                    # Générer le nouveau numéro chrono
                    new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                    obj_chrono = Chrono.objects.get(prefixe = CHRONO_NOTE_IMPOSITION)
                    obj_chrono.last_chrono = new_chrono 
                    obj_chrono.save();

                    # Créer l'objet Note d'imposition pour l'activité de transport
                    ni = NoteImposition()
                    
                    # Référence de la note d'imposition (chronologique)
                    ni.reference = new_chrono
                    
                    # Contribuable
                    ni.contribuable = obj.contribuable

                    # Entity Modèle : 'VehiculeProprietaire'
                    ni.entity = ENTITY_VEHICULE_ACTIVITE
                    
                    # Identifiant de l'entity : 'VehiculeActivite'
                    ni.entity_id = obj.id
                    
                    # Période de paiement
                    # Si période multiple (soit : mensuel, trimestriel, ou annuel), alors localiser la période en cours
                    ni.periode = PeriodeHelpers.getCurrentPeriode(obj.vehicule.sous_categorie.taxe_activite.periode_type)
                    
                    # Année de paiement (Très important pour la gestion des périodes)
                    ni.annee = dateTimeNow.year
                    
                    # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                    ni.taxe = obj.vehicule.sous_categorie.taxe_activite

                    # Montant dû
                    MONTANT_DU = obj.vehicule.sous_categorie.taxe_activite.tarif

                    # Solde de depart
                    if obj.solde_depart>0:
                        MONTANT_DU += obj.solde_depart

                    # Montant total de la taxe à payer (parametre taxe)
                    ni.taxe_montant = MONTANT_DU

                    # Traçabilité (date_create est créée depuis le model)
                    ni.date_update = dateTimeNow
                    ni.date_validate = dateTimeNow
                    
                    ni.user_create = user
                    ni.user_update = user
                    ni.user_validate = user
                    
                    # Sauvegarder la note d'imposition (taxe sur activité)
                    ni.save()
                else:
                    return ErrorsHelpers.show_message(request, "Erreur, le montant de la note d'imposition doit être positif")
    except IntegrityError as e:
        return ErrorsHelpers.show_message(request,  "Erreur de génération de l'écriture " + str(e))

    data = dict()
    data['url_redirect'] = request.session['url_list']
    data['html_content_list'] = render_to_string(VehiculeActiviteTemplate.list, context=get_context(request))

    return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def vehicule_activite_ecriture_externe(request):
    """
    Génération de la note d'imposition de l'une activité externe (temporaire)
    TRANSACTION :
    - Note d'imposition avec Montant : ZERO
    """
    # Load l'Objet VehiculeActivite
    ID = request.POST["id"]
    ANNEE = request.POST["annee"]
    PERIODE_ID = request.POST["periode_id"]

    # Chercher l'objet entity
    obj = get_object_or_404(VehiculeActivite, pk=ID)
 
    # Mise en garde : L'objet doit être validé
    if not obj.date_validate:
        return ErrorsHelpers.show_message(request, "Erreur, Vous devez valider cet objet avant de générer les écritures")

    # get current user 
    user = User.objects.get(pk=request.user.id) 

    # get current datetime 
    dateTimeNow = datetime.datetime.now()
    
    try:
        with transaction.atomic():
            # Pour les véhicules qui n'exerce pas d'activité sous son propre compte
            if not obj.vehicule.compte_propre:
                #---------------------------------------------------------------------
                # 3 - Créer et Valider la note d'imposition (taxe sur l'activité de transport municipal)
                # Générer le nouveau numéro chrono
                new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                obj_chrono = Chrono.objects.get(prefixe = CHRONO_NOTE_IMPOSITION)
                obj_chrono.last_chrono = new_chrono 
                obj_chrono.save();

                # Créer l'objet Note d'imposition pour l'activité de transport
                ni = NoteImposition()
                
                # Référence de la note d'imposition (chronologique)
                ni.reference = new_chrono
                
                # Contribuable
                ni.contribuable = obj.contribuable

                # Entity Modèle : 'VehiculeProprietaire'
                ni.entity = ENTITY_VEHICULE_ACTIVITE
                
                # Identifiant de l'entity : 'VehiculeActivite'
                ni.entity_id = obj.id
                
                # Détécter la période suivante
                next_periode = Periode.objects.get(id=int(PERIODE_ID))
                if next_periode:
                    ni.periode = next_periode

                # Année de paiement (Très important pour la gestion des périodes)
                ni.annee = int(ANNEE)

                # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                ni.taxe = obj.vehicule.sous_categorie.taxe_activite

                # Montant total de la taxe à payer (parametre taxe)
                ni.taxe_montant = 0

                # Traçabilité (date_create est créée depuis le model)
                ni.date_update = dateTimeNow
                ni.date_validate = dateTimeNow
                
                ni.user_create = user
                ni.user_update = user
                ni.user_validate = user
                
                # Sauvegarder la note d'imposition (taxe sur activité)
                ni.save()
    except IntegrityError as e:
        return ErrorsHelpers.show_message(request,  "Erreur de génération de l'écriture " + str(e))

    data = dict()
    data['url_redirect'] = request.session['url_list']
    data['html_content_list'] = render_to_string(VehiculeActiviteTemplate.list, context=get_context(request))

    return JsonResponse(data)

#----------------------------------------------------------------
def vehicule_activite_upload(request, pk):
    """
    Upload du fichier 'CARTE ROSE' pour le véhicule rémunéré
    """
    obj = get_object_or_404(VehiculeActivite, pk=pk)
    if request.method == 'POST':
        form = VehiculeActiviteFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['fichier_carterose'] is not None:
                obj.fichier_carterose = form.cleaned_data['fichier_carterose']
                obj.save()
            if form.cleaned_data['fichier_autorisation'] is not None:
                obj.fichier_autorisation = form.cleaned_data['fichier_autorisation']
                obj.save()
            return redirect('vehicule_activite_list')
        else:
            return ErrorsHelpers.show(request, form)
    else:
        data = dict()
        context = {'obj': obj}
        data['html_form'] = render_to_string(VehiculeActiviteTemplate.upload, context, request=request)

    return JsonResponse(data)

#----------------------------------------------------------------
#---------- PRINT : Impression de la carte d'activité' ----------
#----------------------------------------------------------------

@login_required(login_url="login/")
def vehicule_activite_print(request, pk):
    """
    Mise à jour du numero_carte_physique du modèle VehiculeActivite avant impression
    """
    obj = get_object_or_404(VehiculeActivite, pk=pk)
    if request.method == 'POST':
        form = VehiculeActivitePrintForm(request.POST, instance=obj)
    else:
        form = VehiculeActivitePrintForm(instance=obj) 

    return save_vehicule_activite_form(request, form, VehiculeActiviteTemplate.print, 'update') # 'update' : Mise à jour !!! IMPORTANT !!!

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_activite_print_authorization(request, pk):
    """
    Demander d'autorisation d'impression de la carte (car le nombre MAX_NUMBER est atteint)
    """
    obj = get_object_or_404(VehiculeActivite, pk=pk)
    if request.method == 'POST':
        form = VehiculeActivitePrintAuthorizationForm(request.POST, instance=obj)
    else:
        form = VehiculeActivitePrintAuthorizationForm(instance=obj) 

    return save_vehicule_activite_form(request, form, VehiculeActiviteTemplate.print_authorization, 'update') # 'update' : Mise à jour !!! IMPORTANT !!!

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def vehicule_activite_print_confirm(request, pk):
    """
    Confirmer l'impression de la carte d'activite professionnelle
    """
    data = dict()
    success = 'true'
    message = ''

    try:
        obj = get_object_or_404(VehiculeActivite, pk=pk)
        obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
        if obj and obj_gv and obj.nombre_impression >= int(obj_gv.valeur):
            success = 'false'
            message = "Ereur d'impression, vous n'avez que " + obj_gv.valeur + " essais d'impression. <br> Veuillez demander l'autorisation d'impression auprès de votre supérieur."
    
    except IntegrityError as e: 
        success = 'false'
        message = "Erreur inattendu, " + str(e)
        
    data['success'] = success
    data['html_form'] = message

    return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_activite_print_pdf(request, pk):
    """
    Impression de la carte d'activité professionnelle de transport rémunéré
    """
    # Nom du fichier template html
    filename = 'carte_activite'
    
    obj = VehiculeActivite.objects.get(pk=pk)
    
    obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
    if obj.nombre_impression >= int(obj_gv.valeur):
        # Empecher le download du PDF
        return vehicule_activite_print_confirm(request, pk)
    else:
        if obj and obj.date_validate: # + Payement effectué
            # Action save print
            obj.nombre_impression += 1 

            # Action save print
            OperationsHelpers.execute_action_print(request, obj)    

            try:
                # personne physique:
                obj_pp = PersonnePhysique.objects.get(pk=obj.contribuable.id)
                if obj_pp:
                    # photo d'identité
                    photo_url = 'file://' + settings.MEDIA_ROOT + '/' + obj_pp.photo_file.name  
            except:
                photo_url = '-'

            # Definir le context
            context = {'obj': obj, 'qr_options': ReportHelpers.get_qr_options(), 'qr_data':get_qr_data(obj), 'photo_url':photo_url}

            # Generate PDF
            return ReportHelpers.Render(request, filename, context) 

        return ErrorsHelpers.show_message(request, "Erreur d'impression de la carte d'activité de transport")

#----------------------------------------------------------------
def get_qr_data(obj):
    """
    Composition des données du qr code
    """
    if isinstance(obj, VehiculeActivite):
        return 'ID-card: {} \nMatricule: {} \nNom: {} \nMarque: {} \nPlaque: {} \nChassis: {} \nCatégorie: {} \nValidé: {}'.format(
            obj.numero_activite, 
            obj.contribuable.matricule,
            obj.contribuable.nom,
            obj.vehicule.modele.nom,
            obj.vehicule.plaque,
            obj.vehicule.chassis,
            obj.vehicule.sous_categorie.nom,
            obj.user_print,
            obj.date_validate.strftime('%Y-%m-%d %H:%M:%S'))

    return 'GDAF'

#------------------------------------------------------------
#------------------ DROIT DE STATIONNEMENT ------------------
#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def vehicule_stationnement_list(request):
    """
    Liste des activités des véhicules
    """
    # Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
    request.session['url_list'] = request.get_full_path()

    return render(request, VehiculeStationnementTemplate.index, context=get_context(request))

@login_required(login_url="login/")
def vehicule_activite_print_authorisation(request, pk):
     obj = get_object_or_404(VehiculeActivite, pk=pk)
     obj.nombre_impression = 0
     obj.save()

     request.session['url_list'] = request.get_full_path()
     return render(request, VehiculeActiviteTemplate.index, context=get_context(request))

def vehicule_activite_print_authorisationpr(request, pk):
     obj = get_object_or_404(VehiculeProprietaire, pk=pk)
     obj.nombre_impression = 0
     obj.save()

     request.session['url_list'] = request.get_full_path()
     return render(request, VehiculeActiviteTemplate.index, context=get_context(request))


# ----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_activite_arretEtReouverture(request, pk):
    """
    envoie du formulaire pour effectue l´arret et reouverture de l´activite
    """
    obj = get_object_or_404(VehiculeActivite, pk=pk)
    # get current user
    user = User.objects.get(pk=request.user.id)
    # get current datetime
    dateTimeNow = datetime.datetime.now()
    objac = get_object_or_404(Vehicule, pk=obj.vehicule_id)
    id_periode = ''
    annee = ''
    paid = 0
    monthTopaie = 0
    msg = ''
    # print(dateTimeNow.month)
    # print(dateTimeNow.year)
    print(request)
    getpayement = NoteImposition.objects.filter(entity_id=pk)
    for gtp in getpayement:
        id_periode = gtp.periode_id
        annee = gtp.annee

    data = dict()
    if request.method == 'POST':

        form = ImageUploadArretServiceForm(request.POST, request.FILES)
        if request.POST.get('ouverture'):
            if form.is_valid():
                # copier dans la table historique pour les activite de transport
                objaca = VehiculeActiviteArret()
                objaca.numero_activite = obj.numero_activite
                objaca.date_debut = obj.date_debut
                objaca.chassis = obj.chassis
                objaca.solde_depart = obj.solde_depart
                objaca.fichier_carterose = obj.fichier_carterose
                objaca.fichier_autorisation = obj.fichier_autorisation
                objaca.motif = obj.motif
                objaca.fichier_formulaire_arret = obj.fichier_formulaire_arret
                objaca.numero_carte_physique = obj.numero_carte_physique
                objaca.nombre_impression = obj.nombre_impression
                objaca.date_create = obj.date_create
                objaca.date_update = obj.date_update
                objaca.date_validate = obj.date_validate
                objaca.date_print = obj.date_print
                objaca.note = obj.note
                objaca.date_note = obj.date_note
                objaca.reponse_note = obj.reponse_note
                objaca.demande_annulation_validation = obj.demande_annulation_validation
                objaca.date_cancel = obj.date_cancel
                objaca.date_ecriture = obj.date_ecriture
                objaca.contribuable_id = obj.contribuable_id
                objaca.user_arret_id = obj.user_arret_id
                objaca.user_cancel_id = obj.user_cancel_id
                objaca.user_create_id = obj.user_create_id
                objaca.user_ecriture_id = obj.user_ecriture_id
                objaca.user_note_id = obj.user_note_id
                objaca.user_print_id = obj.user_print_id
                objaca.user_update_id = obj.user_update_id
                objaca.user_validate_id = obj.user_validate_id
                objaca.vehicule_id = obj.vehicule_id
                objaca.save()

                # reunitialiser les champs de la table vehiculeActivite
                obj.fichier_autorisation = form.cleaned_data['fichier_formulaire_arret']
                obj.date_debut = dateTimeNow
                obj.motif = None
                obj.date_fin = None
                obj.fichier_formulaire_arret = None
                obj.user_arret_id = None
                obj.save()

                # mettre le vehicule en activite
                objac.actif = True
                objac.save()
                # print('ouverture des activites')

        else:
            if form.is_valid():
                if form.cleaned_data['fichier_formulaire_arret'] is not None:
                    obj.fichier_formulaire_arret = form.cleaned_data['fichier_formulaire_arret']
                    obj.motif = request.POST.get('motif')
                    obj.date_fin = dateTimeNow
                    obj.user_arret_id = user
                    obj.save()
                    # desactiver le vehicule
                    objac.actif = False
                    objac.save()
                    # print('fermeture des activite')

        return redirect(request.session['url_list'])
        data['html_content_list'] = render_to_string(VehiculeActiviteTemplate.list, context=get_context(request))
        data['url_redirect'] = request.session['url_list']

    else:
        if id_periode < 13 and id_periode != dateTimeNow.month and id_periode < dateTimeNow.month:
            monthTopaie = id_periode - dateTimeNow.month
            if monthTopaie == 1:
                msg = 'vous devez d\'abord payer le mois suivant'
            else:
                msg = 'vous devez d\'abord payer tous  les' + monthTopaie + ' mois suivant'

            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)

        elif id_periode == 13 and dateTimeNow.month > 3:
            if dateTimeNow.month > 6:
                msg = 'vous devez d\'abord payer tous  les trimestres suivant'
            else:
                msg = 'vous devez d\'abord payer cet trimestre'

            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)

        elif id_periode == 14 and dateTimeNow.month > 6:
            if dateTimeNow.month > 9:
                msg = 'vous devez d\'abord payer  tous les trimestres suivant'
            else:
                msg = 'vous devez d\'abord payer cet trimestre'

            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)

        elif id_periode == 15 and dateTimeNow.month > 9:
            msg = 'vous devez d\'abord payer cet trimestre'
            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)

        elif id_periode == 16 and annee != dateTimeNow.year:
            if dateTimeNow.month < 3:
                msg = 'vous devez d\'abord payer cet trimestre'
            else:
                msg = 'vous devez d\'abord payer  tous les trimestres suivant'

            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)

        elif id_periode == 17 and dateTimeNow.month > 6:
            msg = 'vous devez d\'abord payer cet semaistre'
            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)

        elif id_periode == 18 and annee != dateTimeNow.year:
            msg = 'vous devez d\'abord payer cet semaistre'
            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)

        elif id_periode == 19 and annee != dateTimeNow.year:
            msg = 'vous devez d\'abord payer cette annee'
            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)
        
        elif id_periode == 19 and annee != dateTimeNow.year:
            msg = 'vous devez d\'abord payer cette annee'
            context = {'message': msg}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.msgerror, context, request=request)

        else:
            context = {'obj': obj, 'objac': objac}
            data['html_form'] = render_to_string(VehiculeActiviteTemplate.arret, context, request=request)

    return JsonResponse(data)