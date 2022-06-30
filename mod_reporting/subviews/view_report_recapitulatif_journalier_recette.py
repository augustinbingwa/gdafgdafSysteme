from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Func, F
from django.views.decorators.csrf import csrf_exempt

from mod_finance.models import NoteImpositionPaiement

from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_session import SessionHelpers

from mod_parametrage.enums import *

from mod_helpers.hlp_validators import *

import calendar

#-----------------------------------------------------------------
#--- RECPITULATIF journalier DES RECETTES IMPOSES PAR MODULES ----
#-----------------------------------------------------------------
def load_list_by_entity(lst_base, entity):
	""" Charger la liste """
	lst = lst_base.filter(Q(note_imposition__entity = entity)) \
		.annotate(date_valid = Func(F('date_validate'), function='date')) \
		.values('date_valid') \
		.annotate(montant = Sum('montant_tranche')) \
		.order_by('date_valid')

	return lst

def append_list(day, lst_entity, lst_res, o, col):
	""" Ajouter un element valide dans la liste """
	for obj in lst_entity:
		date = obj['date_valid'].strftime("%d/%m/%Y")
		jour = int(obj['date_valid'].strftime("%d"))
		if day == jour:
			o['date'] = date
			o[col] = obj['montant']

			found = False
			for res in lst_res:
				if res['date'] == date:
					found = True
					break

			if not found:
				lst_res.append(o)

			break

