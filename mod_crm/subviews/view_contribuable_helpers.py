from django.http import JsonResponse, HttpResponse
from django.db.models import Q

from mod_parametrage.models import Quartier
from mod_crm.models import *

import json

#------------------------------------------------------------
def contribuable_auto_complete(request):
	"""
	Autocomplte : Recherche d'un contribuable valide
	date_validate__isnull = False
	Rechêrche par : matricule ou nom
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(date_validate__isnull = False) & (Q(matricule__icontains=term) | Q(nom__icontains=term))
		lst = Contribuable.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['label'] = item.matricule + ' - ' + item.nom
			obj_json['value'] = item.id
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'
	
	return HttpResponse(data, mimetype)

#------------------------------------------------------------
def adresse_auto_complete(request):
	"""
	Autocomplete : Recherche d'une adresse exacte
	Recherche par nom de zone ou nom quartier
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')		
		query = Q(nom__icontains=term) | Q(zone__nom__icontains=term)
		lst = Quartier.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['label'] = item.nom + ' - (Zone de ' + item.zone.nom + ')'
			obj_json['value'] = item.id
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	
	mimetype = 'application/json'

	return HttpResponse(data, mimetype)