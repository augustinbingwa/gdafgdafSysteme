from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.views.decorators.csrf import csrf_exempt

from mod_finance.models import NoteImpositionPaiement

from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_validators import *

from mod_parametrage.enums import *

#-------------------------------------------------------
#------- CENTRALISATION JOURNALIERE DES RECETTES -------
#-------------------------------------------------------

def get_list_by_criteria(request, by_paginator = True):
	"""
	Renvoie la liste des recettes avec criteria
	"""
	query = Q(note_imposition__taxe__categorie_taxe__type_impot = 1)
	
	# Variables session DATE
	recette_date_du_jour = SessionHelpers.init_variables(request, 'recette_date_du_jour')

	# Variable session des MODULES
	recette_module = SessionHelpers.init_variables(request, 'recette_module')

	# Titre du Module
	recette_module_titre = ''

	if recette_module=='1': 
		query &= SessionHelpers.get_query(None, Q(note_imposition__entity = ENTITY_IMPOT_FONCIER)) # 10	
		recette_module_titre = 'IMPÔT FONCIER'
	elif recette_module=='2':
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_ACTIVITE_STANDARD)) # 1
		recette_module_titre = 'ACTIVITÉ STANDARD'
	elif recette_module=='3':
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_ACTIVITE_MARCHE)) # 2
		recette_module_titre = 'ACTIVITÉ MARCHÉ'
	elif recette_module=='4':
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_VEHICULE_ACTIVITE)) # 11
		recette_module_titre = 'ACTIVITÉ TRANSPORT'
	elif recette_module=='5':
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_DROIT_STATIONNEMENT)) # 12
		recette_module_titre = 'DROIT DE STASTIONNEMENT'
	elif recette_module=='6':
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_VEHICULE_PROPRIETE)) # 13
		recette_module_titre = 'IMPÔT PROPRIÉTAIRE'
	elif recette_module=='7':
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_PUBLICITE_MUR_CLOTURE)) # 7
		recette_module_titre = 'PUBLICITÉ'
	elif recette_module=='8':
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_ALLOCATION_ESPACE_PUBLIQUE)) # 5
		recette_module_titre = 'ESPACE PUBLICQUE'
	elif recette_module=='9':
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE)) # 6
		recette_module_titre = 'PANNEAU PUBLICITAIRE'
	elif recette_module=='10': 
		query &= SessionHelpers.get_query(query, Q(note_imposition__entity = ENTITY_ALLOCATION_PLACE_MARCHE)) # 8
		recette_module_titre = 'PLACE MARCHÉ'

	# Si période valide
	if is_date_fr_valid(recette_date_du_jour):
		du = date_picker_to_date_string(recette_date_du_jour)
		au = date_picker_to_date_string(recette_date_du_jour, True)

		# Executer la liste
		lst = NoteImpositionPaiement.objects.filter(query & Q(date_validate__range=[du, au])).order_by('note_imposition')
	else:
		# Executer la liste
		lst = NoteImpositionPaiement.objects.filter(query).order_by('note_imposition')

	# Nombre d'enregistrement
	total = lst.count

	# TOTAL DE LA SOMME
	queryset = lst.filter(query).aggregate(somme=Sum('montant_tranche'))
	somme = queryset.get('somme', 0)

	# Renvoyer le résultat de la requete filtrée avec paginator
	if by_paginator:
		return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total, somme, recette_module_titre
	else:
		return lst, total, somme, recette_module_titre

#----------------------------------------------------------------
def get_context(request, by_paginator = True):
	"""
	Renvoie les info du context
	"""
	# Charger la liste
	lst, total, somme, recette_module_titre = get_list_by_criteria(request, by_paginator)

	# Sauvegader le context
	context = {
		'lst': lst,
		'total': total,
		'somme': somme,
		'recette_module_titre': recette_module_titre,

		'recette_date_du_jour': request.session['recette_date_du_jour'],
		'recette_module': request.session['recette_module'],
	}

	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt # Pour les methode POST qui necessite crsf_token
def centralisation_journaliere_recette(request):
	"""
	Centralisation (recette)
	"""
	
	return render(request, 'page/page_centralisation_journaliere_recette.html', context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def centralisation_journaliere_recette_print_pdf(request):
	"""
	Génération Centralisation journalière des recettes
	"""
	
	# Nom du fichier template html
	filename = 'report_centralisation_journaliere_recette_print_pdf'
	
	# Generate PDF 
	return ReportHelpers.Render(request, filename, context=get_context(request, False)) # False : sans pagination dans PDF