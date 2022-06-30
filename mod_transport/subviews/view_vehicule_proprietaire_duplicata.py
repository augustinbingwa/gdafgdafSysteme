from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_transport.models import VehiculeProprietaireDuplicata
from mod_transport.forms import * 
from mod_transport.templates import *

from mod_helpers.models import Chrono
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_validators import *

from mod_finance.models import AvisImposition, NoteImposition
from mod_crm.models import *

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#-CRUD : Duplicata d'une carte de propriétaire -
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = VehiculeProprietaireDuplicata.objects.count

	# Initialier les variables locales, sesions via variables POST
	vpd_numero_carte = SessionHelpers.init_variables(request, 'vpd_numero_carte')
	vpd_modele = SessionHelpers.init_variables(request, 'vpd_modele')
	vpd_plaque = SessionHelpers.init_variables(request, 'vpd_plaque')
	vpd_chassis = SessionHelpers.init_variables(request, 'vpd_chassis')
	vpd_matricule = SessionHelpers.init_variables(request, 'vpd_matricule')
	vpd_nom = SessionHelpers.init_variables(request, 'vpd_nom')
	vpd_user_create = SessionHelpers.init_variables(request, 'vpd_user_create')
	vpd_status = SessionHelpers.init_variables(request, 'vpd_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'vpd_du')
	au = SessionHelpers.init_variables(request, 'vpd_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(vehicule_proprietaire__numero_carte__icontains=vpd_numero_carte))
	query = SessionHelpers.get_query(query, Q(vehicule_proprietaire__vehicule__modele__nom__icontains=vpd_modele))
	query = SessionHelpers.get_query(query, Q(vehicule_proprietaire__vehicule__plaque__icontains=vpd_plaque))
	query = SessionHelpers.get_query(query, Q(vehicule_proprietaire__vehicule__chassis__icontains=vpd_chassis))
	query = SessionHelpers.get_query(query, Q(vehicule_proprietaire__contribuable__matricule__icontains=vpd_matricule))
	query = SessionHelpers.get_query(query, Q(vehicule_proprietaire__contribuable__nom__icontains=vpd_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=vpd_user_create))

	if vpd_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif vpd_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))

	# Charger la liste
	if query:
		lst = VehiculeProprietaireDuplicata.objects.filter(query)
	else:
		lst = VehiculeProprietaireDuplicata.objects.all()

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

		'vpd_numero_carte': request.session['vpd_numero_carte'],
		'vpd_modele': request.session['vpd_modele'],
		'vpd_plaque': request.session['vpd_plaque'],
		'vpd_chassis': request.session['vpd_chassis'],
		'vpd_matricule': request.session['vpd_matricule'],
		'vpd_nom': request.session['vpd_nom'],
		'vpd_user_create': request.session['vpd_user_create'],
		'vpd_status': request.session['vpd_status'],

		'vpd_du': request.session['vpd_du'],
		'vpd_au': request.session['vpd_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def vehicule_proprietaire_duplicata_list(request):
	"""
	Liste des duplicata des cartes de propriétaire
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, VehiculeProprietaireDuplicataTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_duplicata_create(request):
	"""
	Création/Ajout d'un duplicata d'une carte de propriétaire
	"""
	if request.method == 'POST':
		form = VehiculeProprietaireDuplicataForm(request.POST)
	else:
		form = VehiculeProprietaireDuplicataForm()

	return save_vehicule_proprietaire_duplicata_form(request, form, VehiculeProprietaireDuplicataTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_duplicata_update(request, pk):
	"""
	Modification des informations du duplicata d'une carte de propriétaire
	"""
	obj = get_object_or_404(VehiculeProprietaireDuplicata, pk=pk)
	if request.method == 'POST':
		form = VehiculeProprietaireDuplicataForm(request.POST, instance=obj)
	else:
		form = VehiculeProprietaireDuplicataForm(instance=obj) 

	return save_vehicule_proprietaire_duplicata_form(request, form, VehiculeProprietaireDuplicataTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_duplicata_delete(request, pk):
	"""
	Suppression d'un carte de propriétaire
	"""
	obj = get_object_or_404(VehiculeProprietaireDuplicata, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True
		data['html_content_list'] = render_to_string(VehiculeProprietaireDuplicataTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(VehiculeProprietaireDuplicataTemplate.delete, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
def save_vehicule_proprietaire_duplicata_form(request, form, template_name, action):
	"""
	Sauvegarde des informations d'un duplicata d'une carte de propriétaire
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			OperationsHelpers.execute_action(request, action, form)	

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(VehiculeProprietaireDuplicataTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def vehicule_proprietaire_duplicata_validate(request):
	"""
	Validation des informations du duplicata d'une carte de propriétaire du véhicule
	"""
	ID = request.POST["id"]
	obj = get_object_or_404(VehiculeProprietaireDuplicata, pk=ID)

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
		
			# 1 - Mettre à jour le duplicata
			OperationsHelpers.execute_action_validate(request, obj)
	except:
		return ErrorsHelpers.show_message(request, 'Erreur de validation')

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(VehiculeProprietaireDuplicataTemplate.list, context=get_context(request))

	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt  # pour les methode POST qui necessite crsf_token
def vehicule_proprietaire_duplicata_ecriture(request):
	"""
	Validation des informations du duplicata d'une carte de propriétaire du véhicule
	"""
	ID = request.POST["id"]
	obj = get_object_or_404(VehiculeProprietaireDuplicata, pk=ID)

	# get current user 
	user = User.objects.get(pk=request.user.id) 

	try:
		with transaction.atomic():
			#---------------------------------------------------------------------
			# 1 - Générer l'écriture de l'objet principal
			OperationsHelpers.execute_action_ecriture(request, obj)

			if obj.vehicule_proprietaire.vehicule.sous_categorie.ai_cout_carte_propriete.tarif>0:
				#---------------------------------------------------------------------
				# 2 - Créer et Valider l'avis d'imposition pour le coût de la carte de propriétaire
				# Générer le nouveau numéro chrono
				new_chrono = ChronoHelpers.get_new_num(CHRONO_AVIS_IMPOSITION)
				obj_chrono = Chrono.objects.get(prefixe = CHRONO_AVIS_IMPOSITION)
				obj_chrono.last_chrono = new_chrono 
				obj_chrono.save();
				
				#---------------------------------------------------------------------
				# 3 - Créer le l'objet AvisImposition
				ai = AvisImposition()

				# Référence de l'avis d'imposition (chronologique)
				ai.reference = new_chrono

				# Contribuable
				ai.contribuable = obj.vehicule_proprietaire.contribuable

				# Cout de la carte, Objet taxe (Type : Avis d'imposition)
				ai.taxe = obj.vehicule_proprietaire.vehicule.sous_categorie.ai_cout_carte_propriete

				# ai.taxe_montant : Tarif de la taxe (Type : Avis d'imposition) (Formule : tarif * nombre_copie), nombre copie = 1
				ai.montant_total = ai.taxe_montant = obj.vehicule_proprietaire.vehicule.sous_categorie.ai_cout_carte_propriete.tarif

				# Entity Modèle : 'VehiculeProprietaire'
				ai.entity = ENTITY_VEHICULE_PROPRIETE_DUPLICATA

				# Identifiant de l'entity : 'VehiculeProprietaireDuplicata'
				ai.entity_id = obj.id

				# Libellé
				ai.libelle = 'Duplicata de la carte de propriété n°' + obj.vehicule_proprietaire.numero_carte + ', Vélo/vélo-moteur n°: ' + obj.vehicule_proprietaire.vehicule.plaque + ' - ' + obj.vehicule_proprietaire.vehicule.sous_categorie.nom

				# Traçabilité (date_create est créée depuis le model)
				ai.user_create = user
				
				# Sauvegarder l'avis d'imposition (coût de la carte de propriété)
				ai.save()
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur de génération de l'écriture " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(VehiculeProprietaireDuplicataTemplate.list, context=get_context(request))

	return JsonResponse(data)

#----------------------------------------------------------------
#--- PRINT : Impression du duplicata de la carte de propriété ---
#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_duplicata_print(request, pk):
	"""
	Mise à jour du numero_carte_physique du modèle VehiculeProprietaireDuplicata avant impression
	"""
	obj = get_object_or_404(VehiculeProprietaireDuplicata, pk=pk)
	if request.method == 'POST':
		form = VehiculeProprietaireDuplicataPrintForm(request.POST, instance=obj)
	else:
		form = VehiculeProprietaireDuplicataPrintForm(instance=obj) 

	return save_vehicule_proprietaire_duplicata_form(request, form, VehiculeProprietaireDuplicataTemplate.print, 'update') # 'update' : Mise à jour !!! IMPORTANT !!!

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_duplicata_print_authorization(request, pk):
	"""
	Demander d'autorisation d'impression du duplicata de la carte (car le nombre MAX_NUMBER est atteint)
	"""
	obj = get_object_or_404(VehiculeProprietaireDuplicata, pk=pk)
	if request.method == 'POST':
		form = VehiculeProprietaireDuplicataPrintAuthorizationForm(request.POST, instance=obj)
	else:
		form = VehiculeProprietaireDuplicataPrintAuthorizationForm(instance=obj) 

	return save_vehicule_proprietaire_duplicata_form(request, form, VehiculeProprietaireDuplicataTemplate.print_authorization, 'update') # 'update' : Mise à jour !!! IMPORTANT !!!

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def vehicule_proprietaire_duplicata_print_confirm(request, pk):
	"""
	Confirmer l'impression de la carte de proprietaire du véhicule
	"""
	data = dict()
	success = 'true'
	message = ''

	try:
		obj = get_object_or_404(VehiculeProprietaireDuplicata, pk=pk)
		obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
		if obj and obj_gv and obj.nombre_impression >= int(obj_gv.valeur):
			success = 'false'
			message = "Ereur d'impression, vous n'avez que 3 essais d'impression. <br> Veuillez demander l'autorisation d'impression auprès de votre supérieur."
	except IntegrityError as e:	
		success = 'false'
		message = "Erreur inattendu, " + str(e)
		
	data['success'] = success
	data['html_form'] = message

	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def vehicule_proprietaire_duplicata_print_pdf(request, pk):
	"""
	Impression du duplicata de la carte de proprietaire des véhicules sans carte rose (après cnofirmation)
	"""
	# Nom du fichier template html
	filename = 'carte_proprietaire_duplicata'

	obj = VehiculeProprietaireDuplicata.objects.get(pk=pk)

	obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
	if obj.nombre_impression >= int(obj_gv.valeur):
		# Empecher le download du PDF
		return vehicule_proprietaire_duplicata_print_confirm(request, pk)
	else:
		if obj and obj.date_validate: # + Payement effectué
			# Action save print
			obj.nombre_impression += 1 

			OperationsHelpers.execute_action_print(request, obj)   

			try:
				# Personne physique
				obj_pp = PersonnePhysique.objects.get(pk=obj.vehicule_proprietaire.contribuable.id)
				if obj_pp:
					# photo d'identité
					photo_url = 'file://' + settings.MEDIA_ROOT + '/' + obj_pp.photo_file.name
			except:
				photo_url = ''

			# Définir le context
			context = { 'obj': obj, 'qr_options': ReportHelpers.get_qr_options(), 'qr_data':get_qr_data(obj), 'photo_url':photo_url }

			# Generate PDF
			return ReportHelpers.Render(request, filename, context)

		return ErrorsHelpers.show_message(request, "Erreur d'impression du duplicata de la carte de propriétaire")

#----------------------------------------------------------------
def get_qr_data(obj):
	"""
	Composition des données du qr code
	"""
	if isinstance(obj, VehiculeProprietaireDuplicata):
		return 'ID-card: {} \nMatricule: {} \nNom: {} \nMarque: {} \nPlaque: {} \nChassis: {} \nCatégorie: {} \nValidé: {}'.format(
			obj.vehicule_proprietaire.numero_carte, 
			obj.vehicule_proprietaire.contribuable.matricule,
			obj.vehicule_proprietaire.contribuable.nom,
			obj.vehicule_proprietaire.vehicule.modele.nom,
			obj.vehicule_proprietaire.vehicule.plaque,
			obj.vehicule_proprietaire.vehicule.chassis,
			obj.vehicule_proprietaire.vehicule.sous_categorie.nom,
			obj.date_validate.strftime('%Y-%m-%d %H:%M:%S'))

	return 'GDAF'