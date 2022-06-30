from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_transport.models import *
from mod_transport.submodels.model_vehicule_parametrage import *
from mod_transport.subforms.form_vehicule import *
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

from mod_finance.models import AvisImposition, NoteImposition

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#--------------------------- CRUD Véhicule ----------------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
    """
    Renvoie la liste avec criteria
    """
    total = Vehicule.objects.count

    # Initialier les variables locales, sesions via variables POST
    v_sous_categorie = SessionHelpers.init_variables(request, 'v_sous_categorie')
    v_modele = SessionHelpers.init_variables(request, 'v_modele')
    v_plaque = SessionHelpers.init_variables(request, 'v_plaque')
    v_chassis = SessionHelpers.init_variables(request, 'v_chassis')
    v_matricule = SessionHelpers.init_variables(request, 'v_matricule')
    v_nom = SessionHelpers.init_variables(request, 'v_nom')
    v_user_create = SessionHelpers.init_variables(request, 'v_user_create')
    v_status = SessionHelpers.init_variables(request, 'v_status')

    # Initialier les variables locales, sesions via variables POST pour la période
    du = SessionHelpers.init_variables(request, 'v_du')
    au = SessionHelpers.init_variables(request, 'v_au')

    # Définir les parametres de recherche
    #query = SessionHelpers.get_query(None, Q(sous_categorie=v_sous_categorie)) #Premier parametre à None
    query = SessionHelpers.get_query(None, Q(modele__nom__icontains=v_modele))
    query = SessionHelpers.get_query(query, Q(plaque__icontains=v_plaque))
    query = SessionHelpers.get_query(query, Q(chassis__icontains=v_chassis))
    query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=v_matricule))
    query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=v_nom))
    query = SessionHelpers.get_query(query, Q(user_create__username__icontains=v_user_create))
   
    if v_status=='1': #Valide
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
    elif v_status=='2': #En attente
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
    elif v_status=='3': #Brouillon
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & Q(fichier_carterose__exact=''))
    
    # Charger la liste
    if query:
        lst = Vehicule.objects.filter(query)
        if v_status=='2':
            lst = lst.exclude(fichier_carterose__exact='')
    else:
        lst = Vehicule.objects.all()
        if v_status=='2':
            lst = lst.exclude(fichier_carterose__exact='')

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

        'v_sous_categorie': request.session['v_sous_categorie'], 
        'v_modele': request.session['v_modele'],
        'v_plaque': request.session['v_plaque'],
        'v_chassis': request.session['v_chassis'],
        'v_matricule': request.session['v_matricule'],
        'v_nom': request.session['v_nom'],
        'v_user_create': request.session['v_user_create'],
        'v_status': request.session['v_status'],
        
        'v_du': request.session['v_du'],
        'v_au': request.session['v_au'],

        'lst_notification':lst_notification,
        'user' : User.objects.get(pk=request.user.id),
    }
    
    return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def vehicule_list(request):
    """
    Liste des véhicules
    """
    # Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
    request.session['url_list'] = request.get_full_path()
    
    return render(request, VehiculeTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_create(request):
    """
    Créer/Ajouter un véhicule
    """
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
    else:
        form = VehiculeForm()

    return save_vehicule_form(request, form, VehiculeTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_update(request, pk):
    """
    Modification de l'information du véhicule
    """
    obj = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=obj)
    else:
        form = VehiculeForm(instance=obj)
    
    return save_vehicule_form(request, form, VehiculeTemplate.update, 'update')


@login_required(login_url="login/")
def vehicule_arret_create(request, pk):
    """
    Modification de l'information du véhicule
    """
    obj = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=obj)
    else:
        form = VehiculeForm(instance=obj)

    return save_vehicule_form(request, form, VehiculeTemplate.arret, 'createar')

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_delete(request, pk):
    """
    Suppression d'un véhicule non valide
    """
    obj = get_object_or_404(Vehicule, pk=pk)
    data = dict()
    if request.method == 'POST':
        obj.delete()

        data['form_is_valid'] = True
        data['html_content_list'] = render_to_string(VehiculeTemplate.list, context=get_context(request))
        data['url_redirect'] = request.session['url_list']
    else:
        context = {'obj': obj}
        data['html_form'] = render_to_string(VehiculeTemplate.delete, context, request=request)
    
    return JsonResponse(data)

