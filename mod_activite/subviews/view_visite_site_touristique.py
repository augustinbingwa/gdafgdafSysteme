from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_activite.models import VisiteSiteTouristique
from mod_activite.forms import VisiteSiteTouristiqueForm
from mod_activite.templates import *

from mod_helpers.models import Chrono
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_validators import *

from mod_finance.models import *

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#-------------- CRUD Visite des sites touristiques --------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = VisiteSiteTouristique.objects.count

	# Initialier les variables locales, sessions via variables POST
	vst_numero_visite = SessionHelpers.init_variables(request, 'vst_numero_visite')
	vst_site = SessionHelpers.init_variables(request, 'vst_site')
	vst_motif_visite = SessionHelpers.init_variables(request, 'vst_motif_visite')
	vst_beneficiaire = SessionHelpers.init_variables(request, 'vst_beneficiaire')
	vst_user_create = SessionHelpers.init_variables(request, 'vst_user_create')
	vst_status = SessionHelpers.init_variables(request, 'vst_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'vts_du')
	au = SessionHelpers.init_variables(request, 'vts_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(numero_visite__icontains=vst_numero_visite))
	query = SessionHelpers.get_query(query, Q(site_touristique__adresse_place__icontains=vst_site))
	query = SessionHelpers.get_query(query, Q(motif_visite__icontains=vst_motif_visite))
	query = SessionHelpers.get_query(query, Q(beneficiaire__icontains=vst_beneficiaire))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=vst_user_create))

	if vst_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif vst_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	
	# Charger la liste
	if query:
		lst = VisiteSiteTouristique.objects.filter(query)
	else:
		lst = VisiteSiteTouristique.objects.all()

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

		'vst_numero_visite': request.session['vst_numero_visite'],
		'vst_site': request.session['vst_site'],
		'vst_motif_visite': request.session['vst_motif_visite'],
		'vst_beneficiaire': request.session['vst_beneficiaire'],
		'vst_user_create': request.session['vst_user_create'],
		'vst_status': request.session['vst_status'],

		'vts_du': request.session['vts_du'],
		'vts_au': request.session['vts_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#---------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def visite_site_touristique_list(request):
	"""
	Liste des visites des sites touristiques
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()
	
	return render(request, VisiteSiteTouristiqueTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def visite_site_touristique_create(request):
	"""
	Création d'une visite de site touristique
	"""
	if request.method == 'POST':
		form = VisiteSiteTouristiqueForm(request.POST)
	else:
		form = VisiteSiteTouristiqueForm()

	return save_visite_site_touristique_form(request, form, VisiteSiteTouristiqueTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def visite_site_touristique_update(request, pk):
	"""
	Modification d'une visite de site touristique
	"""
	obj = get_object_or_404(VisiteSiteTouristique, pk=pk)
	if request.method == 'POST':
		form = VisiteSiteTouristiqueForm(request.POST, instance=obj)
	else:
		form = VisiteSiteTouristiqueForm(instance=obj)

	return save_visite_site_touristique_form(request, form, VisiteSiteTouristiqueTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def visite_site_touristique_delete(request, pk):
	"""
	Suppression d'une visite de site touristique
	"""
	obj = get_object_or_404(VisiteSiteTouristique, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True		    
		data['html_content_list'] = render_to_string(VisiteSiteTouristiqueTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(VisiteSiteTouristiqueTemplate.delete, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
def save_visite_site_touristique_form(request, form, template_name, action):
	"""
    Sauvegarde des informations de la visite de site touristique
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_VISITE_SITE_TOURISTIQUE, 'numero_visite')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(VisiteSiteTouristiqueTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def visite_site_touristique_validate(request):
	"""
	Validation des informations de la visite de site touristique
	"""
	# Récuperer l'identifiant de la viite
	ID = request.POST["id"]
	obj = get_object_or_404(VisiteSiteTouristique, pk=ID)
	
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
		
			# Sauvegarder l'objet activité exceptionnelle
			OperationsHelpers.execute_action_validate(request, obj)
	except:
		return ErrorsHelpers.show_message(request, 'Erreur de validation')

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(VisiteSiteTouristiqueTemplate.list, context=get_context(request))

	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def visite_site_touristique_ecriture(request):
	"""
	Validation des informations de la visite de site touristique
	Transaction : Avis d'imposition
	"""
	#Récuperer l'identifiant de la viite
	ID = request.POST["id"]
	obj = get_object_or_404(VisiteSiteTouristique, pk=ID)
	
	# get current user 
	user = User.objects.get(pk=request.user.id) 

	# get current datetime 
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)

	try:
		with transaction.atomic():
			#---------------------------------------------------------------------
			# 1 - Générer l'écriture de l'objet principal
			OperationsHelpers.execute_action_ecriture(request, obj)

			if obj.site_touristique.tarif>0:
				#---------------------------------------------------------------------
				# 2 - Créer et Valider l'avis d'imposition pour le coût de la visite
				# Générer le nouveau numéro chrono
				new_chrono = ChronoHelpers.get_new_num(CHRONO_AVIS_IMPOSITION)
				obj_chrono = Chrono.objects.get(prefixe = CHRONO_AVIS_IMPOSITION)
				obj_chrono.last_chrono = new_chrono 
				obj_chrono.save();

				# 3 - Créer l'objet AvisImposition
				ai = AvisImposition()

				# Référence de l'avis d'imposition (chronologique)
				ai.reference = new_chrono

				# nom du bénéficiaire
				ai.nom = obj.beneficiaire

				# Cout de l'activité exceptionnelle, Objet taxe (Type : Avis d'imposition)
				ai.taxe = obj.taxe

				# coût de l'activité', ai.taxe_montant : Tarif de la taxe (Type : Avis d'imposition) (Formule : tarif * nombre_copie), nombre copie = 1
				ai.nombre_copie = 1 #obj.piece
				
				# Montant de la visite
				ai.taxe_montant = obj.site_touristique.tarif

				# Montant total = Montant par pièce (copie)
				ai.montant_total =  ai.taxe_montant * ai.nombre_copie

				# Nombre de jours de validité de l'activité
				ai.validite = (obj.date_expiration.date() - obj.date_delivrance.date()).days

				# Entity Modèle : 'VisiteSiteTouristique'
				ai.entity = ENTITY_VISITE_SITE_TOURISTIQUE

				# Identifiant de l'entity : 'VisiteSiteTouristique.id'
				ai.entity_id = obj.id

				# Libellé
				ai.libelle = 'Visite du site touristique n°' + obj.numero_visite + ' - '+ obj.site_touristique.adresse_place

				# Traçabilité (date_create est créée depuis le model)
				ai.date_update = dateTimeNow
				
				ai.user_create = user
				ai.user_update = user
				
				# Sauvegarder l'avis d'imposition (coût de la carte d'activité)
				ai.save()
			else:
				return ErrorsHelpers.show_message(request, "Erreur, le montant de l'avis d'imposition doit être positif")
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur de génération de l'écriture " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(VisiteSiteTouristiqueTemplate.list, context=get_context(request))

	return JsonResponse(data)