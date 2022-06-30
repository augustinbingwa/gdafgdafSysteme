from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import intcomma

from mod_foncier.models import FoncierExpertise
from mod_foncier.forms import FoncierExpertiseForm, ImageUploadFoncierExpertiseForm, FoncierExpertiseAnnulationForm
from mod_foncier.templates import FoncierExpertiseTemplate

from mod_helpers.models import Chrono,NoteArchive

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_validators import *
from mod_helpers.hlp_entity import EntityHelpers

from mod_finance.models import *
from mod_foncier.subviews.view_foncier_helpers import *
from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#------------- CRUD expertie technique des terrains -------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = FoncierExpertise.objects.count

	# Initialier les variables locales, sesions via variables POST
	fexp_numero_parcelle = SessionHelpers.init_variables(request, 'fexp_numero_parcelle')
	fexp_annee = SessionHelpers.init_variables(request, 'fexp_annee')
	fexp_matricule = SessionHelpers.init_variables(request, 'fexp_matricule')
	fexp_nom = SessionHelpers.init_variables(request, 'fexp_nom')
	fexp_user_create = SessionHelpers.init_variables(request, 'fexp_user_create')
	fexp_status = SessionHelpers.init_variables(request, 'fexp_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'fexp_du')
	au = SessionHelpers.init_variables(request, 'fexp_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(parcelle__numero_parcelle__icontains=fexp_numero_parcelle))
	if is_number_only(fexp_annee):
		query = SessionHelpers.get_query(query, Q(annee=fexp_annee))
	query = SessionHelpers.get_query(query, Q(parcelle__contribuable__matricule__icontains=fexp_matricule))
	query = SessionHelpers.get_query(query, Q(parcelle__contribuable__nom__icontains=fexp_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=fexp_user_create))

	if fexp_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif fexp_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	elif fexp_status=='3': #Brouillon
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True) & (Q(dossier_expertise__exact='')))
	
	# Charger la liste
	if query:
		lst = FoncierExpertise.objects.filter(query)
		if fexp_status=='2':
			lst = lst.exclude(dossier_expertise__exact='')
	else:
		lst = FoncierExpertise.objects.all()
		if fexp_status=='2':
			lst = lst.exclude(dossier_expertise__exact='')

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

		'fexp_numero_parcelle': request.session['fexp_numero_parcelle'],
		'fexp_annee': request.session['fexp_annee'],
		'fexp_matricule': request.session['fexp_matricule'],
		'fexp_nom': request.session['fexp_nom'],
		'fexp_user_create': request.session['fexp_user_create'],
		'fexp_status': request.session['fexp_status'],

		'fexp_du': request.session['fexp_du'],
		'fexp_au': request.session['fexp_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_expertise_list(request):
	"""
	Liste des exprtises techniques
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, FoncierExpertiseTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_expertise_create(request):
	"""
	Création/Ajout d'une exprtise technique
	"""
	if request.method == 'POST':
		form = FoncierExpertiseForm(request.POST)
	else:
		form = FoncierExpertiseForm()
	
	return save_foncier_expertise_form(request, form, FoncierExpertiseTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_expertise_update(request, pk):
	"""
	Modification de l'information d'une expertise technique
	"""
	obj = get_object_or_404(FoncierExpertise, pk=pk)
	if request.method == 'POST':
		form = FoncierExpertiseForm(request.POST, instance=obj)
	else:
		form = FoncierExpertiseForm(instance=obj)

	return save_foncier_expertise_form(request, form, FoncierExpertiseTemplate.update, 'update')

#----------------------------------------------------------------
def save_foncier_expertise_form(request, form, template_name, action):
	"""
	Sauvegarde des informations d'une exprtise technique
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			msg = OperationsHelpers.execute_action(request, action, form)
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(FoncierExpertiseTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_expertise_validate(request):
	"""
	Valider les informations de l'expertise technique
	"""
	# Récuperer l'identifiant de la parcelle
	ID = request.POST["id"]
	obj = get_object_or_404(FoncierExpertise, pk=ID)

	# Calculer le montant des impots (terrain non batis et construction)
	somme_taxe, tnb, tb = get_montant_note(obj)
	if somme_taxe<=0:
		return ErrorsHelpers.show_message(request, "Erreur de validation, le montant de l'impôt foncier doit être positif")

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

				# Si une note est déjà générée alors la mettre à jour (status = VALIDE)
			
			# 3 - Valider l'objet principal
			OperationsHelpers.execute_action_validate(request, obj)
	except:
		return ErrorsHelpers.show_message(request, 'Erreur de validation')

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(FoncierExpertiseTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_expertise_ecriture(request):
	"""
	Générer l'écriture de la note de la déclaration de l'impôt foncier
	"""
	# Récuperer l'identifiant de la parcelle
	ID = request.POST["id"]
	obj = get_object_or_404(FoncierExpertise, pk=ID)

	# get current user 
	user = User.objects.get(pk=request.user.id) 

	# get current datetime 
	dateTimeNow = datetime.datetime.now()

	try:
		with transaction.atomic():
			#---------------------------------------------------------------------
			# 1 - Générer l'écriture de l'objet principal
			OperationsHelpers.execute_action_ecriture(request, obj)

			#---------------------------------------------------------------------
			# 2 - Générer le nouveau numéro chrono
			new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
			obj_chrono = Chrono.objects.get(prefixe = CHRONO_NOTE_IMPOSITION)
			obj_chrono.last_chrono = new_chrono 
			obj_chrono.save();

			# Calculer le montant de l'impot (terrain non bati et construction)
			somme_taxe, tnb, tb = get_montant_note(obj)

			# Si accroissement existe
			taux_accroisement = obj.has_accroissement
			MONTANT_DU = accroissement = 0
			if somme_taxe>0 and taux_accroisement>0:
				accroissement = (somme_taxe * taux_accroisement) / 100

			MONTANT_DU = somme_taxe + accroissement

			if somme_taxe>0:
				#---------------------------------------------------------------------
				# 3 - Créer l'objet Note d'imposition
				ni = NoteImposition()

				# Référence de la note d'imposition (chronologique)
				ni.reference = new_chrono

				# Contribuable qui se trouve sur l'allocation de la place dans le marché (contrat préalable) IMPORTANT !!!
				ni.contribuable = obj.parcelle.contribuable

				# Entity Modèle : 'BaseActivite'
				ni.entity = ENTITY_IMPOT_FONCIER

				# Identifiant de l'entity : 'FoncierExpertise'
				ni.entity_id = obj.id

				# Période de paiement
				ni.periode = PeriodeHelpers.getCurrentPeriode(obj.parcelle.taxe.periode_type)

				# Année de paiement (Très important pour la gestion des périodes)
				ni.annee = obj.annee

				 # Taxe sur activité, Objet taxe (Type : Note d'imposition)
				ni.taxe = obj.parcelle.taxe

				# Libellé de la note (Par défaut = libellé de la taxe)
				ni.libelle = 'Impôt foncier de la parcelle n°' + obj.parcelle.numero_parcelle

				if taux_accroisement>0:
					ni.libelle += ". Avec un taux d'accroissement de " + str(taux_accroisement) + '%, pour un montant de ' + str(intcomma(int(accroissement))) + ' Bif sur un montant de ' + str(intcomma(int(somme_taxe))) + ' Bif'
 
				# Montant total de la taxe à payer (parametre taxe le terrain non batit et construction) avec accroisment
				ni.taxe_montant = MONTANT_DU

				# Traçabilité (date_create est créée depuis le model)
				ni.date_update = dateTimeNow
				ni.date_validate = dateTimeNow

				ni.user_create = user
				ni.user_update = user
				ni.user_validate = user

				# Sauvegarder la note d'imposition (taxe sur l'allocation)
				ni.save()
			else:
				return ErrorsHelpers.show_message(request, "Erreur, le montant de la note d'imposition doit être positif")
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur de génération de l'écriture " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(FoncierExpertiseTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
def foncier_expertise_upload(request, pk):
	"""
	Upload des pièces jointes
	"""
	obj = get_object_or_404(FoncierExpertise, pk=pk)

	# get current user 
	user = User.objects.get(pk=request.user.id) 

	# get current datetime 
	dateTimeNow = datetime.datetime.now()
	data = dict()
	if request.method == 'POST':
		form = ImageUploadFoncierExpertiseForm(request.POST, request.FILES)
		if form.is_valid():			
			if form.cleaned_data['dossier_expertise'] is not None:
				obj.dossier_expertise = form.cleaned_data['dossier_expertise']
				obj.user_create_id = user
				obj.date_declaration = dateTimeNow
				obj.save()			
		return redirect('foncier_expertise_list')
		
		data['form_is_valid'] = False
		data['form_error'] = form.errors
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(FoncierExpertiseTemplate.upload, context, request=request)
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def apercu_ni_print_pdf(request, pk):
	"""
	Impression de la note d'imposition de la carte de proprietaire des véhicules sans carte rose
	"""
	# Nom du fichier template html
	filename = 'apercu_note_imposition_foncier_print'

	obj_entity = FoncierExpertise.objects.get(pk=pk)

	lstCara = FoncierCaracteristique.objects.all().filter(expertise_id=obj_entity.id)

	if obj_entity:
		# Definir le context
		context = { 'obj_entity':obj_entity, 'lstCara': lstCara, 'user': User.objects.get(pk=request.user.id)}
		
		# Generate PDF
		return ReportHelpers.Render(request, filename, context) 

	# Renvoyer l'erreur
	return ErrorsHelpers.show_message(request, "Erreur d'impression de l'aperçu de la note d'imposition")

#----------------------------------------------------------------
#------------------ ANNULATION DE DECLARATION -------------------
#----------------------------------------------------------------
@login_required(login_url="login/")
def foncier_expertise_delete(request, pk):
	"""
	Suppression d'une exprtise technique ou Déclaration foncière
	"""
	# Objet Expertise ou Déclaration
	obj = get_object_or_404(FoncierExpertise, pk=pk)

	data = dict()

	if request.method == 'POST':
		form = FoncierExpertiseAnnulationForm(request.POST, instance=obj)
	else:
		form = FoncierExpertiseAnnulationForm(instance=obj)

	context = {'form': form}
	data['html_form'] = render_to_string(FoncierExpertiseTemplate.delete, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_expertise_delete_action(request):
	"""
	Confirmer l'annulation de la déclaration

	CAS ANNULATION TOTALE:
	- Mettre la déclaration (expertise) en annulation totale
	- Si une note est déjà généré alors il faut aussi annuler cette note
	
	CAS ANNULATION PARTIELLE   
	- Mettre l'expertise en mode invalide
	- Si une note est déjà générée alors la mettre en status "INVALIDE"
	"""
	
	# return ErrorsHelpers.show_message(request, "aaa")
	
    # get current user
	# user = User.objects.get(pk=request.user.id)
	# useget = request.user.id
	# get current datetime

	# obj = get_object_or_404(FoncierExpertise, pk=ID)

	# get current user 
	user = User.objects.get(pk=request.user.id) 

	# get current datetime 
	dateTimeNow = datetime.datetime.now()
	try:
		with transaction.atomic():
			# 1 - CAS ANNULATION TOTALE
			if request.method == 'POST':
				
				idpost = request.POST.get('id')
				# print(idpost)
				btchs = request.POST.get('nbt')
				# print(btchs)
				motif = request.POST.get('text')
				# print(motif)
				objfonc = get_object_or_404(FoncierExpertise, pk = idpost)
				objni = get_object_or_404(NoteImposition, entity_id = idpost)

				if btchs == "2":
					print(idpost)
					print(btchs)
					print(motif)

					objfonc.date_delete = dateTimeNow
					objfonc.motif_delete = motif
					objfonc.user_delete_id = request.user.id
					objfonc.etat = False
					objfonc.save()

					objni.date_delete = dateTimeNow
					objni.motif_delete = motif
					objni.user_delete_id = request.user.id
					objni.etat = False
					objni.save()

				# 2 - CAS ANNULATION PARTIELLE
				if btchs == "1":
					obj = NoteImpositionDelete()
					obj.reference = objni.reference
					obj.entity = objni.entity
					obj.entity_id = objni.entity_id
					obj.annee = objni.annee
					obj.libelle = objni.libelle
					obj.taxe_montant = objni.taxe_montant
					obj.numero_carte_physique = objni.numero_carte_physique
					obj.nombre_impression = objni.nombre_impression
					obj.date_create = objni.date_create
					obj.date_update = objni.date_update
					obj.date_validate = objni.date_validate
					obj.date_print = objni.date_print
					obj.contribuable_id = objni.contribuable_id
					obj.periode_id = objni.periode_id
					obj.taxe_id = objni.taxe_id
					obj.user_create_id = objni.user_create_id
					obj.user_print_id = objni.user_print_id
					obj.user_update_id = objni.user_update_id
					obj.user_validate_id = objni.user_validate_id
					obj.date_delete = dateTimeNow
					obj.motif_delete = motif
					obj.user_delete_id = request.user.id
					obj.save()

					objni.delete()
					objfonc.date_ecriture = None
					objfonc.save()		
						# Traçabilité (date_create est créée depuis le model)
		
			
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur d'annulation de la déclaration " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(FoncierExpertiseTemplate.list, context=get_context(request))
	
	return JsonResponse(data)