def get_list_by_criteria(request):
	"""
	Renvoie la liste des recap/recette
	"""
	# Variable session MOIS
	recap_journalier_recette_mois = SessionHelpers.init_variables(request, 'recap_journalier_recette_mois')

	# Variables session ANNEE
	recap_journalier_recette_annee = SessionHelpers.init_variables(request, 'recap_journalier_recette_annee')

	du = au = None
	mois = ''

	if recap_journalier_recette_mois == '1': 
		mois = 'JANVIER'
		du = date_picker_to_date_string('01/01/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('31/01/' + recap_journalier_recette_annee, True)
		
	elif recap_journalier_recette_mois == '2':
		mois = 'FEVRIER'
		du = date_picker_to_date_string('01/02/' + recap_journalier_recette_annee)
		
		if is_date_fr_valid('29/02/' + recap_journalier_recette_annee):
			au = date_picker_to_date_string('29/02/' + recap_journalier_recette_annee, True)
		else:	
			au = date_picker_to_date_string('28/02/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='3':
		mois = 'MARS'
		du = date_picker_to_date_string('01/03/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('31/03/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='4':
		mois = 'AVRIL'
		du = date_picker_to_date_string('01/04/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('30/04/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='5':
		mois = 'MAI'
		du = date_picker_to_date_string('01/05/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('31/05/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='6':
		mois = 'JUIN'
		du = date_picker_to_date_string('01/06/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('30/06/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='7':
		mois = 'JUILLET'
		du = date_picker_to_date_string('01/07/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('31/07/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='8':
		mois = 'AOUT'
		du = date_picker_to_date_string('01/08/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('31/08/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='9':
		mois = 'SEPTEMBRE'
		du = date_picker_to_date_string('01/09/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('30/09/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='10': 
		mois = 'OCTOBRE'
		du = date_picker_to_date_string('01/10/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('31/10/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='11':
		mois = 'NOVEMBRE'
		du = date_picker_to_date_string('01/11/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('30/11/' + recap_journalier_recette_annee, True)

	elif recap_journalier_recette_mois=='12':
		mois = 'DECEMBRE'
		du = date_picker_to_date_string('01/12/' + recap_journalier_recette_annee)
		au = date_picker_to_date_string('31/12/' + recap_journalier_recette_annee, True)

	# Executer la liste de base
	query = Q(note_imposition__taxe__categorie_taxe__type_impot = 1) & SessionHelpers.get_query(None, Q(date_validate__range=[du, au]))
	lst_base = NoteImpositionPaiement.objects.filter(query)

	lst_foncier = load_list_by_entity(lst_base, ENTITY_IMPOT_FONCIER) # 10
	lst_standard = load_list_by_entity(lst_base, ENTITY_ACTIVITE_STANDARD) # 1
	lst_marche = load_list_by_entity(lst_base, ENTITY_ACTIVITE_MARCHE) # 2
	lst_transport = load_list_by_entity(lst_base, ENTITY_VEHICULE_ACTIVITE) # 11
	lst_stationnement = load_list_by_entity(lst_base, ENTITY_DROIT_STATIONNEMENT) # 12
	lst_propriete = load_list_by_entity(lst_base, ENTITY_VEHICULE_PROPRIETE) # 13
	lst_publicite = load_list_by_entity(lst_base, ENTITY_PUBLICITE_MUR_CLOTURE) # 7
	lst_espace_pub = load_list_by_entity(lst_base, ENTITY_ALLOCATION_ESPACE_PUBLIQUE) # 5
	lst_panneau = load_list_by_entity(lst_base, ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE) # 6
	lst_place_marche = load_list_by_entity(lst_base, ENTITY_ALLOCATION_PLACE_MARCHE) # 8

	lst_res = []

	cal = calendar.Calendar()

	# Parcourir les jours du mois choisi
	somme_foncier = 0
	somme_standard = 0
	somme_marche = 0
	somme_transport = 0
	somme_stationnement = 0
	somme_propriete = 0
	somme_publicite = 0
	somme_espace_pub = 0
	somme_panneau = 0
	somme_place_marche = 0

	# Au premier lancement
	if recap_journalier_recette_annee == '':
		recap_journalier_recette_annee = datetime.datetime.now().year
	if recap_journalier_recette_mois == '':
		recap_journalier_recette_mois = datetime.datetime.now().month

	for day in cal.itermonthdays(int(recap_journalier_recette_annee), int(recap_journalier_recette_mois)):
		if (day > 0):
			o = {
				'date': '',
				'mt_foncier': 0,
				'mt_standard': 0,
				'mt_marche': 0,
				'mt_place_marche': 0,
				'mt_transport': 0,
				'mt_stationnement': 0,
				'mt_propriete': 0,
				'mt_publicite': 0,
				'mt_panneau': 0,
				'mt_espace_pub': 0,
			}
			
			append_list(day, lst_foncier, lst_res, o, 'mt_foncier')
			append_list(day, lst_standard, lst_res, o, 'mt_standard')
			append_list(day, lst_marche, lst_res, o, 'mt_marche')
			append_list(day, lst_place_marche, lst_res, o, 'mt_place_marche')
			append_list(day, lst_transport, lst_res, o, 'mt_transport')
			append_list(day, lst_stationnement, lst_res, o, 'mt_stationnement')
			append_list(day, lst_propriete, lst_res, o, 'mt_propriete')
			append_list(day, lst_publicite, lst_res, o, 'mt_publicite')
			append_list(day, lst_panneau, lst_res, o, 'mt_panneau')
			append_list(day, lst_espace_pub, lst_res, o, 'mt_espace_pub')

			somme_foncier += o['mt_foncier']
			somme_standard += o['mt_standard']
			somme_marche += o['mt_marche']
			somme_transport += o['mt_transport']
			somme_stationnement += o['mt_stationnement']
			somme_propriete += o['mt_propriete']
			somme_publicite += o['mt_publicite']
			somme_espace_pub += o['mt_espace_pub']
			somme_panneau += o['mt_panneau']
			somme_place_marche += o['mt_place_marche']

	o = {
		'date': 'TOTAL MOIS',
		'mt_foncier': somme_foncier,
		'mt_standard': somme_standard,
		'mt_marche': somme_marche,
		'mt_place_marche': somme_place_marche,
		'mt_transport': somme_transport,
		'mt_stationnement': somme_stationnement,
		'mt_propriete': somme_propriete,
		'mt_publicite': somme_publicite,
		'mt_panneau': somme_panneau,
		'mt_espace_pub': somme_espace_pub,
	}

	lst_res.append(o)

	count = len(lst_res)

	"""
	select mod_finance_noteimpositionpaiement.date_validate::date, sum(mod_finance_noteimpositionpaiement.montant_tranche) as montant from mod_finance_noteimpositionpaiement
	inner join mod_finance_noteimposition on mod_finance_noteimposition.id = mod_finance_noteimpositionpaiement.note_imposition_id
	where mod_finance_noteimposition.entity = 10 and (mod_finance_noteimpositionpaiement.date_validate::date >= '2019-01-01' and mod_finance_noteimpositionpaiement.date_validate::date <= '2019-01-31')
	group by mod_finance_noteimpositionpaiement.date_validate::date order by mod_finance_noteimpositionpaiement.date_validate::date ASC
	"""

	return lst_res, count, mois

#----------------------------------------------------------------
def get_context(request):
	"""
	Renvoie les info du context
	"""
	# Charger la liste
	lst, count, mois = get_list_by_criteria(request)

	# Sauvegarder le context
	context = {
		'lst': lst,
		'count': count,
		'mois': mois,
		
		'recap_journalier_recette_annee': request.session['recap_journalier_recette_annee'],
		'recap_journalier_recette_mois': request.session['recap_journalier_recette_mois'],
	}

	return context

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt # Pour les methode POST qui necessite crsf_token
def recapitulatif_journalier_recette(request):
	"""
	Recapitulatif journalier des recettes
	"""

	return render(request, 'page/page_recapitulatif_journalier_recette.html', context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def recapitulatif_journalier_recette_print_pdf(request):
	"""
	Génération Recapitulatif journalier des recettes
	"""

	# Nom du fichier template html
	filename = 'report_recapitulatif_journalier_recette_print_pdf'
	
	# Generate PDF 
	return ReportHelpers.Render(request, filename, context=get_context(request))