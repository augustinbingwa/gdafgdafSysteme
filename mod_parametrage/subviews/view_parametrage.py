#from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt #Utiliser pour les methode POST
from django.db.models import Q

from mod_parametrage.models import Quartier, RueOuAvenue

import json

#------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def adresse_rue_avenue_by_zone(request):
	"""
	Chercher la liste des Rue ou Avenue d'un quartier
	"""
	adresseId = request.POST["adresse"]
	obj_quartier = Quartier.objects.get(pk=adresseId)
	
	if obj_quartier:
		obj_numero_rueavenue = RueOuAvenue.objects.filter(zone = obj_quartier.zone).values()	
	
	data = dict()
	if obj_quartier:
		data['success'] = True
		data['numero_rueavenue'] = list(obj_numero_rueavenue) #Liste des rue et numero_rueavenue selon le quartier
	else:
		data['success'] = False
		data['numero_rueavenue'] = ""

	return JsonResponse(data)

#------------------------------------------------------------
def adresse_zone_autocomplete(request):
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

#------------------------------------------------------------
def adresse_rue_avenue_autocomplete(request, quartier_id):
	"""
	Autocompete : Recherche d'une rue et/ou avenue d'une zone données
	Reamarque : Les Rues/Avenues dependes d'une zone
	Alors que dans l'adresse on a que le qartier, alors il faut remonter à partir de ce quartier pour chercher
	la zone et on aura toutes les avenues correspondantes
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')		

		quartier = Quartier.objects.get(id=quartier_id)
		zone_id = quartier.zone.id

		query = Q(zone__id=zone_id) & Q(nom__icontains=term)
		
		lst = RueOuAvenue.objects.filter(query)[:10]
		
		results = []
		for item in lst:
			obj_json = {}

			obj_json['id'] = item.id
			obj_json['label'] = item.nom
			obj_json['value'] = item.id
			if item.accessibilite:
				obj_json['accessibilite_id'] = item.accessibilite.id
			else:
				obj_json['accessibilite_id'] = None

			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	
	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def load_accessibilite_by_rue_avenue(request):
	"""
	Chrercher l'accebilité d'une rue ou avenue
	"""
	id_numero_rueavenue = request.POST["id_numero_rueavenue"]

	obj = RueOuAvenue.objects.get(id=id_numero_rueavenue)

	data = dict()
	if obj:
		if obj.accessibilite:
			data['success'] = True
			data['accessibilite_id'] = obj.accessibilite.id
		else:
			data['success'] = False
			data['accessibilite_id'] = None
	else:
		data['success'] = False
		data['accessibilite_id'] = None

	return JsonResponse(data)