from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

import json

from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers

from mod_finance.models import *
from mod_finance.forms import *
from mod_finance.templates import *

from mod_parametrage.enums import *

from mod_transport.models import *
from mod_activite.models import *
from mod_foncier.models import *
import datetime
#----------------------------------------------------------------
#-------------- IMPRESSION DE LA NOTE D'IMPOSITION --------------
#----------------------------------------------------------------
@login_required(login_url="login/")
def ni_print_pdf(request, pk):
	"""
	Impression de la note d'imposition de la carte de proprietaire des véhicules sans carte rose
	"""
	# Nom du fichier template html
	filename = 'note_imposition_print'
	filename_foncier = 'note_imposition_foncier_print'

	obj = NoteImposition.objects.get(pk=pk)
	objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
	datenow = datetime.datetime.now()

	if obj and obj.is_valid: # Note validée
		# Objet entity (VehiculeProprietaire, VehiculeActivite, ActiviteBase, etc.)
		obj_entity = None

		if obj.entity == ENTITY_ACTIVITE_STANDARD:	
			obj_entity = Standard.objects.get(id=obj.entity_id)
		if obj.entity == ENTITY_ACTIVITE_MARCHE:	
			obj_entity = Marche.objects.get(id=obj.entity_id)
		if obj.entity == ENTITY_ALLOCATION_ESPACE_PUBLIQUE:	
			obj_entity = AllocationEspacePublique.objects.get(id=obj.entity_id)
		if obj.entity == ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:	
			obj_entity = AllocationPanneauPublicitaire.objects.get(id=obj.entity_id)
		if obj.entity == ENTITY_PUBLICITE_MUR_CLOTURE:	
			obj_entity = PubliciteMurCloture.objects.get(id=obj.entity_id)
		if obj.entity == ENTITY_ALLOCATION_PLACE_MARCHE:	
			obj_entity = AllocationPlaceMarche.objects.get(id=obj.entity_id)
		#if obj.entity == ENTITY_BATIMENTS_MUNICIPAUX:	
			#obj_entity = BatimentMunicipaux.objects.get(id=obj.entity_id)

		# Transport
		if obj.entity == ENTITY_VEHICULE_PROPRIETE:	
			obj_entity = VehiculeProprietaire.objects.get(id=obj.entity_id)
		elif obj.entity == ENTITY_VEHICULE_ACTIVITE:	
			obj_entity = VehiculeActivite.objects.get(id=obj.entity_id)
		elif obj.entity == ENTITY_DROIT_STATIONNEMENT:	
			obj_entity = VehiculeActivite.objects.get(id=obj.entity_id)
		elif obj.entity == ENTITY_IMPOT_FONCIER:	
			obj_entity = FoncierExpertise.objects.get(id=obj.entity_id)

		# Impot foncier
		elif obj.entity == ENTITY_IMPOT_FONCIER:	
			obj_entity = FoncierExpertise.objects.get(id=obj.entity_id)

		if obj_entity:
			# Action save print
			OperationsHelpers.execute_action_print(request, obj)
			reste = obj.taxe_montant - obj.taxe_montant_paye
			majoration_taxe =objExpr.montant_tb + objExpr.montant_tnb + objExpr.accroissement_montant
			print(majoration_taxe,objExpr.montant_tb ,objExpr.montant_tnb , objExpr.accroissement_montant)
			nb_month = objExpr.intere_taux
			# Definir le context
			context = {'obj': obj,'reste':reste,'nb_month':nb_month,'objExpr':objExpr,'majoration_taxe':majoration_taxe,'date':datenow,'obj_entity':obj_entity, 'user': User.objects.get(pk=request.user.id)}

			# TRAITEMENT SPECIFIQUE DE LA NOTE IMPOT FONCIER
			if obj.entity == ENTITY_IMPOT_FONCIER:
				filename = filename_foncier
				lstCara = FoncierCaracteristique.objects.all().filter(expertise_id=obj_entity.id)
				context['lstCara'] = lstCara

			# Generate PDF
			return ReportHelpers.Render(request, filename, context) 

	return ErrorsHelpers.show_message(request, "Erreur d'impression de la note d'imposition")

