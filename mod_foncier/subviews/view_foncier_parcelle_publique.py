from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from mod_foncier.models import FoncierParcellePublique
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

from mod_parametrage.enums import *

#----------------------------------------------------------------
#-------------- CRUD Foncier Parcelle Publique  -----------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = FoncierParcellePublique.objects.count

	# Initialier les variables locales, sesions via variables POST
	fppq_numero_parcelle = SessionHelpers.init_variables(request, 'fppq_numero_parcelle')
	fppq_commune = SessionHelpers.init_variables(request, 'fppq_commune')
	fppq_zone = SessionHelpers.init_variables(request, 'fppq_zone')
	fppq_quartier = SessionHelpers.init_variables(request, 'fppq_quartier')
	fppq_occupee = SessionHelpers.init_variables(request, 'fppq_occupee')
	fppq_user_create = SessionHelpers.init_variables(request, 'fppq_user_create')
	fppq_status = SessionHelpers.init_variables(request, 'fppq_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'fppq_du')
	au = SessionHelpers.init_variables(request, 'fppq_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(numero_parcelle__icontains=fppq_numero_parcelle))
	query = SessionHelpers.get_query(query, Q(adresse__zone__commune__nom__icontains=fppq_commune))
	query = SessionHelpers.get_query(query, Q(adresse__zone__nom__icontains=fppq_zone))
	query = SessionHelpers.get_query(query, Q(adresse__nom__icontains=fppq_quartier))
	
	if fppq_occupee == 'True':
		query = SessionHelpers.get_query(query, Q(occupee=True))
	elif fppq_occupee == 'False':
		query = SessionHelpers.get_query(query, Q(occupee=False))

	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=fppq_user_create))

	if fppq_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif fppq_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	
	# Charger la liste
	if query:
		lst = FoncierParcellePublique.objects.filter(query)
	else:
		lst = FoncierParcellePublique.objects.all()

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

		'fppq_numero_parcelle': request.session['fppq_numero_parcelle'],
		'fppq_commune': request.session['fppq_commune'],
		'fppq_zone': request.session['fppq_zone'],
		'fppq_quartier': request.session['fppq_quartier'],
		'fppq_occupee': request.session['fppq_occupee'],
		'fppq_user_create': request.session['fppq_user_create'],
		'fppq_status': request.session['fppq_status'],

		'fppq_du': request.session['fppq_du'],
		'fppq_au': request.session['fppq_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_parcelle_publique_list(request):
	"""
	Liste des des parcelles publiques
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, FoncierParcellePubliqueTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_parcelle_publique_create(request):
	"""
	Création d'une parcelle publique
	"""
	if request.method == 'POST':
		form = FoncierParcellePubliqueForm(request.POST)
	else:
		form = FoncierParcellePubliqueForm()
	
	return save_foncier_parcelle_publique_form(request, form, FoncierParcellePubliqueTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_parcelle_publique_update(request, pk):
	"""
	Modification d'une parcelle publique
	"""
	obj = get_object_or_404(FoncierParcellePublique, pk=pk)
	if request.method == 'POST':
		form = FoncierParcellePubliqueForm(request.POST, instance=obj)
	else:
		form = FoncierParcellePubliqueForm(instance=obj)
	
	return save_foncier_parcelle_publique_form(request, form, FoncierParcellePubliqueTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_parcelle_publique_delete(request, pk):
	"""
	Suppression d'une parcelle publique
	"""
	obj = get_object_or_404(FoncierParcellePublique, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True		    
		data['html_content_list'] = render_to_string(FoncierParcellePubliqueTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(FoncierParcellePubliqueTemplate.delete, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
def save_foncier_parcelle_publique_form(request, form, template_name, action):
	"""
    Sauvegarde des informations de l'parcelle publique
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_PARCELLE_PUBLIQUE, 'numero_parcelle')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(FoncierParcellePubliqueTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_parcelle_publique_validate(request):
	"""
	Validation des informations de la parcelle publique
	"""
	# Récuperer l'identifiant de la parcelle publique
	ID = request.POST["id"]
	obj = get_object_or_404(FoncierParcellePublique, pk=ID)

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
		return ErrorsHelpers.show_message(request, 'Erreur de validation')

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(FoncierParcellePubliqueTemplate.list, context=get_context(request))
	
	return JsonResponse(data)