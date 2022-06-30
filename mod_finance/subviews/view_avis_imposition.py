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
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_validators import *

from mod_finance.models import AvisImposition
from mod_finance.forms import *
from mod_finance.templates import *

from mod_parametrage.enums import *

#----------------------------------------------------------------
#------------------------ Avis d'imposition ---------------------
#----------------------------------------------------------------
def get_list_by_criteria(request, taxe_filter):
	"""
	Renvoie la liste avec criteria
	"""
	lst = AvisImposition.objects

	#Filtrer les taxes de catégorie : Avis d'imposition (enum : choix_imposition = 0)
	if taxe_filter == str(TAXE_ACTIVITE_EXCEPTIONNELLE):
		# Avis généré par les entity' SANS CONTRIBUABLE
		lst = lst.filter(entity=ENTITY_ACTIVITE_EXCEPTIONNELLE).order_by('-reference')
	elif taxe_filter == str(TAXE_VISITE_SITE_TOURISTIQUE):
		# Avis généré par les entity'  SANS CONTRIBUABLE
		lst = lst.filter(entity=ENTITY_VISITE_SITE_TOURISTIQUE).order_by('-reference')
	else:
		# Avis purs
		lst = lst.filter(taxe__categorie_taxe__type_impot = 0, taxe__taxe_filter = taxe_filter).order_by('-reference')
		
	# Nombre total d'enregistrement
	total = lst.count
 
	# Initialier les variables locales, sesions via variables POST
	ai_reference = SessionHelpers.init_variables(request, 'ai_reference')
	ai_ref_paiement = SessionHelpers.init_variables(request, 'ai_ref_paiement')
	ai_agence = SessionHelpers.init_variables(request, 'ai_agence')
	ai_matricule = SessionHelpers.init_variables(request, 'ai_matricule')
	ai_nom = SessionHelpers.init_variables(request, 'ai_nom')
	ai_user_create = SessionHelpers.init_variables(request, 'ai_user_create')
	ai_status = SessionHelpers.init_variables(request, 'ai_status')
	ai_paiement = SessionHelpers.init_variables(request, 'ai_paiement')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'ai_du')
	au = SessionHelpers.init_variables(request, 'ai_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(reference__icontains=ai_reference))
	if ai_ref_paiement: # !!! IMPORTANT car nullable !!!
		query = SessionHelpers.get_query(query, Q(ref_paiement__icontains=ai_ref_paiement))
	if ai_agence: # !!! IMPORTANT car nullable !!!
		query = SessionHelpers.get_query(query, Q(agence__sigle__icontains=ai_agence))
	if ai_matricule: # !!! IMPORTANT car nullable !!!
		query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=ai_matricule))
	if taxe_filter == str(TAXE_AI_DOCUMENT_FINANCIER) or taxe_filter == str(TAXE_BASE_ACTIVITE):
		query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=ai_nom))
	else:
		if ai_nom: # !!! IMPORTANT !!!
			query = SessionHelpers.get_query(query, Q(nom__icontains=ai_nom))
	
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=ai_user_create))

	if ai_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif ai_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif ai_status=='3': #Brouillon
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & Q(fichier_paiement=''))

	if ai_paiement=='1': #Payé
		query = SessionHelpers.get_query(query, Q(date_paiement__isnull=False))
	elif ai_paiement=='2': #Non payé
		query = SessionHelpers.get_query(query, Q(date_paiement__isnull=True))


	# Charger la liste
	if query:
		lst = lst.filter(query)
		if ai_status=='2':
			lst = lst.exclude(fichier_paiement='')
	else:
		if ai_status=='2':
			lst = lst.exclude(fichier_paiement='')

	# Si période valide
	if is_date_fr_valid(du) and is_date_fr_valid(au):
		du = date_picker_to_date_string(du)
		au = date_picker_to_date_string(au, True)
	
		#if is_date_valid(du) and is_date_valid(au):
		lst = lst.filter(date_validate__range=[du, au]).order_by('-date_validate')

	# Renvoyer le résultat de la requete filtrée avec paginator
	return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total

