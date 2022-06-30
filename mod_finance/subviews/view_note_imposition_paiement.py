from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_foncier.models import FoncierExpertise

from mod_finance.models import NoteImposition, NoteImpositionPaiement
from mod_finance.forms import NoteImpositionPaiementForm, NoteImpositionPaiementFileUploadForm
from mod_finance.templates import *

from django.utils import timezone
import datetime

from mod_parametrage.enums import *

#----------------------------------------------------------------
#------ CRUD - Gestion de paiement des notes d'imposition--------
#----------------------------------------------------------------
def get_context(request, ni_pk):
	"""
	Liste des paiemens de notes d'impositions pour toutes activites
	Condition : Filtrer les paiements par 'note d'imposition'
	"""
	# L'objet note d'impostion à suivre
	obj_ni=get_object_or_404(NoteImposition, pk=ni_pk)

	# Lire les notifications
	lst_notification = NotificationHelpers.get_list(request)

	lst = NoteImpositionPaiement.objects.filter(note_imposition=ni_pk).order_by('date_paiement')

	context = {
		'obj': obj_ni,
		'lst': lst,
		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}
	
	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
def note_imposition_paiement_list(request, pk):
	"""
	Liste de paiements des notes d'imposiiton
	pk : Identifiant de la note à payer
	"""
	# Enregistrer en session le pk de la note d'imposition (ceci sera utilisé dans le CRUD de paiement d'une note)
	request.session['ni_pk']=pk

	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	# Afficher la liste des paiements de la note
	return render(request, NoteImpositionPaiementTemplate.index, context=get_context(request, pk))

