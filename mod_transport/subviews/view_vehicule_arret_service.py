from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.submodels.model_chrono import Chrono
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_validators import *

from mod_transport.submodels.model_vehicule_arret_service import ArretVehiculeService
from mod_transport.submodels.model_vehicule import Vehicule
from mod_transport.submodels.model_vehicule_activite import VehiculeActivite
from mod_finance.models import NoteImposition
from mod_transport.subforms.form_vehicule_arret_service import ArretVehiculeServiceForm, ImageUploadArretServiceForm, ImageUploadCarteActiviteForm
from mod_transport.templates import *
from mod_parametrage.enums import *

from django.utils import timezone
from datetime import datetime

#----------------------------------------------------------------
#---------------- CRUD Arret ervice d'activité ------------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
    Renvoie la liste avec criteria
    """
	total = ArretVehiculeService.objects.count

	# Initialier les variables locales, sesions via variables POST
	vaa_numero_activite = SessionHelpers.init_variables(request, 'vaa_numero_activite')
	vaa_user_create = SessionHelpers.init_variables(request, 'vaa_user_create')
	vaa_status = SessionHelpers.init_variables(request, 'vaa_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'vaa_du')
	au = SessionHelpers.init_variables(request, 'vaa_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(activite__numero_activite__icontains=vaa_numero_activite))#Premier parametre à None
	query = SessionHelpers.get_query(query, Q(user_arret__username__icontains=vaa_user_create))

	if vaa_status == '1':  # parciel
		query = SessionHelpers.get_query(query, Q(definitif__icontains=False))
	elif vaa_status == '2':  # definitif
		query = SessionHelpers.get_query(query, Q(definitif__icontains=True))
	elif vaa_status == '3':  # valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif vaa_status == '4':  # non valider
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif vaa_status == '5':  # non valider
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))

	# Charger la liste
	if query:
		lst = ArretVehiculeService.objects.filter(query)
	else:
		lst = ArretVehiculeService.objects.all()

	if is_date_fr_valid(du) and is_date_fr_valid(au):
		du = date_picker_to_date_string(du)
		au = date_picker_to_date_string(au, True)
		lst = lst.filter(date_arret__range=[du, au]).order_by('-date_arret')

	# Renvoyer le résultat de la requete filtrée avec paginator
	return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total

# ------------------------------------------------------------
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

		'vaa_numero_activite': request.session['vaa_numero_activite'],
		'vaa_user_create': request.session['vaa_user_create'],
		'vaa_status': request.session['vaa_status'],

		'vaa_du': request.session['vaa_du'],
		'vaa_au': request.session['vaa_au'],

		'lst_notification': lst_notification,
		'user': User.objects.get(pk=request.user.id),
	}

	return context

@login_required(login_url="login/")
@csrf_exempt
def vehicule_arret_service_list(request):
	"""
	Liste des arrêts de service d'activités
	"""
	request.session['url_list'] = request.get_full_path()

	return render(request, VehiculeArretServiceTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_arret_service_create(request):
	"""
	Création d'un arrêt service activité
	"""
	ckcf = 0
	note =''
	data = dict()
	if request.method == 'POST':
		getpayement = NoteImposition.objects.filter(entity_id=request.POST.get('activite'))
		for gtp in getpayement:
			if gtp.taxe_montant > gtp.taxe_montant_paye and gtp.entity== 11:
				note += gtp.reference +'pour vehucule activite'
				ckcf = 1
			if gtp.taxe_montant > gtp.taxe_montant_paye and gtp.entity== 12:
				note += gtp.reference +'pour droit stationnement'
				ckcf = 1
			if gtp.taxe_montant > gtp.taxe_montant_paye and gtp.entity== 13:
				note += gtp.reference
				ckcf = 1
			if ckcf == 0:
				form = ArretVehiculeServiceForm(request.POST)
			else:
				context = {'message': note}
				data['html_form'] = render_to_string(VehiculeArretServiceTemplate.errormassage, context, request=request)
				return JsonResponse(data)

	else:
		form = ArretVehiculeServiceForm()

	return save_arret_service_form(request, form, VehiculeArretServiceTemplate.create, 'createar')

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_arret_service_update(request, pk):
	"""
	Suppression d'un arrêt service activité
	"""
	obj = get_object_or_404(ArretVehiculeService, pk=pk)
	if request.method == 'POST':
		form = ArretVehiculeServiceForm(request.POST, instance=obj)
	else:
		form = ArretVehiculeServiceForm(instance=obj)
	return save_arret_service_form(request, form, VehiculeArretServiceTemplate.update, 'updatear')

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_arret_service_delete(request, pk):
	"""
    Sauvegarde des informations d'un arrêt service activité
	"""
	obj = get_object_or_404(ArretVehiculeService, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()
		
		lst = PaginatorHelpers.get_list_paginator(request, ArretVehiculeService)

		# Lire les notifications
		lst_notification = NotificationHelpers.get_list(request)

		context = {
			'user' : User.objects.get(pk=request.user.id),
			'lst': lst,
			'lst_notification':lst_notification,
		}

		data['form_is_valid'] = True
		data['html_content_list'] = render_to_string(VehiculeArretServiceTemplate.list, context)
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(VehiculeArretServiceTemplate.delete, context, request=request)
	return JsonResponse(data)

#----------------------------------------------------------------
def save_arret_service_form(request, form, template_name, action):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			OperationsHelpers.execute_action(request, action, form)

			lst = PaginatorHelpers.get_list_paginator(request, ArretVehiculeService) 
			
			# Lire les notifications
			lst_notification = NotificationHelpers.get_list(request)

			context = {
				'user' : User.objects.get(pk=request.user.id),
				'lst': lst,
				'lst_notification':lst_notification,
			}

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(VehiculeArretServiceTemplate.list, context)
		else:
			return ErrorsHelpers.show(request, form)
	else:
		context = {'form': form}
		data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
def vehicule_arret_service_upload(request, pk):
	"""
	Upload du fichier arret de formulaire d'activité
	"""
	obj = get_object_or_404(ArretVehiculeService, pk=pk)
	data = dict()
	if request.method == 'POST':
		form = ImageUploadArretServiceForm(request.POST, request.FILES)
		if form.is_valid():		
			if form.cleaned_data['fichier_formulaire_arret_image'] is not None:
				obj.fichier_formulaire_vehicule_arret = form.cleaned_data['fichier_formulaire_arret_image']
				obj.save()
		return redirect('vehicule_arret_service_list')
		
		data['form_is_valid'] = False
		data['form_error'] = form.errors
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(VehiculeArretServiceTemplate.upload, context, request=request)

	return JsonResponse(data)


def vehicule_carte_municipale_upload(request, pk):
	"""
	Upload du fichier arret de formulaire d'activité
	"""
	obj = get_object_or_404(ArretVehiculeService, pk=pk)
	data = dict()
	if request.method == 'POST':
		form = ImageUploadCarteActiviteForm(request.POST, request.FILES)
		if form.is_valid():
			if form.cleaned_data['fichier_carte_municipale_image'] is not None:
				obj.fichier_cart_minispal = form.cleaned_data['fichier_carte_municipale_image']
				obj.save()
		return redirect('vehicule_arret_service_list')

		data['form_is_valid'] = False
		data['form_error'] = form.errors
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(VehiculeArretServiceTemplate.upload_carte, context, request=request)

	return JsonResponse(data)


# ----------------------------------------------------------------
def vehicule_reouverture_service(request, pk):
	"""
	Upload du fichier arret de formulaire d'activité
	"""
	obj = get_object_or_404(ArretVehiculeService, pk=pk)
	user = User.objects.get(pk=request.user.id)
	data = dict()
	if request.method == 'POST':
		objva = get_object_or_404(VehiculeActivite, pk=obj.activite_id)
		objv = get_object_or_404(Vehicule, pk=objva.vehicule_id)
		dateTimeNow = datetime.now(tz=timezone.utc)

		#metre l'etat de vehicule a true model vehicule
		objv.actif = True
		objv.save()
		#metre l'etat reouverture a true model arretvehiculeservice
		obj.etat_reouverture = True
		obj.save()
		#modification dela date de debut d'activite model vehiculeactivite
		objva.date_debut = date_picker_to_date_string(request.POST.get('datereouverture'))
		objva.date_update = dateTimeNow
		objva.user_update = user
		objva.save()
        #creation d'une note de la periode encour
		currentMonth = dateTimeNow.month

		objnotemini = NoteImposition.objects.filter(entity=12, entity_id=objva.id, periode_id=currentMonth, annee=dateTimeNow.year)
		if not objnotemini:
			new_note = NoteImposition(
				reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
				entity=12,
				entity_id=objva.id,
				annee=dateTimeNow.year,
				libelle=objva.vehicule.sous_categorie.taxe_stationnement.libelle,
				taxe_montant=objva.vehicule.sous_categorie.taxe_stationnement.tarif,
				taxe_montant_paye=0.00,
				numero_carte_physique=objva.numero_carte_physique,
				nombre_impression=0,
				date_create=dateTimeNow,
				date_update=dateTimeNow,
				date_validate=dateTimeNow,
				date_print=None,
				contribuable_id=objva.contribuable_id,
				periode_id=currentMonth,
				taxe_id=objva.vehicule.sous_categorie.taxe_stationnement.id,
				user_create_id=1,
				user_print_id=None,
				user_update_id=1,
				user_validate_id=1,
				date_delete=None,
				motif_delete=None,
				user_delete_id=None,
				paiement_externe_file='',
				etat=True,
				date_penalite=None,
				montant_penalite=0,
				montant_taxe=0,
				taux_penalite=0,
				user_penalite_id=None)
			new_note.save()
			obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
			obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
			obj_chrono.save()

		periode_type = objv.sous_categorie.taxe_activite.periode_type_id

		if periode_type == 4:
			periodelimit = 19
		else:
			if int(currentMonth) < 4:
				periodelimit = 13
			elif int(currentMonth) < 3 and int(currentMonth) < 7:
				periodelimit = 14
			elif int(currentMonth) > 6 and int(currentMonth) < 10:
				periodelimit = 15
			elif int(currentMonth) > 9 and int(currentMonth) < 13:
				periodelimit = 16

		objnotestat = NoteImposition.objects.filter(entity=11, entity_id=objva.id, periode_id=periodelimit, annee= dateTimeNow.year)
		if not objnotestat:
			new_note = NoteImposition(
				reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
				entity=11,
				entity_id=objva.id,
				annee=dateTimeNow.year,
				libelle=objva.vehicule.sous_categorie.taxe_activite.libelle,
				taxe_montant=objva.vehicule.sous_categorie.taxe_activite.tarif,
				taxe_montant_paye=0.00,
				numero_carte_physique=objva.numero_carte_physique,
				nombre_impression=0,
				date_create=dateTimeNow,
				date_update=dateTimeNow,
				date_validate=dateTimeNow,
				date_print=None,
				contribuable_id=objva.contribuable_id,
				periode_id=periodelimit,
				taxe_id=objva.vehicule.sous_categorie.taxe_activite.id,
				user_create_id=1,
				user_print_id=None,
				user_update_id=1,
				user_validate_id=1,
				date_delete=None,
				motif_delete=None,
				user_delete_id=None,
				paiement_externe_file='',
				etat=True,
				date_penalite=None,
				montant_penalite=0,
				montant_taxe=0,
				taux_penalite=0,
				user_penalite_id=None)
			new_note.save()
			obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
			obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
			obj_chrono.save()

		data['form_is_valid'] = True
		data['html_content_list'] = render_to_string(VehiculeArretServiceTemplate.list, context=get_context(request))

	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(VehiculeArretServiceTemplate.reouverture, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def vehicule_arret_service_validate(request):
	"""
	Valider les informations d'arret  de service d'activité
	"""	
	#Récuperer l'identifiant de l'activité
	try:
		with transaction.atomic():
			activite_id = request.POST["id"]
			obj = get_object_or_404(ArretVehiculeService, pk=activite_id)	
			
			user = User.objects.get(pk=request.user.id) # get current user 
			dateTimeNow = datetime.now(tz=timezone.utc)
			obj.date_validate = dateTimeNow
			obj.user_validate = user
			obj.save()
			
			#Mise à jour du champ "Actif " dans la base activité
			objVehiculeActivite = get_object_or_404(VehiculeActivite, pk=obj.activite_id)
			objActivite = get_object_or_404(Vehicule, pk=objVehiculeActivite.vehicule_id)
			objActivite.actif = False
			objActivite.save()

	except IntegrityError:
		return ErrorsHelpers.show_message(request, "Erreur de validation de l'arrêt servive")

	lst = PaginatorHelpers.get_list_paginator(request, ArretVehiculeService)
	
	# Lire les notifications
	lst_notification = NotificationHelpers.get_list(request)

	context = {
		'user' : User.objects.get(pk=request.user.id),
		'lst': lst,
		'lst_notification':lst_notification,
	}

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(VehiculeArretServiceTemplate.list,context)
	
	return JsonResponse(data)

