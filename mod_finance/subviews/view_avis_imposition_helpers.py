from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import json
from mod_finance.models import Taxe

#Utiliser pour les methode POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt #pour les methode POST qui necessite crsf_token
def avis_imposition_taxe_changed(request):
	"""
	Renvoyer la période selon le type de période de la taxe seléctionnée
	"""
	taxe_id = request.POST["taxe"]

	obj_taxe = Taxe.objects.get(pk=taxe_id) 
	
	data = dict()

	if obj_taxe:
		data['success'] = True
		data['taxe_montant'] = obj_taxe.tarif #tarif de la taxe
		data['nom_activite'] = obj_taxe.nom_activite #nom de l'activité
		data['libelle'] = "Paiement de " + obj_taxe.libelle #nom de l'activité
	else:
		data['success'] = False
		data['periode'] = ""
		data['taxe_montant'] = 0
		data['nom_activite'] = ""
		data['libelle'] = ""

	return JsonResponse(data)