#----------------------------------------------------------------
@login_required(login_url="login/")
def note_imposition_paiement_create(request):
	"""
	Créer un paiement de note d'imposition
	"""
	ckcf = 0
	note = "<h3><b class='text-danger'>NOTE D'IMPOSITION A PAIE D'ABORD</b></h3></br>"
	dateTimeNow = datetime.datetime.now()
	if request.method == 'POST':
		form=NoteImpositionPaiementForm(request.POST, ni_pk=request.session['ni_pk'])
	else:
		obj_ni = get_object_or_404(NoteImposition, pk=request.session['ni_pk'])
		if obj_ni.entity == 10:
			obj_exp = get_object_or_404(FoncierExpertise, pk=obj_ni.entity_id)
			get_note = NoteImposition.objects.filter(entity=10,entity_id=obj_exp.id,contribuable_id=obj_ni.contribuable_id, annee=obj_exp.annee)
			if get_note:
				for ln_note in get_note:
					if ln_note.taxe_montant_paye < ln_note.taxe_montant:
						try:
							preveu_year = ln_note.annee - 1
							check_exp = FoncierExpertise.objects.get(parcelle_id=obj_exp.parcelle_id,annee=preveu_year)
							check_note = NoteImposition.objects.get(entity=10,entity_id=check_exp.id,contribuable_id=obj_ni.contribuable_id, annee=check_exp.annee)
							if check_note.taxe_montant_paye < check_note.taxe_montant:
								note += check_note.reference + ' pour un montant de ' + str(round(check_note.taxe_montant - check_note.taxe_montant_paye)) + 'Fbu de l\'année  ' + str(check_note.annee) + ' </br>'
								ckcf = 1
							check_expertise = FoncierExpertise.objects.filter(parcelle_id=obj_exp.parcelle_id).order_by('annee')
							for in_chk_exp in check_expertise:
								if in_chk_exp.annee < check_note.annee:
									check_note_get = NoteImposition.objects.get(entity=10, entity_id=in_chk_exp.id,ontribuable_id=obj_ni.contribuable_id,annee=in_chk_exp.annee)
									if check_note_get:
										if check_note_get.taxe_montant_paye < check_note_get.taxe_montant:
											note += check_note.reference + ' pour un montant de ' + str(round( check_note.taxe_montant - check_note.taxe_montant_paye)) + 'Fbu de l\'année  ' + str(check_note.annee) + ' </br>'
											ckcf = 1

						except:
							pass
							pass
			if ckcf == 0:
				form=NoteImpositionPaiementForm(ni_pk=request.session['ni_pk'])
			else:
				data = dict()
				massage = mark_safe(note)
				context = {'message': massage}
				data['html_form'] = render_to_string('_message_erreur.html', context,request=request)
				return JsonResponse(data)
		else :
			form = NoteImpositionPaiementForm(ni_pk=request.session['ni_pk'])

	
	return save_note_imposition_paiement_form(request, form, NoteImpositionPaiementTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def note_imposition_paiement_update(request, pk):
	"""
	Modifier le paiement de la note d'imposition
	pk : Identifiant du paiement à modifier
	"""
	obj=get_object_or_404(NoteImpositionPaiement, pk=pk)
	if request.method == 'POST':
		form=NoteImpositionPaiementForm(request.POST, instance=obj, ni_pk=request.session['ni_pk'])
	else:
		form=NoteImpositionPaiementForm(instance=obj, ni_pk=request.session['ni_pk'])
	
	return save_note_imposition_paiement_form(request, form, NoteImpositionPaiementTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def note_imposition_paiement_delete(request, pk):
	"""
	Supprimer le paiement de note d'imposition
	pk : Identifiant du paiement à supprimer
	"""
	obj = get_object_or_404(NoteImpositionPaiement, pk=pk)
	data = dict()
	if request.method == 'POST':
		try:
			with transaction.atomic():
				# 1 - Supprimer l'objet paiement
				obj.delete()

				# 2 - Mettre à jour la NoteImposition.taxe_montant_paye
				obj_ni = NoteImposition.objects.get(pk=request.session['ni_pk'])
				obj_paie_lst = NoteImpositionPaiement.objects.filter(note_imposition=request.session['ni_pk'])
				somme = 0
				for o in obj_paie_lst:
					 somme += o.montant_tranche

				obj_ni.taxe_montant_paye = somme
				
				obj_ni.save() 	
		except:
			return ErrorsHelpers.show_message(request, 'Erreur de suppression de la ligne de paiement')
		
		data['form_is_valid']=True
		data['html_content_list']=render_to_string(NoteImpositionPaiementTemplate.list, context=get_context(request, request.session['ni_pk']))
		data['url_redirect'] = request.session['url_list']

	else:
		context={'note_imposition_paiement': obj} #JS ve ?
		data['html_form']=render_to_string(NoteImpositionPaiementTemplate.delete, context, request=request)
		
	return JsonResponse(data)

#----------------------------------------------------------------
def save_note_imposition_paiement_form(request, form, template_name, action):
	"""
	Sauvegarder l'objet paiement de note d'imposition
	"""
	data=dict()
	if request.method == 'POST':
		if form.is_valid():
			# Mise à jour de la traçabilité
			msg = OperationsHelpers.execute_action(request, action, form)
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid']=True
			data['html_content_list']=render_to_string(NoteImpositionPaiementTemplate.list, context=get_context(request, request.session['ni_pk']))
			data['url_redirect']=request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)
	
	context = {
		'form': form,
		'ni_pk': request.session['ni_pk'],
	}
	data['html_form']=render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def note_imposition_paiement_upload(request, pk):
	"""
	Upload File : Bordereau de versement ou autre preuve de paiement
	"""
	obj = get_object_or_404(NoteImpositionPaiement, pk=pk)
	if request.method == 'POST':
		form = NoteImpositionPaiementFileUploadForm(request.POST, request.FILES)
		if form.is_valid():			
			if form.cleaned_data['fichier_paiement'] is not None:
				obj.fichier_paiement = form.cleaned_data['fichier_paiement']
				obj.save()			

				# Recharger la page entière
				return redirect('note_imposition_paiement_list', request.session['ni_pk'])
		else:
			return ErrorsHelpers.show(request, form)
	else:
		data=dict()
		context={'note_imposition_paiement': obj}
		data['html_form']=render_to_string(NoteImpositionPaiementTemplate.upload, context, request=request)
		
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def note_imposition_paiement_upload_temp(request, pk):
	"""
	Upload File : Bordereau de versement ou autre preuve de paiement
	"""
	obj = get_object_or_404(NoteImpositionPaiement, pk=pk)
	if request.method == 'POST':
		form = NoteImpositionPaiementFileUploadForm(request.POST, request.FILES)
		if form.is_valid():			
			if form.cleaned_data['fichier_paiement'] is not None:
				obj.fichier_paiement = form.cleaned_data['fichier_paiement']
				obj.save()			

				# Recharger la page entière
				return redirect('note_imposition_paiement_list', request.session['ni_pk'])
		else:
			return ErrorsHelpers.show(request, form)
	else:
		data=dict()
		context={'note_imposition_paiement': obj}
		data['html_form']=render_to_string('note_imposition_paiement/includes/_note_imposition_paiement_upload_temp.html', context, request=request)
		
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def note_imposition_paiement_validate(request, pk):
	"""
	Validation de la ligne de paiement
	Utilisation de la transaction
	"""
	try:
		with transaction.atomic():
			ni_paiement_id = request.POST["id"]
			
			# 1 - Sauvegarder la NoteImpositionPaiement
			# Récuperer l'identifiant du paiement de la note d'imposition
			obj = get_object_or_404(NoteImpositionPaiement, pk=ni_paiement_id)

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
				
			obj.date_validate = datetime.datetime.now()
			obj.user_validate = User.objects.get(pk=request.user.id) # get current user 
			obj.save()	

			# 2 - Mettre à jour NoteImposition.taxe_montant_paye
			obj_ni = NoteImposition.objects.get(pk=pk)
			obj_paie_lst = NoteImpositionPaiement.objects.filter(note_imposition=pk)
			somme = 0
			for o in obj_paie_lst:
				 somme += o.montant_tranche

			obj_ni.taxe_montant_paye = somme
			
			obj_ni.save() 
	except:
		return ErrorsHelpers.show_message(request, 'Erreur de validation de la ligne de paiement')

	data=dict()
	data['url_redirect']=request.session['url_list']
	data['html_content_list']=render_to_string(NoteImpositionPaiementTemplate.list, context=get_context(request, pk))
	
	return JsonResponse(data)