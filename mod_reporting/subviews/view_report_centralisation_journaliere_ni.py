from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.views.decorators.csrf import csrf_exempt

from mod_finance.models import NoteImposition

from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_validators import *

from mod_parametrage.enums import *

#-----------------------------------------------------------------
#------- CENTRALISATION JOURNALIERE DES NOTES D'IMPOSITION -------
#-----------------------------------------------------------------

def get_list_by_criteria(request, by_paginator = True):
	"""
	Renvoie la liste des recettes avec criteria
	"""
	query = Q(taxe__categorie_taxe__type_impot = 1)
	
	# Variables session DATE
	ni_date_du_jour = SessionHelpers.init_variables(request, 'ni_date_du_jour')

	# Variable session des MODULES
	ni_module = SessionHelpers.init_variables(request, 'ni_module')

	# Titre du Module
	ni_module_titre = ''

	if ni_module=='1': 
		query &= SessionHelpers.get_query(None, Q(entity = ENTITY_IMPOT_FONCIER)) # 10	
		ni_module_titre = 'IMPÔT FONCIER'
	elif ni_module=='2':
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_ACTIVITE_STANDARD)) # 1
		ni_module_titre = 'ACTIVITÉ STANDARD'
	elif ni_module=='3':
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_ACTIVITE_MARCHE)) # 2
		ni_module_titre = 'ACTIVITÉ MARCHÉ'
	elif ni_module=='4':
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_VEHICULE_ACTIVITE)) # 11
		ni_module_titre = 'ACTIVITÉ TRANSPORT'
	elif ni_module=='5':
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_DROIT_STATIONNEMENT)) # 12
		ni_module_titre = 'DROIT DE STASTIONNEMENT'
	elif ni_module=='6':
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_VEHICULE_PROPRIETE)) # 13
		ni_module_titre = 'IMPÔT PROPRIÉTAIRE'
	elif ni_module=='7':
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_PUBLICITE_MUR_CLOTURE)) # 7
		ni_module_titre = 'PUBLICITÉ'
	elif ni_module=='8':
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_ALLOCATION_ESPACE_PUBLIQUE)) # 5
		ni_module_titre = 'ESPACE PUBLICQUE'
	elif ni_module=='9':
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE)) # 6
		ni_module_titre = 'PANNEAU PUBLICITAIRE'
	elif ni_module=='10': 
		query &= SessionHelpers.get_query(query, Q(entity = ENTITY_ALLOCATION_PLACE_MARCHE)) # 8
		ni_module_titre = 'PLACE MARCHÉ'

	# Si période valide
	if is_date_fr_valid(ni_date_du_jour):
		du = date_picker_to_date_string(ni_date_du_jour)
		au = date_picker_to_date_string(ni_date_du_jour, True)

		# Executer la liste
		lst = NoteImposition.objects.filter(query & Q(date_validate__range=[du, au])).order_by('reference')
	else:
		# Executer la liste
		lst = NoteImposition.objects.filter(query).order_by('reference')	

	# Nombre d'enregistrement
	total = lst.count

	# TOTAL DE LA SOMME
	queryset = lst.filter(query).aggregate(somme=Sum('taxe_montant'))
	somme = queryset.get('somme', 0)

	# Renvoyer le résultat de la requete filtrée avec paginator
	if by_paginator:
		return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total, somme, ni_module_titre
	else:
		return lst, total, somme, ni_module_titre

#----------------------------------------------------------------
def get_context(request, by_paginator = True):
	"""
	Renvoie les info du context
	"""
	# Charger la liste
	lst, total, somme, ni_module_titre = get_list_by_criteria(request, by_paginator)

	# Sauvegader le context
	context = {
		'lst': lst,
		'total': total,
		'somme': somme,
		'ni_module_titre': ni_module_titre,

		'ni_date_du_jour': request.session['ni_date_du_jour'],
		'ni_module': request.session['ni_module'],
	}

	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt # Pour les methode POST qui necessite crsf_token
def centralisation_journaliere_ni(request):
	"""
	Centralisation (note d'imposition)
	"""
	
	return render(request, 'page/page_centralisation_journaliere_ni.html', context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def centralisation_journaliere_ni_print_pdf(request):
	"""
	Génération Centralisation journalière des notes d'imposition
	"""
	
	# Nom du fichier template html
	filename = 'report_centralisation_journaliere_ni_print_pdf'
	
	# Generate PDF 
	return ReportHelpers.Render(request, filename, context=get_context(request, False)) # False : sans pagination dans PDF