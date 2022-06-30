from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from mod_activite.models import PubliciteMurCloture
from mod_activite.forms import PubliciteMurClotureForm, ImageUploadPubliciteMurClotureForm
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

from mod_finance.models import NoteImposition

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#------- CRUD Allocation Publicité sur les Murs/Clôtures  -------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = PubliciteMurCloture.objects.count

	# Initialier les variables locales, sesions via variables POST
	pmc_numero_allocation = SessionHelpers.init_variables(request, 'pmc_numero_allocation')
	pmc_Type = SessionHelpers.init_variables(request, 'pmc_Type')
	pmc_reference_juridique = SessionHelpers.init_variables(request, 'pmc_reference_juridique')
	pmc_adresse = SessionHelpers.init_variables(request, 'pmc_adresse')
	pmc_contribuable = SessionHelpers.init_variables(request, 'pmc_contribuable')
	pmc_contribuable_nom = SessionHelpers.init_variables(request, 'pmc_contribuable_nom')
	pmc_user_create = SessionHelpers.init_variables(request, 'pmc_user_create')
	pmc_status = SessionHelpers.init_variables(request, 'pmc_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'pmc_du')
	au = SessionHelpers.init_variables(request, 'pmc_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(numero_allocation__icontains=pmc_numero_allocation))
	query = SessionHelpers.get_query(query, Q(type_publicite__icontains=pmc_Type))
	query = SessionHelpers.get_query(query, Q(reference_juridique__icontains=pmc_reference_juridique))
	query = SessionHelpers.get_query(query, Q(adresse__nom__icontains=pmc_adresse))
	query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=pmc_contribuable))
	query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=pmc_contribuable_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=pmc_user_create))

	if pmc_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif pmc_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif pmc_status=='3': #Brouillon
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & Q(fichier_lettre_exp_tmp=''))

	# Charger la liste
	if query:
		lst = PubliciteMurCloture.objects.filter(query)
		if pmc_status=='2':
			lst = lst.exclude(fichier_lettre_exp_tmp='')
	else:
		lst = PubliciteMurCloture.objects.all()
		if pmc_status=='2':
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

		'pmc_numero_allocation': request.session['pmc_numero_allocation'],
		'pmc_Type': request.session['pmc_Type'],
		'pmc_reference_juridique': request.session['pmc_reference_juridique'],
		'pmc_adresse': request.session['pmc_adresse'],
		'pmc_contribuable': request.session['pmc_contribuable'],
		'pmc_contribuable_nom': request.session['pmc_contribuable_nom'],
		'pmc_user_create': request.session['pmc_user_create'],
		'pmc_status': request.session['pmc_status'],

		'pmc_du': request.session['pmc_du'],
		'pmc_au': request.session['pmc_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def publicite_mur_cloture_list(request):
	"""
	Liste des publicités sur les Murs/Clôtures
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, PubliciteMurClotureTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def publicite_mur_cloture_create(request):
	"""
	Création d'une publicité sur les Murs/Clôtures
	"""
	if request.method == 'POST':
		form = PubliciteMurClotureForm(request.POST)
	else:
		form = PubliciteMurClotureForm()
	
	return save_publicite_mur_cloture_form(request, form, PubliciteMurClotureTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def publicite_mur_cloture_update(request, pk):
	"""
	Modification d'une publicité sur les Murs/Clôtures
	"""
	obj = get_object_or_404(PubliciteMurCloture, pk=pk)
	if request.method == 'POST':
		form = PubliciteMurClotureForm(request.POST, instance=obj)
	else:
		form = PubliciteMurClotureForm(instance=obj)
	
	return save_publicite_mur_cloture_form(request, form, PubliciteMurClotureTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def publicite_mur_cloture_delete(request, pk):
	"""
	Suppression d'une publicité sur les Murs/Clôtures
	"""
	obj = get_object_or_404(PubliciteMurCloture, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True		    
		data['html_content_list'] = render_to_string(PubliciteMurClotureTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(PubliciteMurClotureTemplate.delete, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
def save_publicite_mur_cloture_form(request, form, template_name, action):
	"""
    Sauvegarde des informations de la publicité sur les murs/clôtures
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_PUBLICITE_MUR_CLOTURE, 'numero_allocation')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(PubliciteMurClotureTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def publicite_mur_cloture_validate(request):
	"""
	Validation des informations de la publicité sur les murs/clôtures
	"""
	# 1- Récuperer l'identifiant de l'allocation
	ID = request.POST["id"]
	obj = get_object_or_404(PubliciteMurCloture, pk=ID)

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

			# Sauvegarder l'objet allocation
			OperationsHelpers.execute_action_validate(request, obj)
	except:
		return ErrorsHelpers.show_message(request, 'Erreur de validation')

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(PubliciteMurClotureTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def publicite_mur_cloture_ecriture(request):
	"""
	Validation des informations de la publicité sur les murs/clôtures
	TRANSACTION : Chrono et Note d'imposition
	"""
	# 1- Récuperer l'identifiant de l'allocation
	ID = request.POST["id"]
	obj = get_object_or_404(PubliciteMurCloture, pk=ID)

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
				# 2 - Créer et Valider la note d'imposition (taxe sur la publicité)
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

				# Entity Modèle : 'PubliciteMurCloture'
				ni.entity = ENTITY_PUBLICITE_MUR_CLOTURE

				# Identifiant de l'entity : 'PubliciteMurCloture'
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

				# Sauvegarder la note d'imposition (taxe sur la publicité)
				ni.save()
			else:
				return ErrorsHelpers.show_message(request, "Erreur, le montant de la note d'imposition doit être positif")
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur de génération de l'écriture " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(PubliciteMurClotureTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
def publicite_mur_cloture_upload(request, pk):
	"""
	Upload des informations de l'allocation de panneau publicitaire
	- fichier_lettre_exp_tmp : Lettre de demande de l’exploitation temporaire
	- fichier_rap_vis_ter : Rapport de visite du terrain (!!! FACULTATIF !!!)
	"""
	obj = get_object_or_404(PubliciteMurCloture, pk=pk)
	if request.method == 'POST':
		form = ImageUploadPubliciteMurClotureForm(request.POST, request.FILES)
		if form.is_valid():		
			if form.cleaned_data['fichier_lettre_exp_tmp'] is not None:
				obj.fichier_lettre_exp_tmp = form.cleaned_data['fichier_lettre_exp_tmp']
				obj.save()
			if form.cleaned_data['fichier_rap_vis_ter'] is not None:
				obj.fichier_rap_vis_ter = form.cleaned_data['fichier_rap_vis_ter']
				obj.save()			
		
			return redirect('publicite_mur_cloture_list')
		else :
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string(PubliciteMurClotureTemplate.upload, context, request=request)
	
	return JsonResponse(data)