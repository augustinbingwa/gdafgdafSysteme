from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from mod_transport.models import *

import json

#----------------------------------------------------------------
def vehicule_autocomplete(request):
	"""
	Autocomplete pour la recherche d'un véhicule
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query =  Q(plaque__icontains=term)
		lst = Vehicule.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.plaque + ' ' +  item.modele.nom
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def vehicule_has_plaque_autocomplete(request):
	"""
	Autocomplete pour la recherche d'un véhicule qui possède de carte rose
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query =  Q(sous_categorie__has_plaque=True) & (Q(plaque__icontains=term) | Q(modele__nom__icontains=term))
		lst = Vehicule.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.plaque + ' (' + item.modele.nom + ') - ' + item.sous_categorie.nom
			obj_json['contribuable_id'] = item.contribuable.id
			obj_json['contribuable'] = item.contribuable.matricule + ' - ' + item.contribuable.nom

			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def vehicule_valide_autocomplete(request):
	"""
	Autocomplete pour la recherche d'un véhicule qui possède une plaque d'immatriculation (carte rose ) et
	qui peut eercer des ativités de tranport rémunéré ie ayant des informations valides (date_validate not Null)
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query =  (Q(date_validate__isnull=False) & Q(plaque__icontains=term) & Q(remunere=True)) | (Q(modele__nom__icontains=term) | Q(chassis__icontains=term))
		lst = Vehicule.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			
			status = ''
			if item.actif:
				status = ' - (EN ACTIVITE)'

			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.plaque + ' - (' + item.modele.nom + ') - ' + item.sous_categorie.nom + status
			obj_json['contribuable_id'] = item.contribuable.id
			obj_json['contribuable'] = item.contribuable.matricule + ' - ' + item.contribuable.nom
			obj_json['chassis'] = item.chassis

			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def vehicule_has_plaque_valide_autocomplete(request):
	"""
	Autocomplete pour la recherche d'un véhicule qui possède une plaque d'immatriculation (carte rose ) et
	qui peut eercer des ativités de tranport rémunéré ie ayant des informations valides (date_validate not Null)
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query =  Q(sous_categorie__has_plaque=True) & Q(date_validate__isnull=False) & (Q(plaque__icontains=term) | Q(modele__nom__icontains=term) | Q(chassis__icontains=term)) 
		lst = Vehicule.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			
			status = ''
			if item.actif:
				status = ' - (EN ACTIVITE)'

			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.plaque + ' - (' + item.modele.nom + ') - ' + item.sous_categorie.nom + status
			obj_json['contribuable_id'] = item.contribuable.id
			obj_json['contribuable'] = item.contribuable.matricule + ' - ' + item.contribuable.nom
			obj_json['chassis'] = item.chassis

			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def vehicule_no_plaque_valide_autocomplete(request):
	"""
	Autocomplete pour la recherche d'un véhicule qui n'a pas de plaque/ie sans carte rose (ex : vélo/vélomoteur)
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query =  Q(sous_categorie__has_plaque = False) & Q(date_validate__isnull=False) & (Q(plaque__icontains=term) | Q(chassis__icontains=term))
		lst = Vehicule.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			
			status = ''
			if item.actif:
				status = ' - (EN ACTIVITE / ' + item.contribuable.matricule + ' - ' + item.contribuable.nom + ')'
			else:
				status = ' - (INACTIF / ' + item.contribuable.matricule + ' - ' + item.contribuable.nom + ')'

			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.plaque + ' - (' +  item.modele.nom + ') - ' + item.sous_categorie.nom + status
			
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def vehicule_activite_municipale_autocomplete_old(request): 
	"""
	Autocomplete pour la recherche d'une activité rémunéré d'un véhicule 
	Condition : Seules les activités rémunurées, validées et non cloturée seront recherchées
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = (Q(date_validate__isnull=False) & Q(date_fin__isnull=True) & Q(vehicule__actif=True)) & (Q(numero_activite__icontains=term) | Q(vehicule__plaque__icontains=term)) | Q(vehicule__chassis__icontains=term) 
		lst = VehiculeActivite.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}

			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.numero_activite
			obj_json['vehicule'] = item.vehicule.plaque + ' - ' + item.vehicule.modele.nom + ' - ' + item.vehicule.sous_categorie.nom
			obj_json['contribuable'] = item.contribuable.matricule + ' - ' + item.contribuable.nom
			obj_json['taxe_activite'] = item.vehicule.sous_categorie.taxe_activite.id
			obj_json['taxe_stationnement'] = item.vehicule.sous_categorie.taxe_stationnement.id
			
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype) 

#----------------------------------------------------------------
def vehicule_activite_autocomplete(request): 
	"""
	Autocomplete pour la recherche d'une activité rémunéré d'un véhicule 
	Condition : Seules les activités rémunurées, validées et non cloturée seront recherchées
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = (Q(date_validate__isnull=False) & Q(date_fin__isnull=True)) & (Q(numero_activite__icontains=term) | Q(vehicule__plaque__icontains=term) | Q(vehicule__chassis__icontains=term))
		lst = VehiculeActivite.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}

			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.numero_activite + ' - ' + item.vehicule.plaque + ' (' + item.vehicule.modele.nom + ') - ' + item.vehicule.sous_categorie.nom + ' - ' + item.vehicule.contribuable.nom
			
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype) 

#----------------------------------------------------------------
def vehicule_proprietaire_autocomplete(request):
	"""
	Autocomplete pour la recherche d'une carte de propriétaire
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(numero_carte__icontains=term) | Q(vehicule__plaque__icontains=term) | Q(vehicule__chassis__icontains=term) 
		lst = VehiculeProprietaire.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}

			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.numero_carte + ' - ' + item.vehicule.plaque + ' (' + item.vehicule.modele.nom + ') - ' + item.vehicule.sous_categorie.nom + ' - ' + item.vehicule.contribuable.nom
			
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype) 

#----------------------------------------------------------------
def vehicule_modele_autocomplete(request):
	"""
	Autocomplete pour la recherche d'un modèle de véhicule 
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(nom__icontains=term)
		lst = VehiculeModele.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.nom
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def vehicule_get_sous_categorie(request):
	"""
	Recherche d'une categorie de véhicule à partir d'un sous catégorie
	Utilisée pour la gestion du COMPTE PROPRE 
	Référence (transport.js)
	"""
	data = dict()
	try:
		ID = request.POST["id"]
		
		obj = get_object_or_404(VehiculeSousCategorie, pk=ID)	
		
		data['has_compte_propre'] = obj.has_compte_propre
	except:
		pass

	return JsonResponse(data)