#----------------------------------------------------------------
#----- IMPRESSION DE LA QUITTANCE DE LA NOTE D'IMPOSITION -------
#----------------------------------------------------------------
def ni_save_form(request, form, template_name, action):
	"""
	Sauvegarde des informations de la carte de propriétaire
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			OperationsHelpers.execute_action(request, 'print', form)
			
			data['form_is_valid'] = True
		else:
			return ErrorsHelpers.show(request, form)

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def ni_quittance_print(request, pk):
	"""
	Mise à jour du numero_carte_physique du modèle NoteImposition avant impression
	"""
	obj = get_object_or_404(NoteImposition, pk=pk)
	if request.method == 'POST':
		form = NoteImpositionPrintForm(request.POST, instance=obj)
	else:
		form = NoteImpositionPrintForm(instance=obj)

	return ni_save_form(request, form, NoteImpositionPrintTemplate.print, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def ni_quittance_print_authorization(request, pk):
	"""
	Demander d'autorisation d'impression de la quittance (car le nombre MAX_NUMBER est atteint)
	"""
	obj = get_object_or_404(VehiculeActivite, pk=pk)
	if request.method == 'POST':
		form = NoteImpositionPrintAuthorizationForm(request.POST, instance=obj)
	else:
		form = NoteImpositionPrintAuthorizationForm(instance=obj) 

	return ni_save_form(request, form, NoteImpositionPrintTemplate.print_authorization, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def ni_quittance_print_confirm(request, pk):
	"""
	Confirmer l'impression de la quittance de la note
	"""
	data = dict()
	success = 'true'
	message = ''

	try:
		obj = get_object_or_404(NoteImposition, pk=pk)
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
def ni_quittance_print_pdf(request, pk):
	"""
	Impression de la quittante de la note d'imposition
	"""
	# Nom du fichier template html à generer
	filename = 'note_imposition_quittance_print'

	# L'objet note d'imposition validée et payée
	obj = NoteImposition.objects.get(pk=pk)

	obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
	if obj.nombre_impression >= int(obj_gv.valeur):
		# Empecher le download du PDF
		return ni_quittance_print_confirm(request, pk)
	else:
		if obj and obj.is_payed: # + Payement effectué
			# Objet entity (VehiculeProprietaire, VehiculeActivite, ActiviteBase, etc.)
			obj_entity = None

			# Activité
			if obj.entity == ENTITY_ACTIVITE_STANDARD:	
				obj_entity = Standard.objects.get(id=obj.entity_id)

			if obj.entity == ENTITY_ACTIVITE_MARCHE:	
				obj_entity = Marche.objects.get(id=obj.entity_id)

			if obj.entity == ENTITY_ALLOCATION_ESPACE_PUBLIQUE:	
				obj_entity = AllocationEspacePublique.objects.get(id=obj.entity_id)

			if obj.entity == ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE:	
				obj_entity = AllocationPanneauPublicitaire.objects.get(id=obj.entity_id)

			if obj.entity == ENTITY_PUBLICITE_MUR_CLOTURE:	
				obj_entity = PubliciteMurCloture.objects.get(id=obj.entity_id)

			if obj.entity == ENTITY_ALLOCATION_PLACE_MARCHE:	
				obj_entity = AllocationPlaceMarche.objects.get(id=obj.entity_id)

			#if obj.entity == ENTITY_BATIMENTS_MUNICIPAUX:	
			#	obj_entity = BatimentMunicipaux.objects.get(id=obj.entity_id)

			# Transport
			if obj.entity == ENTITY_VEHICULE_PROPRIETE:	
				obj_entity = VehiculeProprietaire.objects.get(id=obj.entity_id)
			elif obj.entity == ENTITY_VEHICULE_ACTIVITE:	
				obj_entity = VehiculeActivite.objects.get(id=obj.entity_id)
			elif obj.entity == ENTITY_DROIT_STATIONNEMENT:	
				obj_entity = VehiculeActivite.objects.get(id=obj.entity_id)
			elif obj.entity == ENTITY_DROIT_STATIONNEMENT:	
				obj_entity = VehiculeActivite.objects.get(id=obj.entity_id)

			# Impot foncier
			elif obj.entity == ENTITY_IMPOT_FONCIER:	
				obj_entity = FoncierExpertise.objects.get(id=obj.entity_id)

			if obj_entity:
				# Action save print
				obj.nombre_impression += 1

				# Action save print
				OperationsHelpers.execute_action_print(request, obj)

				# Definir le context
				context = {'obj': obj,'obj_entity': obj_entity, 'qr_options': ReportHelpers.get_qr_options(), 'qr_data':get_qr_data(obj), 'user': User.objects.get(pk=request.user.id)}

				# Generate PDF
				return ReportHelpers.Render(request, filename, context) 

		return ErrorsHelpers.show_message(request, "Erreur d'impression de la quittance de la note d'impostion")

#----------------------------------------------------------------
def get_qr_data(obj):
	"""
	Composition des données du qr code
	"""
	if isinstance(obj, NoteImposition):	
		return 'Réf: {} \nMatricule:  {} \nNom: {} \nPériode: {} \nAnnée: {} \nMontant: {} \nDate: {}'.format(
			obj.reference , 
			obj.contribuable.matricule,
			obj.contribuable.nom,
			obj.periode.get_element_display(),
			obj.annee,
			obj.taxe_montant_paye,
			obj.date_print.strftime('%Y-%m-%d %H:%M:%S'))

	return 'GDAF'