from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt #Utiliser pour les methode POST
from django.db.models import Q

from mod_activite.models import *

import json

#----------------------------------------------------------------
def activite_auto_complete(request):
	"""
	Auto complete pour activité standard et marché
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(numero_activite__icontains=term)
		lst = BaseActivite.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['label'] = item.numero_activite + ' - ' + item.contribuable.nom
			obj_json['value'] = item.id 
			obj_json['contribuable'] = item.contribuable.nom
			obj_json['taxe'] = item.taxe.id #Taxe
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def activite_standard_auto_complete(request):
	"""
	Auto complete pour activité standard
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(numero_activite__icontains=term)
		lst = Standard.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['label'] = item.numero_activite
			obj_json['value'] = item.id 
			obj_json['contribuable_id'] = item.contribuable.id
			obj_json['contribuable_nom'] = item.contribuable.matricule + ' - ' + item.contribuable.nom
			obj_json['taxe_id'] = item.taxe.id
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def activite_marche_auto_complete(request):
	"""
	Auto complete pour activité dans le marché
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(numero_activite__icontains=term)
		lst = Marche.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['label'] = item.numero_activite + ' - ' + item.contribuable.nom
			obj_json['value'] = item.id 
			obj_json['contribuable'] = item.contribuable.nom
			obj_json['taxe'] = item.taxe.id #Taxe
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)


#----------------------------------------------------------------
def activite_publique_auto_complete(request):
	"""
	Auto complete pour activité des sociétés publiques
	"""
	if request.is_ajax():
		term = request.GET.get('term', '') 
		query = Q(numero_activite__icontains=term) & Q(taxe__categorie_taxe = 7)
		lst = Standard.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['label'] = item.numero_activite
			obj_json['value'] = item.id 
			obj_json['contribuable'] = item.contribuable.matricule + ' - ' + item.contribuable.nom
			obj_json['taxe'] = item.taxe.id #Taxe
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'
	
	return HttpResponse(data, mimetype)
	
#----------------------------------------------------------------
def droit_place_marche_autocomplete(request):
	"""
	Autocomplete pour la recherche d'un nom de marché avec ses infos
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		
		lst = DroitPlaceMarche.objects.all().extra(
			where=["CONCAT(nom_marche_id, '' ,numero_place) LIKE %s"], params=[term + '%']
		)
		
		i = 0
		results = []
		for item in lst:
			obj_json = {}

			status = ''
			if item.occupee    :
				status = ' - (OCCUPÉE)'
			else:
				status = ' - (DISPONIBLE)'
	
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.nom_marche.nom + ' - Place n°' + item.numero_place + ' - Coût: ' + str(item.cout_place) + ' BIF' + status
			obj_json['cout_place'] = str(item.cout_place)

			results.append(obj_json)
			i += 1
			if i>=10:
				break;
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def allocation_place_marche_autocomplete(request):
	"""
	Autocomplete pour la recherche d'une allocation de place dans les marchés avec ses infos
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query =  Q(date_validate__isnull=False) & (Q(contribuable__matricule__icontains=term) | Q(contribuable__nom__icontains=term) | Q(droit_place_marche__nom_marche__nom__icontains=term) | Q(droit_place_marche__numero_place__icontains=term))
		
		lst = AllocationPlaceMarche.objects.filter(query)[:10]
		
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.droit_place_marche.nom_marche.nom.capitalize() + ' - place n°' + item.droit_place_marche.numero_place + ' par '+ item.contribuable.matricule + ' - ' + item.contribuable.nom
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def allocation_parcelle_publique_autocomplete(request):
	"""
	Autocomplete pour la recherche d'une allocation de l'espace/parcelle publique avec ses infos
	Condition : VALIDÉ et NON OCCUPÉ
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query =  Q(date_validate__isnull=False) & (Q(contribuable__matricule__icontains=term) | Q(numero_allocation__icontains=term) | Q(reference_juridique__icontains=term) | Q(parcelle_publique__numero_parcelle__icontains=term))
		
		lst = AllocationEspacePublique.objects.filter(query)[:10]
		
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = 'Réf n°' + item.numero_allocation + ' - Parcelle n°' + item.parcelle_publique.numero_parcelle + ' - Par '+ item.contribuable.nom + ' (' + item.contribuable.matricule + ')'
			
			obj_json['contribuable_id'] = item.contribuable.id
			obj_json['contribuable_label'] = item.contribuable.matricule + ' - ' + item.contribuable.nom

			obj_json['adresse_id'] = item.parcelle_publique.adresse.id
			obj_json['adresse_label'] = item.parcelle_publique.adresse.nom + ' - (Zone de ' + item.parcelle_publique.adresse.zone.nom + ')'

			obj_json['numero_rueavenue_id'] = item.parcelle_publique.numero_rueavenue.id
			obj_json['numero_rueavenue_label'] = item.parcelle_publique.numero_rueavenue.nom

			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)