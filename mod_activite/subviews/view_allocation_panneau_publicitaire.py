from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from mod_activite.models import AllocationPanneauPublicitaire
from mod_activite.forms import AllocationPanneauPublicitaireForm, ImageUploadAllocationPanneauPublicitaireForm
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
from mod_helpers.hlp_accroissement import AccroissementHelpers
from mod_helpers.hlp_validators import *

from mod_foncier.models import FoncierParcellePublique

from mod_finance.models import NoteImposition

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#---------- CRUD Allocation Panneau Publicitaire  ---------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = AllocationPanneauPublicitaire.objects.count

	# Initialier les variables locales, sesions via variables POST
	app_numero_allocation = SessionHelpers.init_variables(request, 'app_numero_allocation')
	app_reference_juridique = SessionHelpers.init_variables(request, 'app_reference_juridique')
	app_numero_parcelle = SessionHelpers.init_variables(request, 'app_numero_parcelle')
	app_contribuable = SessionHelpers.init_variables(request, 'app_contribuable')
	app_contribuable_nom = SessionHelpers.init_variables(request, 'app_contribuable_nom')
	app_user_create = SessionHelpers.init_variables(request, 'app_user_create')
	app_status = SessionHelpers.init_variables(request, 'app_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'app_du')
	au = SessionHelpers.init_variables(request, 'app_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(numero_allocation__icontains=app_numero_allocation))
	query = SessionHelpers.get_query(query, Q(reference_juridique__icontains=app_reference_juridique))
	query = SessionHelpers.get_query(query, Q(parcelle_publique__numero_parcelle__icontains=app_numero_parcelle))
	query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=app_contribuable))
	query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=app_contribuable_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=app_user_create))

	if app_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif app_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif app_status=='3': #Brouillon
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & Q(fichier_lettre_exp_tmp=''))

	# Charger la liste
	if query:
		lst = AllocationPanneauPublicitaire.objects.filter(query)
		if app_status=='2':
			lst = lst.exclude(fichier_lettre_exp_tmp='')
	else:
		lst = AllocationPanneauPublicitaire.objects.all()
		if app_status=='2':
			lst = lst.exclude(fichier_lettre_exp_tmp='')

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

		'app_numero_allocation': request.session['app_numero_allocation'],
		'app_reference_juridique': request.session['app_reference_juridique'],
		'app_numero_parcelle': request.session['app_numero_parcelle'],
		'app_contribuable': request.session['app_contribuable'],
		'app_contribuable_nom': request.session['app_contribuable_nom'],
		'app_user_create': request.session['app_user_create'],
		'app_status': request.session['app_status'],

		'app_du': request.session['app_du'],
		'app_au': request.session['app_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_panneau_publicitaire_list(request):
	"""
	Liste des allocations de panneau publicitaire
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, AllocationPanneauPublicitaireTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_panneau_publicitaire_create(request):
	"""
	Création d'une allocation de panneau publicitaire
	"""
	if request.method == 'POST':
		form = AllocationPanneauPublicitaireForm(request.POST)
	else:
		form = AllocationPanneauPublicitaireForm()
	
	return save_allocation_panneau_publicitaire_form(request, form, AllocationPanneauPublicitaireTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_panneau_publicitaire_update(request, pk):
	"""
	Modification d'une allocation de panneau publicitaire
	"""
	obj = get_object_or_404(AllocationPanneauPublicitaire, pk=pk)
	if request.method == 'POST':
		form = AllocationPanneauPublicitaireForm(request.POST, instance=obj)
	else:
		form = AllocationPanneauPublicitaireForm(instance=obj)
	
	return save_allocation_panneau_publicitaire_form(request, form, AllocationPanneauPublicitaireTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_panneau_publicitaire_delete(request, pk):
	"""
	Suppression d'une allocation de panneau publicitaire
	"""
	obj = get_object_or_404(AllocationPanneauPublicitaire, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True		    
		data['html_content_list'] = render_to_string(AllocationPanneauPublicitaireTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(AllocationPanneauPublicitaireTemplate.delete, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
def save_allocation_panneau_publicitaire_form(request, form, template_name, action):
	"""
    Sauvegarde des informations de l'allocation de panneau publicitaire
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_ALLOCATION_PANNEAU_PUBLICITAIRE, 'numero_allocation')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(AllocationPanneauPublicitaireTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_panneau_publicitaire_validate(request):
	"""
	Validation des informations de l'allocation de panneau publicitaire
	"""
	# 1- Récuperer l'identifiant de l'allocation
	ID = request.POST["id"]
	obj = get_object_or_404(AllocationPanneauPublicitaire, pk=ID)

	try:
		with transaction.atomic():
			# Lire l'information de la parcelle/espace public
			obj_parcelle_pub = get_object_or_404(FoncierParcellePublique, pk=obj.parcelle_publique.id)

			if not obj_parcelle_pub.occupee:
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
				# 1 - Valider l'objet allocation
				OperationsHelpers.execute_action_validate(request, obj)

				#---------------------------------------------------------------------
				# 2 - Mettre à jour la parcelle maintenant qui est desormais occupée
				obj_parcelle_pub.occupee = True
				obj_parcelle_pub.usage = USAGE_PANNEAU
				obj_parcelle_pub.save()
			else:
				return ErrorsHelpers.show_message(request, 'Erreur de validation, cette espace public est déjà occupée')
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, 'Erreur de validation ' + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(AllocationPanneauPublicitaireTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_panneau_publicitaire_ecriture(request):
	"""
	Validation des informations de l'allocation de panneau publicitaire
	"""
	# 1- Récuperer l'identifiant de l'allocation
	ID = request.POST["id"]
	obj = get_object_or_404(AllocationPanneauPublicitaire, pk=ID)

	# get current user 
	user = User.objects.get(pk=request.user.id) 

	# get current datetime 
	dateTimeNow = datetime.datetime.now()

	try:
		with transaction.atomic():
			#---------------------------------------------------------------------
			# 1 - Générer l'écriture de l'objet principal
			OperationsHelpers.execute_action_ecriture(request, obj)

			if obj.taxe.tarif>0:
				#---------------------------------------------------------------------
				# 2 - Créer et Valider la note d'imposition (taxe sur l'allocation du panneau publicitaire)
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

				# Entity Modèle : 'AllocationPanneauPublicitaire'
				ni.entity = ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE

				# Identifiant de l'entity : 'AllocationPanneauPublicitaire'
				ni.entity_id = obj.id

				# Période de paiement
				ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)

				# Année de paiement (Très important pour la gestion des périodes)
				ni.annee = dateTimeNow.year

				# Taxe sur activité, Objet taxe (Type : Note d'imposition)
				ni.taxe = obj.taxe

				# Montant total de la taxe à payer (montant par m² x tarif)
				montant_total = obj.superficie * obj.taxe.tarif

				# ACCROISEMENT
				taux_accroisement = AccroissementHelpers.has_accroissement(dateTimeNow.year, dateTimeNow)
				accroissement = 0
				if taux_accroisement>0:
					accroissement = (montant_total * taux_accroisement) / 100

				MONTANT_DU = montant_total + accroissement

				# Solde de depart
				if obj.solde_depart>0:
					MONTANT_DU += obj.solde_depart

				# Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
				ni.taxe_montant = MONTANT_DU

				# Traçabilité (date_create est créée depuis le model)
				ni.date_update = dateTimeNow
				ni.date_validate = dateTimeNow

				ni.user_create = user
				ni.user_update = user
				ni.user_validate = user

				# Sauvegarder la note d'imposition (taxe sur l'allocation de l'espace)
				ni.save()
			else:
				return ErrorsHelpers.show_message(request, "Erreur, le montant de la note d'imposition doit être positif")
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur de génération de l'écriture " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(AllocationPanneauPublicitaireTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
def allocation_panneau_publicitaire_upload(request, pk):
	"""
	Upload des informations de l'allocation de panneau publicitaire
	- fichier_lettre_exp_tmp : Lettre de demande de l’exploitation temporaire
	- fichier_rap_vis_ter : Rapport de visite du terrain (!!! FACULTATIF !!!)
	"""
	obj = get_object_or_404(AllocationPanneauPublicitaire, pk=pk)
	if request.method == 'POST':
		form = ImageUploadAllocationPanneauPublicitaireForm(request.POST, request.FILES)
		if form.is_valid():		
			if form.cleaned_data['fichier_lettre_exp_tmp'] is not None:
				obj.fichier_lettre_exp_tmp = form.cleaned_data['fichier_lettre_exp_tmp']
				obj.save()
			if form.cleaned_data['fichier_rap_vis_ter'] is not None:
				obj.fichier_rap_vis_ter = form.cleaned_data['fichier_rap_vis_ter']
				obj.save()			

			return redirect('allocation_panneau_publicitaire_list')
		else :
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string(AllocationPanneauPublicitaireTemplate.upload, context, request=request)
	
	return JsonResponse(data)