#----------------------------------------------------------------
def save_vehicule_form(request, form, template_name, action):
    """
    Sauvegarde des informations du véhicule
    """
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            #Enregistrer le numéro de la plaque pour les véhicule sans carte rose dans CHRONO
            msg = OperationsHelpers.execute_action(request, action, form)
            if msg:
                return ErrorsHelpers.show_message(request, msg)

            data['form_is_valid'] = True
            data['html_content_list'] = render_to_string(VehiculeTemplate.list, context=get_context(request))
            data['url_redirect'] = request.session['url_list']
        else:
            return ErrorsHelpers.show(request, form)

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def vehicule_validate(request):
    """
    Valider les informations du véhicule
    TRANSACTION : On crée un titre de propriété si le véhicule n'a pas de plaque d'immatriculation
    cas : Vélo/Vélo Moteur
    ATTENTION : Pour les véhicules
    """
    # Load l'Objet Vehicule
    ID = request.POST["id"]
    obj = get_object_or_404(Vehicule, pk=ID)

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
            # 1 - Valider l'info du véhicule
            OperationsHelpers.execute_action_validate(request, obj)
            
            # Pour les véhicule ayant le titre de propriétaire (Vélo, Vélo moteur, Taxi vélo)
            if not obj.sous_categorie.has_plaque:
                #---------------------------------------------------------------------
                # 2 - Créer et valider le titre de propriété pour ce vehicule sans plaque d'immatriculation 
                # Générer le nouveau numéro chrono
                new_chrono_ca = ChronoHelpers.get_new_num(CHRONO_CARTE_PROPRIETE_VEHICULE)
                obj_chrono = Chrono.objects.get(prefixe = CHRONO_CARTE_PROPRIETE_VEHICULE)
                obj_chrono.last_chrono = new_chrono_ca 
                obj_chrono.save();

                # Gestion de l'objet titre de propriété (Créer et valider l'objet titre en même temps que le véhicule)
                obj_v_titre = VehiculeProprietaire()
                obj_v_titre.vehicule = obj
                obj_v_titre.contribuable = obj.contribuable
                obj_v_titre.numero_carte = new_chrono_ca

                # Traçabilité # Traçabilité (date_create est créée depuis le model)
                obj_v_titre.date_update = dateTimeNow
                obj_v_titre.date_validate = dateTimeNow
                
                obj_v_titre.user_create = user
                obj_v_titre.user_update = user
                obj_v_titre.user_validate = user

                # Sauvegarder le titre de propriétaire
                obj_v_titre.save()
    except IntegrityError as e:
        return ErrorsHelpers.show_message(request, 'Erreur de validation ' + str(e))

    data = dict()
    data['url_redirect'] = request.session['url_list']
    data['html_content_list'] = render_to_string(VehiculeTemplate.list, context=get_context(request))

    return JsonResponse(data)

#----------------------------------------------------------------
def vehicule_upload(request, pk):
    """
    Upload du fichier 'CARTE ROSE' du véhicule rémunéré
    """
    obj = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = CarteRoseFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['fichier_carterose'] is not None:
                obj.fichier_carterose = form.cleaned_data['fichier_carterose']
                obj.save()
            return redirect('vehicule_list')
        else:
            return ErrorsHelpers.show(request, form)
    else:
        data = dict()
        context = {'obj': obj}
        data['html_form'] = render_to_string(VehiculeTemplate.upload, context, request=request)

    return JsonResponse(data)

#----------------------------------------------------------------
def vehicule_upload_temp(request, pk):
    """
    Upload du fichier 'CARTE ROSE' du véhicule rémunéré
    """
    obj = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = CarteRoseFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['fichier_carterose'] is not None:
                obj.fichier_carterose = form.cleaned_data['fichier_carterose']
                obj.save()
            return redirect('vehicule_list')
        else:
            return ErrorsHelpers.show(request, form)
    else:
        data = dict()
        context = {'obj': obj}
        data['html_form'] = render_to_string('vehicule/include/_vehicule_upload_temp.html', context, request=request)

    return JsonResponse(data)