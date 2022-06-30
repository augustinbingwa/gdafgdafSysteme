from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from mod_activite.models import AllocationPlaceMarche, DroitPlaceMarche
from mod_activite.forms import AllocationPlaceMarcheForm, FichierUploadAllocationPlaceMarcheForm
from mod_activite.templates import *

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

from mod_finance.models import NoteImposition

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#------- CRUD Allocation/Occupation place dans le marché  -------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = AllocationPlaceMarche.objects.count

	# Initialier les variables locales, sesions via variables POST
	apm_marche = SessionHelpers.init_variables(request, 'apm_marche')
	apm_place = SessionHelpers.init_variables(request, 'apm_place')
	apm_contribuable = SessionHelpers.init_variables(request, 'apm_contribuable')
	apm_contribuable_nom = SessionHelpers.init_variables(request, 'apm_contribuable_nom')
	apm_user_create = SessionHelpers.init_variables(request, 'apm_user_create')
	apm_status = SessionHelpers.init_variables(request, 'apm_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'apm_du')
	au = SessionHelpers.init_variables(request, 'apm_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(droit_place_marche__nom_marche__nom__icontains=apm_marche))
	query = SessionHelpers.get_query(query, Q(droit_place_marche__numero_place__icontains=apm_place))
	query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=apm_contribuable))
	query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=apm_contribuable_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=apm_user_create))

	if apm_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif apm_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif apm_status=='3': #Brouillon
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & Q(fichier_contrat=''))

	# Charger la liste
	if query:
		lst = AllocationPlaceMarche.objects.filter(query)
		if apm_status=='2':
			lst = lst.exclude(fichier_contrat='')
	else:
		lst = AllocationPlaceMarche.objects.all()
		if apm_status=='2':
			lst = lst.exclude(fichier_contrat='')

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

		'apm_marche': request.session['apm_marche'],
		'apm_place': request.session['apm_place'],
		'apm_contribuable': request.session['apm_contribuable'],
		'apm_contribuable_nom': request.session['apm_contribuable_nom'],
		'apm_user_create': request.session['apm_user_create'],
		'apm_status': request.session['apm_status'],

		'apm_du': request.session['apm_du'],
		'apm_au': request.session['apm_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_place_marche_list(request):
	"""
	Liste des allocations de place dans le marché
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, AllocationPlaceMarcheTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_place_marche_create(request):
	"""
	Création d'une allocation de place dans le marché
	"""
	if request.method == 'POST':
		form = AllocationPlaceMarcheForm(request.POST)
	else:
		form = AllocationPlaceMarcheForm()
	
	return save_allocation_place_marche_form(request, form, AllocationPlaceMarcheTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_place_marche_update(request, pk):
	"""
	Modification d'une allocation de place dans le marché
	"""
	obj = get_object_or_404(AllocationPlaceMarche, pk=pk)
	if request.method == 'POST':
		form = AllocationPlaceMarcheForm(request.POST, instance=obj)
	else:
		form = AllocationPlaceMarcheForm(instance=obj)
	
	return save_allocation_place_marche_form(request, form, AllocationPlaceMarcheTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_place_marche_delete(request, pk):
	"""
	Suppression d'une allocation de place dans le marché
	"""
	obj = get_object_or_404(AllocationPlaceMarche, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True		    
		data['html_content_list'] = render_to_string(AllocationPlaceMarcheTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(AllocationPlaceMarcheTemplate.delete, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
def save_allocation_place_marche_form(request, form, template_name, action):
	"""
	Sauvegarde des informations de l'allocation de place dans le marché
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form)
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(AllocationPlaceMarcheTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
@login_required(login_url="login/")
def allocation_place_marche_validate(request):
	"""
	Validation des informations de l'allocation de place dans le marché
	"""
	# 1- Récuperer l'identifiant de l'allocation
	ID = request.POST["id"]
	obj = get_object_or_404(AllocationPlaceMarche, pk=ID)
	
	# get current user 
	user = User.objects.get(pk=request.user.id) 

	# get current datetime 
	dateTimeNow = datetime.datetime.now()

	try:
		with transaction.atomic():	
			# Lire l'information de la place
			obj_droi_place = get_object_or_404(DroitPlaceMarche, pk=obj.droit_place_marche.id)

			if not obj_droi_place.occupee:
				if obj.note and obj.date_note:
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

					# 2 Effacer la trace de la notification
					obj.note = None
					obj.user_note = None
					obj.date_note = None
					obj.reponse_note = None
					obj.demande_annulation_validation = False
					obj.date_cancel = None
					obj.user_cancel = None

				#---------------------------------------------------------------------
				# 1 - Sauvegarder l'objet allocation
				OperationsHelpers.execute_action_validate(request, obj)

				#---------------------------------------------------------------------
				# 2 - Mettre à jour le champs 'DroitPlaceMarche.occupee = True'
				obj_droi_place.occupee = True
				obj_droi_place.save()
			else:
				return ErrorsHelpers.show_message(request, 'Erreur de validation, cette place est déjà occupée')
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, 'Erreur de validation ' + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(AllocationPlaceMarcheTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
@login_required(login_url="login/")
def allocation_place_marche_ecriture(request):
	"""
	Validation des informations de l'allocation de place dans le marché
	Transaction : DroitPlaceMarche et NoteImposition
	"""
	# 1- Récuperer l'identifiant de l'allocation
	ID = request.POST["id"]
	obj = get_object_or_404(AllocationPlaceMarche, pk=ID)
	
	# get current user 
	user = User.objects.get(pk=request.user.id) 

	# get current datetime 
	dateTimeNow = datetime.datetime.now()

	try:
		with transaction.atomic():	
			#---------------------------------------------------------------------
			# 1 - Générer l'écriture de l'objet principal
			OperationsHelpers.execute_action_ecriture(request, obj)

			if obj.droit_place_marche.cout_place>0:
				#---------------------------------------------------------------------
				# 2 - Créer et Valider la note d'imposition (taxe sur le droit de place)
				# Générer le nouveau numéro chrono
				new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
				obj_chrono = Chrono.objects.get(prefixe = CHRONO_NOTE_IMPOSITION)
				obj_chrono.last_chrono = new_chrono 
				obj_chrono.save();

				#---------------------------------------------------------------------
				# 3 - Créer l'objet Note d'imposition
				ni = NoteImposition()

				# Référence de la note d'imposition (chronologique)
				ni.reference = new_chrono

				# Contribuable
				ni.contribuable = obj.contribuable

				# Entity Modèle : 'AllocationPlaceMarche'
				ni.entity = ENTITY_ALLOCATION_PLACE_MARCHE

				# Identifiant de l'entity : 'AllocationPlaceMarche'
				ni.entity_id = obj.id

				# Période de paiement
				ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)

				# Année de paiement (Très important pour la gestion des périodes)
				ni.annee = dateTimeNow.year

				 # Taxe sur activité, Objet taxe (Type : Note d'imposition)
				ni.taxe = obj.taxe

				# Montant dû
				MONTANT_DU = obj.droit_place_marche.cout_place

				# si CAUTION n'est pas encore payee
				if obj.caution_montant>0:
					MONTANT_DU += obj.caution_montant
					ni.libelle += '. Avec une caution de ' + str(obj.caution_nombre_mois) + ' mois pour un montant de ' + str(intcomma(obj.caution_montant)) + 'Bif.'

				# Solde de depart
				if obj.solde_depart>0:
					MONTANT_DU += obj.solde_depart

				# Montant total de la taxe à payer (parametre taxe dans DroitPlaceMarche)
				ni.taxe_montant = MONTANT_DU

				# Traçabilité (date_create est créée depuis le model)
				ni.date_update = dateTimeNow
				ni.date_validate = dateTimeNow

				ni.user_create = user
				ni.user_update = user
				ni.user_validate = user

				# Sauvegarder la note d'imposition (taxe sur l'allocation de la place)
				ni.save()
			else:
				return ErrorsHelpers.show_message(request, "Erreur, le montant doit être positif")
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur de génération de l'écriture " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(AllocationPlaceMarcheTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_place_marche_upload(request, pk):
	"""
	Upload du fchier contrat de l'allocation de place dans le marché
	"""
	obj = get_object_or_404(AllocationPlaceMarche, pk=pk)
	if request.method == 'POST':
		form = FichierUploadAllocationPlaceMarcheForm(request.POST, request.FILES)
		if form.is_valid():		
			if form.cleaned_data['fichier_contrat'] is not None:
				obj.fichier_contrat = form.cleaned_data['fichier_contrat']
				obj.save()
	
				return redirect('allocation_place_marche_list')
		else:
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string(AllocationPlaceMarcheTemplate.upload, context, request=request)
	
	return JsonResponse(data)