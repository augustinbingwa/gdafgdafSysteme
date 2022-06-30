from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from mod_foncier.models import FoncierParcelle,FoncierParcelleTransfert
from mod_foncier.forms import *
from mod_foncier.templates import *

from mod_helpers.models import Chrono
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_validators import *

from mod_foncier.models import FoncierParcellePublique
from mod_crm.models import Contribuable

from mod_parametrage.enums import *

#----------------------------------------------------------------
#------ CRUD Gestion d'identification des parcelles privées -----
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = FoncierParcelle.objects.count

	# Initialier les variables locales, sesions via variables POST
	fppv_numero_parcelle = SessionHelpers.init_variables(request, 'fppv_numero_parcelle')
	fppv_commune = SessionHelpers.init_variables(request, 'fppv_commune')
	fppv_zone = SessionHelpers.init_variables(request, 'fppv_zone')
	fppv_quartier = SessionHelpers.init_variables(request, 'fppv_quartier')
	fppv_rue_avenue = SessionHelpers.init_variables(request, 'fppv_rue_avenue')
	fppv_matricule = SessionHelpers.init_variables(request, 'fppv_matricule')
	fppv_nom = SessionHelpers.init_variables(request, 'fppv_nom')
	fppv_user_create = SessionHelpers.init_variables(request, 'fppv_user_create')
	fppv_status = SessionHelpers.init_variables(request, 'fppv_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'fppv_du')
	au = SessionHelpers.init_variables(request, 'fppv_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(numero_parcelle__icontains=fppv_numero_parcelle))
	query = SessionHelpers.get_query(query, Q(adresse__zone__commune__nom__icontains=fppv_commune))
	query = SessionHelpers.get_query(query, Q(adresse__zone__nom__icontains=fppv_zone))
	query = SessionHelpers.get_query(query, Q(adresse__nom__icontains=fppv_quartier))
	query = SessionHelpers.get_query(query, Q(numero_rueavenue__nom__icontains=fppv_rue_avenue))
	query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=fppv_matricule))
	query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=fppv_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=fppv_user_create))

	if fppv_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif fppv_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif fppv_status=='3': #Brouillon
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & (Q(fichier_declaration__exact='')))
	
	# Charger la liste
	if query:
		lst = FoncierParcelle.objects.filter(query)
		if fppv_status=='2':
			lst = lst.exclude(fichier_declaration__exact='')
	else:
		lst = FoncierParcelle.objects.all()
		if fppv_status=='2':
			lst = lst.exclude(fichier_declaration__exact='')

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

		'fppv_numero_parcelle': request.session['fppv_numero_parcelle'],
		'fppv_commune': request.session['fppv_commune'],
		'fppv_zone': request.session['fppv_zone'],
		'fppv_quartier': request.session['fppv_quartier'],
		'fppv_rue_avenue': request.session['fppv_rue_avenue'],
		'fppv_matricule': request.session['fppv_matricule'],
		'fppv_nom': request.session['fppv_nom'],
		'fppv_user_create': request.session['fppv_user_create'],
		'fppv_status': request.session['fppv_status'],

		'fppv_du': request.session['fppv_du'],
		'fppv_au': request.session['fppv_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_parcelle_list(request):
	"""
	Liste des parcelles privée
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, FoncierParcelleTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_parcelle_create(request):
	"""
	Création/Ajout d'une parcelle privée
	"""	
	if request.method == 'POST':
		form = FoncierParcelleForm(request.POST)
	else:
		form = FoncierParcelleForm()

	return save_foncier_parcelle_form(request, form, FoncierParcelleTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_parcelle_update(request, pk):
	"""
    Modification de l'information d'une parcele privée
    """
	obj = get_object_or_404(FoncierParcelle, pk=pk)
	if request.method == 'POST':
		form = FoncierParcelleForm(request.POST, instance=obj)
	else:
		form = FoncierParcelleForm(instance=obj)

	return save_foncier_parcelle_form(request, form, FoncierParcelleTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_parcelle_delete(request, pk):
	"""
    Suppression d'une parcelle privée non valide
    """
	obj = get_object_or_404(FoncierParcelle, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True
		data['html_content_list'] = render_to_string(FoncierParcelleTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(FoncierParcelleTemplate.delete, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
def save_foncier_parcelle_form(request, form, template_name, action):
	"""
    Sauvegarde des informations d'une parcelle privée
    """
	data = dict()
	if request.method == 'POST':		
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_PARCELLE_PRIVE,'numero_parcelle')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(FoncierParcelleTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_parcelle_validate(request):
	"""
	Valider les informations de la parcelle
	"""
	ID = request.POST["id"]
	obj = get_object_or_404(FoncierParcelle, pk=ID)

	if obj is None:
		return ErrorsHelpers.show_message(request, "Erreur fondamentale trouvée, veuillez consulter le fournisseur du logiciel")

	try:
		with transaction.atomic():
			if obj.note and obj.date_note:
				# 1 - Créer l'archive
				arc = NoteArchive()
				arc.entity = EntityHelpers.get_entity_class_name(obj) # Nom de l'entité classe
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

				# 2 - Effacer la trace de la notification
				obj.note = None
				obj.user_note = None
				obj.date_note = None
				obj.reponse_note = None
				obj.demande_annulation_validation = False
				obj.date_cancel = None
				obj.user_cancel = None
		
			OperationsHelpers.execute_action_validate(request, obj)
	except:
		return ErrorsHelpers.show_message(request, 'Erreur de validation')

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(FoncierParcelleTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
def foncier_parcelle_upload(request, pk):
	"""
	Upload des pièces jointes
	"""
	obj = get_object_or_404(FoncierParcelle, pk=pk)
	if request.method == 'POST':
		form = ImageUploadFoncierParcelleForm(request.POST, request.FILES)
		if form.is_valid():			
			if form.cleaned_data['fichier_declaration'] is not None:
				obj.fichier_declaration = form.cleaned_data['fichier_declaration']
				obj.save()					
		
			return redirect('foncier_parcelle_list')
		else:
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string(FoncierParcelleTemplate.upload, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
def foncier_parcelle_upload_temp(request, pk):
	"""
	Upload des pièces jointes
	"""
	obj = get_object_or_404(FoncierParcelle, pk=pk)
	if request.method == 'POST':
		form = ImageUploadFoncierParcelleForm(request.POST, request.FILES)
		if form.is_valid():			
			if form.cleaned_data['fichier_declaration'] is not None:
				obj.fichier_declaration = form.cleaned_data['fichier_declaration']
				obj.save()					
		
			return redirect('foncier_parcelle_list')
		else:
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string('foncier_parcelle/includes/_foncier_parcelle_upload_temp.html', context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_parcelle_change_validation(request, pk):
	"""
    enlevement de validation d'une paercelle
    """
	obj = get_object_or_404(FoncierParcelle, pk=pk)
	obj.date_validate = None
	obj.save()

	request.session['url_list'] = request.get_full_path()

	return render(request, FoncierParcelleTemplate.index, context=get_context(request))
#----------------------------------------------------------------


def parcelle_transfert(request, pk):

    obj1 = get_object_or_404(FoncierParcelle, pk=pk)
    obj = get_object_or_404(Contribuable, pk=obj1.contribuable_id)
    data = dict()
    if request.method == 'POST':
      if request.POST.get('id_contribuable'):
        obj_tr = FoncierParcelleTransfert()
        obj_tr.numero_parcelle=obj1.numero_parcelle
        obj_tr.contribuable_nv=request.POST.get('id_contribuable')
        obj_tr.numero_police=obj1.numero_police
        obj_tr.fichier_declaration=obj1.fichier_declaration
        obj_tr.numero_carte_physique=obj1.numero_carte_physique
        obj_tr.nombre_impression=obj1.nombre_impression
        obj_tr.date_create=obj1.date_create
        obj_tr.date_update=obj1.date_update
        obj_tr.date_validate=obj1.date_validate
        obj_tr.date_print=obj1.date_print
        obj_tr.note=obj1.note
        obj_tr.date_note=obj1.date_note
        obj_tr.reponse_note=obj1.reponse_note
        obj_tr.demande_annulation_validation=obj1.demande_annulation_validation
        obj_tr.date_cancel=obj1.date_cancel
        obj_tr.accessibilite_id=obj1.accessibilite_id
        obj_tr.adresse_id=obj1.adresse_id
        obj_tr.contribuable_exi_id=obj1.contribuable_id
        obj_tr.numero_rueavenue_id=obj1.numero_rueavenue_id
        obj_tr.taxe_id=obj1.taxe_id
        obj_tr.user_cancel_id=obj1.user_cancel_id
        obj_tr.user_create_id=obj1.user_create_id
        obj_tr.user_note_id=obj1.user_note_id
        obj_tr.user_print_id=obj1.user_print_id
        obj_tr.user_update_id=obj1.user_update_id
        obj_tr.user_validate_id=obj1.user_validate_id

        obj_tr.save()
        obj1.contribuable_id=request.POST.get('id_contribuable')
        obj1.date_validate=None
        obj1.fichier_declaration=None
        obj1.user_create_id=request.user.id
        obj1.save()

      request.session['url_list'] = request.get_full_path()
      return render(request, FoncierParcelleTemplate.index, context=get_context(request))

    else:
        context = {'obj': obj,'obj1': obj1}
        data['html_form'] = render_to_string(FoncierParcelleTemplate.transfert_parc, context, request=request)

    return JsonResponse(data)