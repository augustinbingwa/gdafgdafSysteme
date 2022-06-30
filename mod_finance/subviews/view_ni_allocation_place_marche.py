from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_validators import *

from mod_finance.models import NoteImposition
from mod_finance.forms import *
from mod_finance.templates import *

from mod_activite.models import *

from mod_parametrage.enums import *

#----------------------------------------------------------------
#CRUD - Note d'imposition pour allocation de place dans le marché
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	ni_query = Q(taxe__categorie_taxe__type_impot = 1) & Q(entity = ENTITY_ALLOCATION_PLACE_MARCHE)
	lst = NoteImposition.objects.filter(ni_query).order_by('-reference')

	total = lst.count

	# Initialier les variables locales, sesions via variables POST
	ni_apm_reference = SessionHelpers.init_variables(request, 'ni_apm_reference')
	ni_apm_numero_place = SessionHelpers.init_variables(request, 'ni_apm_numero_place')
	ni_apm_nom_marche = SessionHelpers.init_variables(request, 'ni_apm_nom_marche')
	ni_apm_matricule = SessionHelpers.init_variables(request, 'ni_apm_matricule')
	ni_apm_nom = SessionHelpers.init_variables(request, 'ni_apm_nom')
	ni_apm_user_create = SessionHelpers.init_variables(request, 'ni_apm_user_create')
	ni_apm_status = SessionHelpers.init_variables(request, 'ni_apm_status')
	ni_apm_paiement = SessionHelpers.init_variables(request, 'ni_apm_paiement')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'ni_apm_du')
	au = SessionHelpers.init_variables(request, 'ni_apm_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(reference__icontains=ni_apm_reference))
	query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=ni_apm_matricule))
	query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=ni_apm_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=ni_apm_user_create))

	if ni_apm_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif ni_apm_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))

	if ni_apm_paiement=='1': #Payé
		query = SessionHelpers.get_query(query, Q(taxe_montant=F('taxe_montant_paye')))
	elif ni_apm_paiement=='2': #Non payé
		query = SessionHelpers.get_query(query, Q(taxe_montant__gt=F('taxe_montant_paye')))

	# Charger la liste
	if query:
		lst = lst.filter(query)

	# Si période valide
	if is_date_fr_valid(du) and is_date_fr_valid(au):
		du = date_picker_to_date_string(du)
		au = date_picker_to_date_string(au, True)
	
		#if is_date_valid(du) and is_date_valid(au):
		lst = lst.filter(date_validate__range=[du, au]).order_by('-date_validate')

	lst = lst.extra(select={'caution_montant':'mod_activite_allocationplacemarche.caution_montant',
							'numero_place' : 'mod_activite_droitplacemarche.numero_place',
							'nom_marche': 'mod_activite_nommarche.nom'},
					tables=["mod_activite_allocationplacemarche", "mod_activite_droitplacemarche", "mod_activite_nommarche"], 
					where =["mod_finance_noteimposition.entity_id = mod_activite_allocationplacemarche.id",
					"mod_activite_allocationplacemarche.droit_place_marche_id = mod_activite_droitplacemarche.id",
					"mod_activite_droitplacemarche.nom_marche_id = mod_activite_nommarche.id"])

	# SPECIFIC FIELDS (QUI N'ONT PAS DE IAISON DIRECT AVEC LA NOTE, MAIS DOIT PASSER PAR ENTITY etENTITY_ID)
	if ni_apm_numero_place:
		lst = lst.extra(where=["mod_activite_droitplacemarche.numero_place LIKE %s"], params=['%'+ni_apm_numero_place+'%'])
	if ni_apm_nom_marche:
		lst = lst.extra(where=["mod_activite_nommarche.nom LIKE %s"], params=['%'+ni_apm_nom_marche+'%'])

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
		
		'ni_apm_reference': request.session['ni_apm_reference'],
		'ni_apm_numero_place': request.session['ni_apm_numero_place'],
		'ni_apm_nom_marche': request.session['ni_apm_nom_marche'],
		'ni_apm_matricule': request.session['ni_apm_matricule'],
		'ni_apm_nom': request.session['ni_apm_nom'],
		'ni_apm_user_create': request.session['ni_apm_user_create'],
		'ni_apm_status': request.session['ni_apm_status'],
		'ni_apm_paiement': request.session['ni_apm_paiement'],

		'ni_apm_du': request.session['ni_apm_du'],
		'ni_apm_au': request.session['ni_apm_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def ni_allocation_place_marche_list(request):
	"""
	Liste des notes d'impositions pour les allocations des places dans les marchés
	Condition : Filtrer les taxes de catégorie notes d'impositions (enum : choix_imposition = 1)
	entity = ENTITY_ALLOCATION_PLACE_MARCHE
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, NI_AllocationPlaceMarcheTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def ni_allocation_place_marche_create(request, entity_id):
	"""
	Créer une note d'imposition
	entity_id = Identifiant de l'allocation de place dans le marché
	"""
	obj = get_object_or_404(AllocationPlaceMarche, pk=entity_id)
	user = User.objects.get(pk=request.user.id)

	if request.method == 'POST':
		form = NI_AllocationPlaceMarcheForm(request.POST, obj_entity=obj, user=user)
	else:
		form = NI_AllocationPlaceMarcheForm(obj_entity=obj, user=user)
		
	return save_ni_allocation_place_marche_form(request, form, NI_AllocationPlaceMarcheTemplate.create, 'create', obj)

#----------------------------------------------------------------
@login_required(login_url="login/")
def ni_allocation_place_marche_update(request, pk):
	"""
	Modifier une note d'imposition
	"""
	obj = get_object_or_404(NoteImposition, pk=pk)
	if request.method == 'POST':
		form = NI_AllocationPlaceMarcheForm(request.POST, instance=obj)
	else:
		form = NI_AllocationPlaceMarcheForm(instance=obj)

	return save_ni_allocation_place_marche_form(request, form, NI_AllocationPlaceMarcheTemplate.update, 'update')

#----------------------------------------------------------------
def save_ni_allocation_place_marche_form(request, form, template_name, action, entity=None):
	"""
	Sauvegarder l'objet note d'imposition
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_NOTE_IMPOSITION,'reference')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(NI_AllocationPlaceMarcheTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)

	context = {'form': form, 'entity':entity}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def ni_allocation_place_marche_validate(request):
	"""
	Valider les informations de la note
	"""
	# Recupérer l'objet note d'imposition
	ID = request.POST["id"]
	obj = get_object_or_404(NoteImposition, pk=ID)
	
	OperationsHelpers.execute_action_validate(request, obj)

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(NI_AllocationPlaceMarcheTemplate.list, context=get_context(request))
	
	return JsonResponse(data)