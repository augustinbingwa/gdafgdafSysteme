from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Utiliser pour les methodes POST
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from mod_activite.models import AllocationEspacePublique
from mod_activite.forms import AllocationEspacePubliqueForm, FichierUploadAllocationEspacePubliqueForm
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
#--------- CRUD Allocation/Occupation Espace Publique -----------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = AllocationEspacePublique.objects.count

	# Initialier les variables locales, sesions via variables POST
	aep_numero_allocation = SessionHelpers.init_variables(request, 'aep_numero_allocation')
	aep_reference_juridique = SessionHelpers.init_variables(request, 'aep_reference_juridique')
	aep_numero_parcelle = SessionHelpers.init_variables(request, 'aep_numero_parcelle')
	aep_contribuable = SessionHelpers.init_variables(request, 'aep_contribuable')
	aep_contribuable_nom = SessionHelpers.init_variables(request, 'aep_contribuable_nom')
	aep_user_create = SessionHelpers.init_variables(request, 'aep_user_create')
	aep_status = SessionHelpers.init_variables(request, 'aep_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'aep_du')
	au = SessionHelpers.init_variables(request, 'aep_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(numero_allocation__icontains=aep_numero_allocation))
	query = SessionHelpers.get_query(query, Q(reference_juridique__icontains=aep_reference_juridique))
	query = SessionHelpers.get_query(query, Q(parcelle_publique__numero_parcelle__icontains=aep_numero_parcelle))
	query = SessionHelpers.get_query(query, Q(contribuable__matricule__icontains=aep_contribuable))
	query = SessionHelpers.get_query(query, Q(contribuable__nom__icontains=aep_contribuable_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=aep_user_create))

	if aep_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif aep_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif aep_status=='3': #Brouillon
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & Q(fichier_lettre_exp_tmp=''))

	# Charger la liste
	if query:
		lst = AllocationEspacePublique.objects.filter(query)
		if aep_status=='2':
			lst = lst.exclude(fichier_lettre_exp_tmp='')
	else:
		lst = AllocationEspacePublique.objects.all()
		if aep_status=='2':
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

		'aep_numero_allocation': request.session['aep_numero_allocation'],
		'aep_reference_juridique': request.session['aep_reference_juridique'],
		'aep_numero_parcelle': request.session['aep_numero_parcelle'],
		'aep_contribuable': request.session['aep_contribuable'],
		'aep_contribuable_nom': request.session['aep_contribuable_nom'],
		'aep_user_create': request.session['aep_user_create'],
		'aep_status': request.session['aep_status'],

		'aep_du': request.session['aep_du'],
		'aep_au': request.session['aep_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_espace_publique_list(request):
	"""
	Liste des allocations d'espace publiques
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, AllocationEspacePubliqueTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_espace_publique_create(request):
	"""
	Création d'une allocation d'espace publique
	"""
	if request.method == 'POST':
		form = AllocationEspacePubliqueForm(request.POST)
	else:
		form = AllocationEspacePubliqueForm()
	
	return save_allocation_espace_publique_form(request, form, AllocationEspacePubliqueTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_espace_publique_update(request, pk):
	"""
	Modification d'une allocation d'espace publique
	"""
	obj = get_object_or_404(AllocationEspacePublique, pk=pk)
	if request.method == 'POST':
		form = AllocationEspacePubliqueForm(request.POST, instance=obj)
	else:
		form = AllocationEspacePubliqueForm(instance=obj)
	
	return save_allocation_espace_publique_form(request, form, AllocationEspacePubliqueTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def allocation_espace_publique_delete(request, pk):
	"""
	Suppression d'une allocation d'espace publique
	"""
	obj = get_object_or_404(AllocationEspacePublique, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()

		data['form_is_valid'] = True		    
		data['html_content_list'] = render_to_string(AllocationEspacePubliqueTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(AllocationEspacePubliqueTemplate.delete, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
def save_allocation_espace_publique_form(request, form, template_name, action):
	"""
    Sauvegarde des informations de l'allocation d'espace publique
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_ALLOCATION_ESPACE_PUBLIQUE, 'numero_allocation')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(AllocationEspacePubliqueTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_espace_publique_validate(request):
	"""
	Validation des informations de l'allocation d'espace publique
	"""
	# Récuperer l'identifiant de l'allocation
	ID = request.POST["id"]
	obj = get_object_or_404(AllocationEspacePublique, pk=ID)

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
				obj_parcelle_pub.usage = USAGE_ACTIVITE
				obj_parcelle_pub.save()
			else:
				return ErrorsHelpers.show_message(request, 'Erreur de validation, cette espace public est déjà occupée')
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur de validation " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(AllocationEspacePubliqueTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def allocation_espace_publique_ecriture(request):
	"""
	Validation des informations de l'allocation d'espace publique
	Transaction : Il faut rendre occupé la parcelle (FoncierParcellePublique.occupee = True) au moment de la validation
	de l'allocation d'espace publique, NoteImpoition
	"""
	# Récuperer l'identifiant de l'allocation
	ID = request.POST["id"]
	obj = get_object_or_404(AllocationEspacePublique, pk=ID)

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
				# 2 - Créer et Valider la note d'imposition (taxe sur l'allocation de l'espace publique)
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

				# Entity Modèle : 'AllocationEspacePublique'
				ni.entity = ENTITY_ALLOCATION_ESPACE_PUBLIQUE

				# Identifiant de l'entity : 'AllocationEspacePublique'
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
	data['html_content_list'] = render_to_string(AllocationEspacePubliqueTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
def allocation_espace_publique_upload(request, pk):
	"""
	Upload des informations de l'allocation d'espace publique
	- fichier_lettre_exp_tmp : Lettre de demande de l’exploitation temporaire
	- fichier_rap_vis_ter : Rapport de visite du terrain (!!! FACULTATIF !!!)
	"""
	obj = get_object_or_404(AllocationEspacePublique, pk=pk)
	if request.method == 'POST':
		form = FichierUploadAllocationEspacePubliqueForm(request.POST, request.FILES)
		if form.is_valid():	
			if form.cleaned_data['fichier_lettre_exp_tmp'] is not None:
				obj.fichier_lettre_exp_tmp = form.cleaned_data['fichier_lettre_exp_tmp']
				obj.save()
			if form.cleaned_data['fichier_rap_vis_ter'] is not None:
				obj.fichier_rap_vis_ter = form.cleaned_data['fichier_rap_vis_ter']
				obj.save()			

			return redirect('allocation_espace_publique_list')
		else :
			return ErrorsHelpers.show(request, form)
	else:
		data = dict()
		context = {'obj': obj}
		data['html_form'] = render_to_string(AllocationEspacePubliqueTemplate.upload, context, request=request)

	return JsonResponse(data)