from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_crm.forms import * 
from mod_crm.models import PersonneMorale
from mod_crm.templates import MoraleTemplate

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_validators import *

from datetime import datetime

#----------------------------------------------------------------
#------------------ CRUD Contribuable morale --------------------
#----------------------------------------------------------------

def get_list_by_criteria(request):
    """
    Renvoie la liste avec criteria
    """
    total = PersonneMorale.objects.count

    # Initialier les variables locales, sesions via variables POST
    matricule = SessionHelpers.init_variables(request, 'pm_matricule')
    nom = SessionHelpers.init_variables(request, 'pm_nom')
    #nif_numero = SessionHelpers.init_variables(request, 'pm_nif_numero')
    rc_numero = SessionHelpers.init_variables(request, 'pm_rc_numero')
    user_create = SessionHelpers.init_variables(request, 'pm_user_create')
    status = SessionHelpers.init_variables(request, 'pm_status')
    
    # Initialier les variables locales, sesions via variables POST pour la période
    du = SessionHelpers.init_variables(request, 'pm_du')
    au = SessionHelpers.init_variables(request, 'pm_au')

    # Définir les parametres de recherche
    query = SessionHelpers.get_query(None, Q(matricule__icontains=matricule)) #Premier parametre à None
    query = SessionHelpers.get_query(query, Q(nom__icontains=nom))
    #query = SessionHelpers.get_query(query, Q(nif_numero__icontains=nif_numero))
    query = SessionHelpers.get_query(query, Q(rc_numero__icontains=rc_numero))
    query = SessionHelpers.get_query(query, Q(user_create__username__icontains=user_create))

    if status=='1': #Valide
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
    elif status=='2': #En attente
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
    elif status=='3': #Brouillon
        query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & (Q(nif_file__exact='') | Q(rc_file__exact='')))

    # Charger la liste
    if query is not None:
        lst = PersonneMorale.objects.filter(query)
        if status=='2':
            lst = lst.exclude(nif_file__exact='').exclude(rc_file__exact='')
    else:
        lst = PersonneMorale.objects.all()
        if status=='2':
            lst = lst.exclude(nif_file__exact='').exclude(rc_file__exact='')

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
    # Lire les notifications
    lst_notification = NotificationHelpers.get_list(request)

    # Charger la liste
    lst, total = get_list_by_criteria(request)
    
    # Sauvegader le context
    context = {
        'total': total,
        'lst': lst,

        'pm_matricule': request.session['pm_matricule'], 
        'pm_nom': request.session['pm_nom'],
        #'pm_nif_numero': request.session['pm_nif_numero'],
        'pm_rc_numero': request.session['pm_rc_numero'],
        'pm_user_create': request.session['pm_user_create'],
        'pm_status': request.session['pm_status'],

        'pm_du': request.session['pm_du'],
        'pm_au': request.session['pm_au'],

        'lst_notification':lst_notification,
        'user' : User.objects.get(pk=request.user.id),
    }

    return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def morale_list(request):
    """
    Afficher la liste des contribuable personne morale
    """
    # Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
    request.session['url_list'] = request.get_full_path()

    return render(request, MoraleTemplate.index, context=get_context(request))

#------------------------------------------------------------
@login_required(login_url="login/")
def morale_create(request):
    """
    Créer les informations d'une personne morale
    """
    if request.method == 'POST':
        form = MoraleForm(request.POST)
    else:
        form = MoraleForm()
    
    return save_morale_form(request, form, MoraleTemplate.create, 'create')

#------------------------------------------------------------
@login_required(login_url="login/")
def morale_update(request, pk):
    """
    Modifier les informations d'une personne morale
    """
    obj = get_object_or_404(PersonneMorale, pk=pk)
    if request.method == 'POST':
        form = MoraleForm(request.POST, instance=obj)
    else:
        form = MoraleForm(instance=obj)

    return save_morale_form(request, form, MoraleTemplate.update, 'update')

#------------------------------------------------------------
@login_required(login_url="login/")
def morale_delete(request, pk):
    """
    Supprimer une personne morale
    """
    obj = get_object_or_404(PersonneMorale, pk=pk)
    data = dict()
    if request.method == 'POST':
        obj.delete()

        data['form_is_valid'] = True
        data['html_content_list'] = render_to_string(MoraleTemplate.list, context=get_context(request))
        data['url_redirect'] = request.session['url_list']
    else:
        context = {'obj': obj}
        data['html_form'] = render_to_string(MoraleTemplate.delete, context, request=request)
    
    return JsonResponse(data)

#------------------------------------------------------------
def save_morale_form(request, form, template_name, action):
    """
    Sauvegarder les informations de la personne morale (Create/Update)
    """
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            # 18 : Province, 1 : Personne Morale
            msg = OperationsHelpers.execute_action(request, action, form, CHRONO_PERSONNE_MORALE, 'matricule')
            if msg:
                return ErrorsHelpers.show_message(request, msg)

            data['form_is_valid'] = True
            data['html_content_list'] = render_to_string(MoraleTemplate.list, context=get_context(request))
            data['url_redirect'] = request.session['url_list']
        else:
            return ErrorsHelpers.show(request, form)
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    
    return JsonResponse(data)

#------------------------------------------------------------
def morale_upload(request, pk):
    """
    Upload de photo de la personne morale
    """
    obj = get_object_or_404(PersonneMorale, pk=pk)
    data = dict()
    if request.method == 'POST':
        form = ImageUploadMoraleForm(request.POST, request.FILES)
        if form.is_valid():         
            if form.cleaned_data['nif_file'] is not None:
                obj.nif_file = form.cleaned_data['nif_file']
                obj.save()
            if form.cleaned_data['rc_file'] is not None:
                obj.rc_file = form.cleaned_data['rc_file']
                obj.save()          
        return redirect('morale_list')          
    else:
        context = {'obj': obj}
        data['html_form'] = render_to_string(MoraleTemplate.upload, context, request=request)

    return JsonResponse(data)

#------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def morale_validate(request):
    """
    Valider les informations de la personne morale
    """
    ID = request.POST["id"]
    obj = get_object_or_404(PersonneMorale, pk=ID) 

    if obj is None:
        return ErrorsHelpers.show_message(request, "Erreur fondamentale trouvée, veuillez consulter le fournisseur du logiciel")

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

            OperationsHelpers.execute_action_validate(request, obj)        
    except:
        return ErrorsHelpers.show_message(request, 'Erreur de validation.')

    data = dict()
    data['url_redirect'] = request.session['url_list']
    data['html_content_list'] = render_to_string(MoraleTemplate.list, context=get_context(request))

    return JsonResponse(data)