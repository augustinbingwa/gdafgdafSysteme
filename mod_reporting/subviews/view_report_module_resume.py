from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Sum

from mod_finance.models import NoteImposition

from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_session import SessionHelpers

from mod_helpers.hlp_validators import *

from mod_parametrage.enums import *

#----------------------------------------------------------------
#-------------------- VIEW RESUME MODULE ------------------------
#----------------------------------------------------------------
def load_data_by_entity(lst_base, entity_name, entity):
	""" Charger la liste de l'entité """
	lst = lst_base.filter(Q(entity = entity))

	# Total des dclarants (UNIQUE)
	nbr_declarant = lst.values('contribuable').distinct().count()

	# Total des dclarants physiques (UNIQUE)
	nbr_phyique = lst.filter(contribuable__matricule__startswith = '180').values('contribuable').distinct().count()

	# Total des dclarants morales (UNIQUE)
	nbr_morale = lst.filter(contribuable__matricule__startswith = '181').values('contribuable').distinct().count()
	
	# Nombre de recettes
	queryset = lst.aggregate(count=Count('reference'))
	nbr_note_imposee = queryset.get('count', 0)

	# Nombre des notes paées
	queryset = lst.filter(Q(taxe_montant_paye__gt = 0)).aggregate(count=Count('reference'))
	nbr_recette = queryset.get('count', 0)

	# Nombre des notes impayées
	queryset = lst.filter(Q(taxe_montant_paye__lte = 0)).aggregate(count=Count('reference'))
	nbr_note_impayee = queryset.get('count', 0)

	# Total de notes imposées
	queryset = lst.aggregate(somme=Sum('taxe_montant'))
	total_imposee = queryset.get('somme', 0)
	if total_imposee is None: total_imposee =0

	# Total de recettes
	queryset = lst.aggregate(somme = Sum('taxe_montant_paye'))
	total_recette = queryset.get('somme', 0)
	if total_recette is None: total_recette =0

	# Total des impayées
	queryset = lst.filter(Q(taxe_montant_paye = 0)).aggregate(somme = Sum('taxe_montant'))
	total_impayee = queryset.get('somme', 0)
	if total_impayee is None: total_impayee =0

	o = {
		'module': entity_name,
		'nbr_declarant': nbr_declarant,
		'nbr_phyique': nbr_phyique,
		'nbr_morale': nbr_morale,
		'nbr_note_imposee': nbr_note_imposee,
		'nbr_recette': nbr_recette,
		'nbr_note_impayee': nbr_note_impayee,
		'total_imposee': total_imposee,
		'total_recette': total_recette,
		'total_impayee': total_impayee,
	}

	return o

def get_list_by_criteria(request):
	"""
	Renvoie la liste des résumés de chaque module selon le criteria
	"""
	# Variable session de la priode
	module_resume_du = SessionHelpers.init_variables(request, 'module_resume_du')
	module_resume_au = SessionHelpers.init_variables(request, 'module_resume_au')

	du = date_picker_to_date_string(module_resume_du)
	au = date_picker_to_date_string(module_resume_au, True)

	# Executer la liste de base
	query = Q(taxe__categorie_taxe__type_impot = 1) & SessionHelpers.get_query(None, Q(date_validate__range=[du, au]))
	lst_base = NoteImposition.objects.filter(query)

	lst_res = []

	lst_res.append(load_data_by_entity(lst_base, 'IMPÔTS FONCIERS', ENTITY_IMPOT_FONCIER)) # 10
	lst_res.append(load_data_by_entity(lst_base, 'ACTIVITÉS STANDARD', ENTITY_ACTIVITE_STANDARD)) # 1
	lst_res.append(load_data_by_entity(lst_base, 'ACTIVITÉS DANS LES MARCHÉS', ENTITY_ACTIVITE_MARCHE)) # 2
	lst_res.append(load_data_by_entity(lst_base, 'TRANPORT RÉMUNÉRÉ', ENTITY_VEHICULE_ACTIVITE)) # 11
	lst_res.append(load_data_by_entity(lst_base, 'DROIT DE STATIONNEMENT', ENTITY_DROIT_STATIONNEMENT)) # 12
	lst_res.append(load_data_by_entity(lst_base, 'IMPÔTS SUR LA PROPRIÉTÉ', ENTITY_VEHICULE_PROPRIETE)) # 13
	lst_res.append(load_data_by_entity(lst_base, 'PUBLICITÉS SUR LES MURS/CLÔTURES', ENTITY_PUBLICITE_MUR_CLOTURE)) # 7
	lst_res.append(load_data_by_entity(lst_base, 'ALLOCATION DES ESPACES PUBLIQUES', ENTITY_ALLOCATION_ESPACE_PUBLIQUE)) # 5
	lst_res.append(load_data_by_entity(lst_base, 'PANNEAUX PUBLICITAIRES', ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE)) # 6
	lst_res.append(load_data_by_entity(lst_base, 'PLACES DANS LES MARCHÉS', ENTITY_ALLOCATION_PLACE_MARCHE)) # 8

	# Sommer la lite
	somme_declarant = 0
	somme_phyique = 0
	somme_morale = 0
	somme_note_imposee = 0
	somme_recette = 0
	somme_note_impayee = 0
	somme_total_imposee = 0
	somme_total_recette = 0
	somme_total_impayee = 0

	for o in lst_res:
		somme_declarant += o['nbr_declarant']
		somme_phyique += o['nbr_phyique']
		somme_morale += o['nbr_morale']
		somme_note_imposee += o['nbr_note_imposee']
		somme_recette += o['nbr_recette']
		somme_note_impayee += o['nbr_note_impayee']
		somme_total_imposee += o['total_imposee']
		somme_total_recette += o['total_recette']
		somme_total_impayee += o['total_impayee']

	o = {
		'module': 'TOTAL',
		'nbr_declarant': somme_declarant,
		'nbr_phyique': somme_phyique,
		'nbr_morale': somme_morale,
		'nbr_note_imposee': somme_note_imposee,
		'nbr_recette': somme_recette,
		'nbr_note_impayee': somme_note_impayee,
		'total_imposee': somme_total_imposee,
		'total_recette': somme_total_recette,
		'total_impayee': somme_total_impayee,
	}

	lst_res.append(o)

	count = len(lst_res)

	return lst_res, count

#----------------------------------------------------------------
def get_context(request):
	"""
	Renvoie les info du context
	"""
	# Charger la liste
	lst, count = get_list_by_criteria(request)

	# Sauvegarder le context
	context = {
		'lst': lst,
		'count': count,

		'module_resume_du': request.session['module_resume_du'],
		'module_resume_au': request.session['module_resume_au'],
	}

	return context

#----------------------------------------------------------------	
@login_required(login_url="login/")
@csrf_exempt # Pour les methode POST qui necessite crsf_token
def report_module_resume(request):
	"""
	Resumé des modules
	"""

	return render(request, 'page/page_module_resume.html', context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def report_module_resume_print_pdf(request):
	"""
	Imprimer LE résumé des modules
	"""
	# Nom du fichier template html
	filename = 'report_module_resume_print_pdf'
	
	# Generate PDF
	return ReportHelpers.Render(request, filename, context=get_context(request))