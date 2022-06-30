from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string
from django.contrib.auth.models import User

from mod_helpers.forms import * 
from mod_helpers.templates import NoteTemplate
from mod_helpers.hlp_error import ErrorsHelpers

from mod_crm.models import PersonnePhysique

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#------------------------------------------------------------
def get_ni_view_name_by_entity(entity):
	"""
	Traitement spécifique de la note d'imposition qui ne représente qu'un seul modele et de plusieurs views
	basées des ENTITY (voir enums)
	"""
	view_name = ''
	
	if entity == ENTITY_ACTIVITE_STANDARD:
		view_name = 'ni_activite_standard_list'
	elif entity == ENTITY_ACTIVITE_MARCHE:
		view_name = 'ni_activite_marche_list'	
	#elif entity == ENTITY_ACTIVITE_EXCEPTIONNELLE:
	#	view_name = 'ni_activite_exceptionnelle_list'
	#elif entity == ENTITY_VISITE_TOURISTIQUE:
	#	view_name = 'ni_visite_touristique_list'
	elif entity == ENTITY_ALLOCATION_ESPACE_PUBLIQUE:
		view_name = 'ni_allocation_espace_publique_list'
	elif entity == ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:
		view_name = 'ni_allocation_panneau_publicitaire_list'
	elif entity == ENTITY_PUBLICITE_MUR_CLOTURE:
		view_name = 'ni_publicite_mur_cloture_list'
	elif entity == ENTITY_ALLOCATION_PLACE_MARCHE:
		view_name = 'ni_allocation_place_marche_list'
	elif entity == ENTITY_BATIMENTS_MUNICIPAUX:
		view_name = 'ni_batments_municipaux_list'
	elif entity == ENTITY_IMPOT_FONCIER:
		view_name = 'ni_impot_foncier_list'
	elif entity == ENTITY_VEHICULE_ACTIVITE:
		view_name = 'ni_vehicule_activite_list'
	elif entity == ENTITY_DROIT_STATIONNEMENT:
		view_name = 'ni_droit_stationnement_list'
	elif entity == ENTITY_VEHICULE_PROPRIETE:
		view_name = 'ni_vehicule_proprietaire_list'

	return view_name

#------------------------------------------------------------
def edit_note(request, pk, class_name, view_name):
	"""
	Editer la note
	Exemple : mod_crm.submodels.model_contribuable.PersonnePhysique
	"""
	if not class_name:
		return redirect('home')

	class_name = import_string(class_name)

	obj = get_object_or_404(class_name, pk=pk)

	# Traitement des cas spécifique (la note d'imposition ne représente qu'un seul modele -> plusieurs views)
	if view_name=='note_imposition':
		view_name = get_ni_view_name_by_entity(obj.entity)

	data = dict()
	if request.method == 'POST':
		form = NoteForm(request.POST)
		if form.is_valid():
			# Requette
			if obj.note is None:
				obj.note = form.cleaned_data['note']
			
			if not obj.user_note:
				obj.user_note = User.objects.get(pk=request.user.id) # get current user 

			if not obj.date_note:
				obj.date_note = datetime.datetime.now(tz=timezone.utc) # get current date
			
			# Réponse
			if form.cleaned_data['reponse_note'] is not None:
				obj.reponse_note = form.cleaned_data['reponse_note']

			if form.cleaned_data['demande_annulation_validation']:
				obj.demande_annulation_validation = form.cleaned_data['demande_annulation_validation']

			obj.save()
				
			return redirect(view_name)
		else:
			return ErrorsHelpers.show(request, form)
	else:	
		context = {'obj': obj}
		data['html_form'] = render_to_string(NoteTemplate.edit, context, request=request)

	return JsonResponse(data)

#------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def unvalidate_entity(request):
	"""
	Annuler la validation d'un objet ou entité
	"""
	obj =  None

	try:
		# Identifiant de l'entty
		id = request.POST["id"]

		class_name = classe_module = request.POST["class_name"]
		classe_module = classe_module.split('.')[-1]
		
		class_name = import_string(class_name)
		obj = get_object_or_404(class_name, pk=id)

		# Si l'instance en cours (voir model) possède un champs date_ecriture et que cette dernière n'est pas nulle
		if hasattr(obj, 'date_ecriture'):
			if obj.date_ecriture:
				return ErrorsHelpers.show_message(request, "Erreur d'annulation de validation de l'objet n°" + str(obj) + " (" + str(classe_module) + "), une <em class='text-primary'>note d'imposition</em> a été déjà générée.")

		# Annuler la validation de l'objet
		obj.date_validate = None
		obj.user_validate = None

		# Mettre à jour l'annulation (user, datetime)
		obj.date_cancel = datetime.datetime.now(tz=timezone.utc)  
		obj.user_cancel = User.objects.get(pk=request.user.id) # Current user (c'est l'admin)

		obj.save()
	except:
		if not obj:
			return 	ErrorsHelpers.show_message(request, "Erreur d'annulation de la validation, l'objet seléctionné est n'est pas defini.")
		return ErrorsHelpers.show_message(request, "Erreur d'annulation de la validation de l'objet " + str(obj))
	
	data = dict()
	data['url_redirect'] = request.session['url_list']

	return JsonResponse(data)