from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_crm.forms import * 
from mod_crm.models import PersonnePhysique
from mod_crm.templates import PhysiqueTemplate

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_validators import *

from datetime import datetime

#----------------------------------------------------------------
#------------------ CRUD Contribuable physique ------------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	# Initialier les variables locales, sesions via variables POST
	matricule = SessionHelpers.init_variables(request, 'pp_matricule')
	nom = SessionHelpers.init_variables(request, 'pp_nom')
	identite = SessionHelpers.init_variables(request, 'pp_identite')
	user_create = SessionHelpers.init_variables(request, 'pp_user_create')
	status = SessionHelpers.init_variables(request, 'pp_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'pp_du')
	au = SessionHelpers.init_variables(request, 'pp_au')
	
	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(matricule__icontains=matricule)) #Premier parametre à None
	query = SessionHelpers.get_query(query, Q(nom__icontains=nom))
	query = SessionHelpers.get_query(query, Q(identite_numero__icontains=identite))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=user_create))
	
	if status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif status=='3': #Brouillon
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & (Q(photo_file__exact='') | Q(identite_file__exact='')))
	
	# Charger la liste
	if query:
		lst = PersonnePhysique.objects.filter(query)
		if status=='2':
			lst = lst.exclude(photo_file__exact='').exclude(identite_file__exact='')
	else:
		lst = PersonnePhysique.objects.all()
		if status=='2':
			lst = lst.exclude(photo_file__exact='').exclude(identite_file__exact='')

	# Si période valide
	if is_date_fr_valid(du) and is_date_fr_valid(au):
		du = date_picker_to_date_string(du)
		au = date_picker_to_date_string(au, True)
	
		#if is_date_valid(du) and is_date_valid(au):
		lst = lst.filter(date_validate__range=[du, au]).order_by('-date_validate')

	return lst

#------------------------------------------------------------
def get_list_paginator(request):
	lst = get_list_by_criteria(request)
	return PaginatorHelpers.get_list_paginator_entity_filter(request, lst)

#------------------------------------------------------------
def get_context(request):
	"""
	Renvoie les info du context
	"""
	# Lire les notifications
	lst_notification = NotificationHelpers.get_list(request)

	# Charger la liste
	lst = get_list_paginator(request)

	# Sauvegader le context
	context = {
		'total': PersonnePhysique.objects.count,
		'lst': lst,
		
		'pp_matricule': request.session['pp_matricule'], 
		'pp_nom': request.session['pp_nom'],
		'pp_identite': request.session['pp_identite'],
		'pp_user_create': request.session['pp_user_create'],
		'pp_status': request.session['pp_status'],

		'pp_du': request.session['pp_du'],
		'pp_au': request.session['pp_au'],
		
		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}
	
	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def physique_list(request):
	"""
	Afficher la liste des contribuable personne physique
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, PhysiqueTemplate.index, context=get_context(request))

#------------------------------------------------------------
@login_required(login_url="login/")
def physique_create(request):
	"""
	Créer les informations d'une personne physique
	"""
	if request.method == 'POST':
		form = PhysiqueForm(request.POST)
	else:
		form = PhysiqueForm()

	return save_physique_form(request, form, PhysiqueTemplate.create, 'create')

#------------------------------------------------------------
@login_required(login_url="login/")
def physique_update(request, pk):
	"""
	Modifier les informations d'une personne physique
	"""
	obj = get_object_or_404(PersonnePhysique, pk=pk)
	if request.method == 'POST':		
		form = PhysiqueForm(request.POST, instance=obj)
	else:	
		form = PhysiqueForm(instance=obj)	
	
	return save_physique_form(request, form, PhysiqueTemplate.update, 'update')

#------------------------------------------------------------
@login_required(login_url="login/")
def physique_delete(request, pk):
	"""
	Supprimer une personne physique
	"""
	obj = get_object_or_404(PersonnePhysique, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True
		data['html_content_list'] = render_to_string(PhysiqueTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(PhysiqueTemplate.delete, context, request=request)
	
	return JsonResponse(data)

#------------------------------------------------------------
def save_physique_form(request, form, template_name, action):
	"""
	Sauvegarder les informations de la personne physique (Create/Update)
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			# 18 : Province, 1 : Personne Morale
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_PERSONNE_PHYSIQUE, 'matricule')
			if msg:
				return ErrorsHelpers.show_message(request, msg)
			
			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(PhysiqueTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	else:
		context = {'form': form}
		data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#------------------------------------------------------------
def physique_upload(request, pk):
	"""
	Upload de photo de la personne physique
	"""
	obj = get_object_or_404(PersonnePhysique, pk=pk)
	if request.method == 'POST':
		form = ImageUploadPhysiqueForm(request.POST, request.FILES)
		if form.is_valid():
			if form.cleaned_data['photo_file'] is not None:
				obj.photo_file = form.cleaned_data['photo_file']
				obj.save()
			if form.cleaned_data['identite_file'] is not None:
				obj.identite_file = form.cleaned_data['identite_file']
				obj.save()
			if form.cleaned_data['nif_file'] is not None:
				obj.nif_file = form.cleaned_data['nif_file']
				obj.save()
			
			return redirect('physique_list')
		else:
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string(PhysiqueTemplate.upload, context, request=request)
	
	return JsonResponse(data)

#------------------------------------------------------------
def physique_upload_temp(request, pk):
	"""
	Upload de photo de la personne physique
	"""
	obj = get_object_or_404(PersonnePhysique, pk=pk)
	if request.method == 'POST':
		form = ImageUploadPhysiqueForm(request.POST, request.FILES)
		if form.is_valid():
			if form.cleaned_data['photo_file'] is not None:
				obj.photo_file = form.cleaned_data['photo_file']
				obj.save()
			if form.cleaned_data['identite_file'] is not None:
				obj.identite_file = form.cleaned_data['identite_file']
				obj.save()
			if form.cleaned_data['nif_file'] is not None:
				obj.nif_file = form.cleaned_data['nif_file']
				obj.save()

			return redirect('physique_list')
		else:
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string('physique/includes/_physique_upload_temp.html', context, request=request)
	
	return JsonResponse(data)

#------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def physique_validate(request):
	"""
	Valider les informations de la personne physique
	"""
	data = dict()
		
	ID = request.POST["id"]	
	obj = get_object_or_404(PersonnePhysique, pk=ID)

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
	data['html_content_list'] = render_to_string(PhysiqueTemplate.list, context=get_context(request))

	return JsonResponse(data)

#----------------------------------------------------------------
#------------------- DATA EXPORT : CSV, XLS ---------------------
#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def physique_export(request):
	"""
	Exporter la liste filtrée (vers CSV et XLS)
	"""
	type_file = request.POST["btn_export"]

	if type_file == 'CSV':
		return ReportHelpers.export_csv(get_list_by_criteria(request), 'Contribuable_personne_phyique')

	if type_file == 'XLS':
		return ReportHelpers.export_xls(get_list_by_criteria(request), 'Contribuable_personne_phyique')

	# Devra renvoyer un message (alert)
	return HttpResponse(status=201)