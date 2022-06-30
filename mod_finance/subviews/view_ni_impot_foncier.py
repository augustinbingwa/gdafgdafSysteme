from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_validators import *

from mod_finance.models import NoteImposition,NoteImpositionPaiement
from mod_finance.forms import *
from mod_finance.templates import *

from mod_foncier.models import *

from mod_parametrage.enums import *

#----------------------------------------------------------------
#------------ CRUD - Note d'imposition Impôt foncier ------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	ni_query = Q(taxe__categorie_taxe__type_impot = 1) & Q(entity = ENTITY_IMPOT_FONCIER)
	lst = NoteImposition.objects.filter(ni_query).order_by('-reference')

	total = lst.count

	# Initialier les variables locales, sesions via variables POST
	ni_if_reference = SessionHelpers.init_variables(request, 'ni_if_reference')
	ni_if_numero_parcelle = SessionHelpers.init_variables(request, 'ni_if_numero_parcelle')
	ni_if_matricule = SessionHelpers.init_variables(request, 'ni_if_matricule')
	ni_if_nom = SessionHelpers.init_variables(request, 'ni_if_nom')
	ni_if_user_create = SessionHelpers.init_variables(request, 'ni_if_user_create')
	ni_if_status = SessionHelpers.init_variables(request, 'ni_if_status')
	ni_if_paiement = SessionHelpers.init_variables(request, 'ni_if_paiement')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'ni_if_du')
	au = SessionHelpers.init_variables(request, 'ni_if_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(reference__icontains=ni_if_reference))
	query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=ni_if_matricule))
	query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=ni_if_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=ni_if_user_create))

	if ni_if_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif ni_if_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))

	if ni_if_paiement=='1': #Payé
		query = SessionHelpers.get_query(query, Q(taxe_montant=F('taxe_montant_paye')))
	elif ni_if_paiement=='2': #Non payé
		query = SessionHelpers.get_query(query, Q(taxe_montant__gt=F('taxe_montant_paye')))

	# Charger la liste
	if query:
		lst = lst.filter(query,etat = True)

	# Si période valide
	if is_date_fr_valid(du) and is_date_fr_valid(au):
		du = date_picker_to_date_string(du)
		au = date_picker_to_date_string(au, True)
	
		#if is_date_valid(du) and is_date_valid(au):
		lst = lst.filter(date_validate__range=[du, au],etat = True).order_by('-date_validate')

	lst = lst.extra(select={},tables=["mod_foncier_foncierexpertise", "mod_foncier_foncierparcelle"],
					where =["mod_finance_noteimposition.entity_id = mod_foncier_foncierexpertise.id",
					"mod_foncier_foncierparcelle.id = mod_foncier_foncierexpertise.parcelle_id",
					"mod_foncier_foncierexpertise.etat = True"])

	# SPECIFIC FIELDS (QUI N'ONT PAS DE IAISON DIRECT AVEC LA NOTE, MAIS DOIT PASSER PAR ENTITY etENTITY_ID)
	if ni_if_numero_parcelle:
		lst = lst.extra(where=["mod_foncier_foncierparcelle.numero_parcelle LIKE %s"], params=['%'+ni_if_numero_parcelle+'%'])

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
		
		'ni_if_reference': request.session['ni_if_reference'],
		'ni_if_numero_parcelle': request.session['ni_if_numero_parcelle'],
		'ni_if_matricule': request.session['ni_if_matricule'],
		'ni_if_nom': request.session['ni_if_nom'],
		'ni_if_user_create': request.session['ni_if_user_create'],
		'ni_if_status': request.session['ni_if_status'],
		'ni_if_paiement': request.session['ni_if_paiement'],

		'ni_if_du': request.session['ni_if_du'],
		'ni_if_au': request.session['ni_if_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def ni_impot_foncier_list(request):
	"""
	Liste des notes d'impositions pour les impôts fonciers
	Condition : Filtrer les taxes de catégorie notes d'impositions (enum : choix_imposition = 1)
	entity = ENTITY_IMPOT_FONCIER
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, NI_ImpotFoncierTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def ni_impot_foncier_update(request, pk):
	"""
	Modifier une note d'imposition
	"""
	obj = get_object_or_404(NoteImposition, pk=pk)
	if request.method == 'POST':
		form = NI_ImpotFoncierForm(request.POST, instance=obj)
	else:
		form = NI_ImpotFoncierForm(instance=obj)

	return save_ni_impot_foncier_form(request, form, NI_ImpotFoncierTemplate.update, 'update')

#----------------------------------------------------------------
def save_ni_impot_foncier_form(request, form, template_name, action):
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
			data['html_content_list'] = render_to_string(NI_ImpotFoncierTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
		
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

@login_required(login_url="login/")
def ni_impot_foncier_authorisation(request, pk):
	"""
	Modifier une note d'imposition
	"""
	# print('good job')
	obj = get_object_or_404(NoteImposition, pk=pk)
	obj.nombre_impression = 0
	obj.save()

	request.session['url_list'] = request.get_full_path()

	return render(request, NI_ImpotFoncierTemplate.index, )

def ni_impot_foncier_authorisationas(request, pk):
	"""
	Modifier une note d'imposition
	"""
	# print('good job')
	obj = get_object_or_404(NoteImposition, pk=pk)
	obj.nombre_impression = 0
	obj.save()
	
	request.session['url_list'] = request.get_full_path()

	return render(request, NI_ImpotFoncierTemplate.index, context=get_context(request))

def ni_impot_foncier_change_numebord(request):
	"""
	Modification numero bordereau
	# """
	obj = NoteImpositionPaiement.objects.all()
	data = dict()
	if request.method == 'POST':
		form = ChangerNumeroBordereau(request.POST)
		ref = request.POST.get('num_bordereau_change')
		id_ref = request.POST.get('id_numero')
		objcha = get_object_or_404(NoteImpositionPaiement, pk=id_ref)
		objcha.ref_paiement = ref
		objcha.save()
		
		request.session['url_list'] = request.get_full_path()
		return render(request, NI_ImpotFoncierTemplate.index, context=get_context(request))
	else:
		form = ChangerNumeroBordereau()

	context = {'obj': obj}
	data['html_form'] = render_to_string(NI_ImpotFoncierTemplate.changer, context, request=request)

	return JsonResponse(data)
	# return render( request,NI_ImpotFoncierTemplate.changer, context)

def ni_impot_foncier_recherche_numebord(request):
	"""
	Modification numero bordereau
	"""
	obj = NoteImpositionPaiement.objects.all()
	data = dict()
	if request.method == 'POST':
		form = ChangerNumeroBordereau(request.POST)
	else:
		form = ChangerNumeroBordereau()

	context = {'obj': obj}
	data['html_form'] = render_to_string(NI_ImpotFoncierTemplate.changer, context, request=request)

	return JsonResponse(data)

