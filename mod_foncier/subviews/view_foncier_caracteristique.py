from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_operations import OperationsHelpers

from mod_foncier.subviews.view_foncier_helpers import *
from mod_foncier.models import *
from mod_foncier.forms import *
from mod_foncier.templates import *

#----------------------------------------------------------------
#--- CRUD Caractéristique des contructions durant l'expertise ---
#----------------------------------------------------------------

def foncier_expertise_caracteristique(request, pk):
	"""
	Liste des caractéristique d'une expertise
	"""
	obj = get_object_or_404(FoncierExpertise, pk=pk)
	lstCara = FoncierCaracteristique.objects.all().filter(expertise_id=pk)
	
	form = FoncierCaracteristiqueForm(expertise = obj)
	context = {'objPar': obj, 'lstCara': lstCara , 'form': form}
	
	data = dict()	
	data['html_form'] = render_to_string(FoncierExpertiseTemplate.caracteristique, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_expertise_caracteristique_create(request):
	"""
	Création/Ajout d'une caratéristique à la contruction
	"""
	# Récuperer id parcelle et id construction
	try:
		with transaction.atomic():
			expertise_id = request.POST["idExpertise"]
			obj_expertise = get_object_or_404(FoncierExpertise, pk=expertise_id)

			impot_id = request.POST["idImpot"]
			obj_impot_batie = get_object_or_404(FoncierImpot, pk=impot_id)

			superficie_batie= request.POST["idSuperficieBatie"] 

			objCara = FoncierCaracteristique()
			objCara.expertise = obj_expertise
			objCara.impot_batie = obj_impot_batie
			objCara.superficie_batie = superficie_batie
			objCara.save()

			# Calculer le montant de l'impot (terrain non bati et construction)
			somme_taxe, tnb, tb = get_montant_note(obj_expertise)
			obj_expertise.montant_tb = tb
			obj_expertise.save()
	except:
		return ErrorsHelpers.show_message(request, "Erreur d'enregistrement des caratéristiques.")
	
	# Definir le context
	lstCara = FoncierCaracteristique.objects.all().filter(expertise_id=expertise_id)
	form = FoncierCaracteristiqueForm()
	context = {'objPar': obj_expertise, 'lstCara': lstCara , 'form': form}

	data = dict()
	data['html_content_list'] = render_to_string(FoncierExpertiseTemplate.caracteristique_liste, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_expertise_caracteristique_delete(request):
	"""
	Suppression d'une caractéristqiue d'une contruction
	"""
	try:
		with transaction.atomic():
			# Récuperer id parcelle et id construction
			expertise_id = request.POST["idExpertise"]
			obj_expertise = get_object_or_404(FoncierExpertise, pk=expertise_id)

			caracteristique_id = request.POST["idCaracteristique"]
			obj_caracteristique = get_object_or_404(FoncierCaracteristique, pk=caracteristique_id)
			obj_caracteristique.delete()

			# Calculer le montant de l'impot (terrain non bati et construction)
			somme_taxe, tnb, tb = get_montant_note(obj_expertise)
			obj_expertise.montant_tb = tb
			obj_expertise.save()
	except:
		return ErrorsHelpers.show_message(request, "Erreur d'enregistrement des caratéristiques.")

	# Definir le context
	lstCara = FoncierCaracteristique.objects.all().filter(expertise_id=expertise_id)
	form = FoncierCaracteristiqueForm()
	context = {'objPar': obj_expertise, 'lstCara': lstCara , 'form': form}

	data = dict()
	data['html_content_list'] = render_to_string(FoncierExpertiseTemplate.caracteristique_liste, context, request=request)

	return JsonResponse(data)