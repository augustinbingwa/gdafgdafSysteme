from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q

import json

from mod_finance.models import *

from mod_parametrage.enums import *

#----------------------------------------------------------------
def taxe_activite_autocomplete(request):
	"""
	Autocomplete d'une taxe sur activité
	type_activite : Standard et Marché
	taxe_filter : 
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(taxe_filter=TAXE_BASE_ACTIVITE) & (Q(code__icontains=term) | Q(libelle__icontains=term))
		
		lst = Taxe.objects.filter(query)[:10]

		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.code + ' - ' + item.libelle.capitalize() + ' (Paiement '+ item.periode_type.libelle + ', Tarif: ' + str(intcomma(item.tarif)) + ' BIF)'
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def note_imposition_taxe_changed(request):
	"""
	Renvoyer la période selon le type de période de la taxe seléctionnée
	"""
	taxe_id = request.POST["taxe"]

	obj_taxe = Taxe.objects.get(pk=taxe_id) 
	
	if obj_taxe:
		obj_periode = Periode.objects.filter(periode_type_id = obj_taxe.periode_type_id).values()

	data = dict()
	if obj_periode:
		data['success'] = True
		data['periode'] = list(obj_periode) #Liste des période selon le temps de la taxe
		data['taxe_montant'] = obj_taxe.tarif #tarif de la taxe
		data['nom_activite'] = obj_taxe.nom_activite #nom de l'activité
		data['taxe_libelle'] = obj_taxe.code + ' - ' + obj_taxe.libelle + ' (' + obj_taxe.periode_type.libelle + '). Tarif : ' + str(intcomma(obj_taxe.tarif)) + ' BIF' 
	else:
		data['success'] = False
		data['periode'] = ""
		data['taxe_montant'] = 0
		data['nom_activite'] = ""
		data['taxe_libelle'] = ""

	return JsonResponse(data)

#----------------------------------------------------------------
def avis_imposition_unused_autocomplete(request, taxe_filter=None):
	"""
	Autocomplete d'un avis d'impositon non encore utilisé (non attribué ou non attaché à aucune entité)
	si taxe_filter est spécifié alors taxe__taxe_filter = taxe_filter
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(entity=None) & Q(entity_id=None) & (Q(reference__icontains=term) | Q(nom__icontains=term)) 
		if taxe_filter is not None:
			query = query & Q(taxe__taxe_filter=taxe_filter)
		
		lst = AvisImposition.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.reference  + ' - ' + item.taxe.libelle + ' (' + item.nom + ')'
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def note_imposition_unused_autocomplete(request):
	"""
	Autocomplete d'une note d'impositon non encore utilisée (non attribuée ou non attachée à aucune entité)
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(entity=None) & Q(entity_id=None) & (Q(reference__icontains=term) | Q(taxe__libelle__icontains=term))
		lst = NoteImposition.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['value'] = item.id
			obj_json['label'] = item.reference  + ' - ' + item.taxe.libelle
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def numero_bordereau_autocomplete(request):
	"""
	Autocomplete d'une note d'impositon non encore utilisée (non attribuée ou non attachée à aucune entité)
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(ref_paiement__icontains = term)
		lst = NoteImpositionPaiement.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			res = ''
			sigle = ''
			note = NoteImposition.objects.filter(pk = item.note_imposition_id)
			for no in note:
				res = no.reference
			bank = Agence.objects.filter(pk = item.agence_id)
			for bak in bank:
				sigle = bak.sigle
				
			obj_json['id'] = item.id
			obj_json['value'] = str(item.montant_tranche)+","+str(res)+","+str(item.date_paiement)+","+str(sigle)
			obj_json['label'] = item.ref_paiement
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)