#----------------------------------------------------------------
def get_context(request, taxe_filter):
	"""
	Renvoie les info du context
	"""
	# Lire les notifications
	lst_notification = NotificationHelpers.get_list(request)

	# Charger la liste
	lst, total = get_list_by_criteria(request, taxe_filter)

	# Sauvegader le context
	context = {
		'TAXE_AI_FILTER' : taxe_filter, # !!! IMPORTANT !!!

		'total': total,
		'lst': lst,
		
		'ai_reference': request.session['ai_reference'],
		'ai_ref_paiement': request.session['ai_ref_paiement'],
		'ai_agence': request.session['ai_agence'],
		'ai_matricule': request.session['ai_matricule'],
		'ai_nom': request.session['ai_nom'],
		'ai_user_create': request.session['ai_user_create'],
		'ai_status': request.session['ai_status'],
		'ai_paiement': request.session['ai_paiement'],

		'ai_du': request.session['ai_du'],
		'ai_au': request.session['ai_au'],

		'lst_notification': lst_notification,
		'user': User.objects.get(pk=request.user.id),
	}

	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def avis_imposition_list(request, taxe_filter):
	"""
	Liste des avi d'impositions
	Condition : Filtrer les taxes de catégorie avis d'impositions (enum : choix_imposition = 0)
	"""
	# VIDER LES SESSIONS des critères de recherche si l'avis change de contexte
	if taxe_filter in request.session:
		if request.session['taxe_filter']:
			if taxe_filter != request.session['taxe_filter']:
				request.session['ai_reference'] = ''
				request.session['ai_ref_paiement'] = ''
				request.session['ai_agence'] = ''
				request.session['ai_matricule'] = ''
				request.session['ai_nom'] = ''
				request.session['ai_user_create'] = ''
				request.session['ai_status'] = ''
				request.session['ai_paiement'] = ''

	# Stocker la session taxe filter pour pouvoir filtrer les taxes 
	# Certains profil ne peuvent pas acceder à toutes les taxes c'est pourquoi la liste devra être filtrée
	request.session['taxe_filter'] = taxe_filter

	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()
	
	return render(request, AvisImpositionTemplate.index, context=get_context(request, taxe_filter))

#----------------------------------------------------------------
@login_required(login_url="login/")
def avis_imposition_create(request):
	"""
	Création d'un avis d'imposition, filtré (soit Administratif ou Autre)
	"""
	if request.method == 'POST':
		form = AvisImpositionForm(request.POST, taxe_filter = request.session['taxe_filter'])
	else:
		form = AvisImpositionForm(taxe_filter = request.session['taxe_filter'])
	
	return save_avis_imposition_form(request, form, AvisImpositionTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def avis_imposition_update(request, pk):
	"""
	Modification des informations d'un avis d'imposition
	"""
	obj = get_object_or_404(AvisImposition, pk=pk)
	if request.method == 'POST':
		form = AvisImpositionForm(request.POST, instance=obj, taxe_filter = request.session['taxe_filter'])
	else:
		form = AvisImpositionForm(instance=obj, taxe_filter = request.session['taxe_filter'])
	
	return save_avis_imposition_form(request, form, AvisImpositionTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def avis_imposition_delete(request, pk):
	"""
	Suppression d'un avis d'imposition
	"""
	obj = get_object_or_404(AvisImposition, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		taxe_filter = int(request.session['taxe_filter'])

		data['form_is_valid'] = True
		data['html_content_list'] = render_to_string(AvisImpositionTemplate.list, context=get_context(request, taxe_filter))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'avis_imposition': obj} #JS ve ?
		data['html_form'] = render_to_string(AvisImpositionTemplate.delete, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
def save_avis_imposition_form(request, form, template_name, action):
	"""
	Sauvegarder l'objet avis d'imposition
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_AVIS_IMPOSITION, 'reference')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			taxe_filter = int(request.session['taxe_filter'])

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(AvisImpositionTemplate.list, context=get_context(request, taxe_filter))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
login_required(login_url="login/")
@csrf_exempt
def avis_imposition_validate(request):
	"""
	Valider les informations de la note
	"""
	#Récuperer l'identifiant de l'avis d'imposition
	ID = request.POST["id"]
	obj = get_object_or_404(AvisImposition, pk=ID)

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
			
			# Valider l'objet principal
			OperationsHelpers.execute_action_validate(request, obj)
	except:
		return ErrorsHelpers.show_message(request, 'Erreur de validation')
	
	taxe_filter = int(request.session['taxe_filter'])

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(AvisImpositionTemplate.list, context=get_context(request, taxe_filter))
	
	return JsonResponse(data)

#----------------------------------------------------------------
login_required(login_url="login/")
def avis_imposition_update_paiement(request, pk):
	"""
	Paiement d'un avis d'imposition
	Après avoir créer un avis d'imposition, le système donne l'autorisation d'attacher 
	le fichier de bordereau avec saisie de quelques info (réf+date+agence de paiement)
	"""
	obj = get_object_or_404(AvisImposition, pk=pk)
	if request.method == 'POST':
		form = AvisImpositionPaiementForm(request.POST, instance=obj)
	else:
		form = AvisImpositionPaiementForm(instance=obj)
	
	return save_avis_imposition_form(request, form, AvisImpositionTemplate.paiement, 'paiement')

#----------------------------------------------------------------
def avis_imposition_upload(request, pk):
	"""
	Upload File : Bordereau de versement ou autre preuve de paiement
	"""
	obj = get_object_or_404(AvisImposition, pk=pk)
	if request.method == 'POST':
		form = AvisImpositionFileUploadForm(request.POST, request.FILES)
		if form.is_valid():			
			if form.cleaned_data['fichier_paiement'] is not None:
				obj.fichier_paiement = form.cleaned_data['fichier_paiement']
				obj.save()			
				return redirect('avis_imposition_list', taxe_filter = request.session['taxe_filter'])
		else:
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string(AvisImpositionTemplate.upload, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def avis_imposition_print(request, pk):
	"""
	Impression de l'avis d'impôsition
	"""
	# Nom du fichier template html
	filename = 'avis_imposition_print'

	obj = AvisImposition.objects.get(pk=pk)

	if obj and not obj.date_validate: # + Payement effectué
		# Action save print
		OperationsHelpers.execute_action_print(request, obj)    

		# Definir le context
		context = { 'obj': obj }

		# Generate PDF
		return ReportHelpers.Render(request, filename, context) 

	return ErrorsHelpers.show_message(request, "Erreur d'impression de l'avis d'imposition")

#----------------------------------------------------------------
@login_required(login_url="login/")
def avis_imposition_quittance_print(request, pk):
	"""
	Impression de la quittance l'avis d'impôsition
	"""
	 # Nom du fichier template html
	filename = 'avis_imposition_quittance_print'

	obj = AvisImposition.objects.get(pk=pk)

	if obj and obj.date_validate: # + Payement effectué
		# Action save print
		OperationsHelpers.execute_action_print(request, obj) 

		# Definir le context
		context = {'obj': obj, 'qr_options': ReportHelpers.get_qr_options(), 'qr_data':get_qr_data(obj)}

		# Generate PDF
		return ReportHelpers.Render(request, filename, context) 

	return ErrorsHelpers.show_message(request, "Erreur d'impression de la quittance de l'avis d'imposition")

#----------------------------------------------------------------
def get_qr_data(obj):
	"""
	Composition des données du qr code
	"""
	if isinstance(obj, AvisImposition):
		if obj.contribuable:
			return 'Réf: {} \nMatricule: {} \nNom: {} \nLibellé: {} \nMontant: {} \nPrint: {}'.format(
				obj.reference, 
				obj.contribuable.matricule,
				obj.contribuable.nom,
				obj.libelle,
				obj.montant_total,
				obj.date_print.strftime('%Y-%m-%d %H:%M:%S'))
		else: 
			return 'Réf: {} \nNom: {} \nLibellé: {} \nMontant: {} \nPrint: {}'.format(
				obj.reference, 
				obj.nom,
				obj.taxe.libelle,
				obj.montant_total,
				obj.date_print.strftime('%Y-%m-%d %H:%M:%S'))

	return 'GDAF'