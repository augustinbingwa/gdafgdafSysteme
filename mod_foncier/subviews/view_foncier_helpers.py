from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from django.db.models import Max

from mod_foncier.models import *
from mod_foncier.forms import *
from mod_foncier.templates import *

from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_operations import OperationsHelpers

import json
import datetime
from django.utils import timezone

#----------------------------------------------------------------
def foncier_non_occupe_valide_autocomplete(request):
	"""
	Autocomplete pour la recherche d'une espace ou parcelle publique valides (date_validate not Null)
	et in-occupée
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(occupee=False) & Q(date_validate__isnull=False) & (Q(numero_parcelle__icontains=term) | 
				Q(adresse_precise__icontains=term) | Q(adresse__nom__icontains=term) |
				Q(adresse__zone__nom__icontains=term) | Q(adresse__zone__commune__nom__icontains=term))

		lst = FoncierParcellePublique.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}
			obj_json['id'] = item.id
			obj_json['value'] = item.id

			adresse = item.numero_parcelle + ' - ' + item.adresse.zone.commune.nom + ' - ' +  item.adresse.zone.nom + ' - ' + item.adresse.nom
			
			if item.numero_rueavenue:
				adresse += ' - (Rue-Avenue: ' + item.numero_rueavenue.nom + ')'

			if item.adresse_precise:
				 adresse += ' (' + item.adresse_precise + ')'

			obj_json['label'] = adresse

			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'

	return HttpResponse(data, mimetype)

#----------------------------------------------------------------
def parcelle_autocomplete(request):
	"""
	Autocomplete pour les parcelle privée validée
	"""
	if request.is_ajax():
		term = request.GET.get('term', '')
		query = Q(date_validate__isnull = False) & Q(numero_parcelle__icontains=term)
		lst = FoncierParcelle.objects.filter(query)[:10]
		results = []
		for item in lst:
			obj_json = {}

			adresse = item.adresse.zone.commune.nom + ' - ' +  item.adresse.zone.nom + ' - ' + item.adresse.nom + ', ' +  item.numero_rueavenue.nom 
			if item.numero_police:
				adresse += ' n°' + item.numero_police

			obj_json['id'] = item.id
			obj_json['label'] = item.numero_parcelle + ', ' + adresse
			obj_json['value'] = item.id
			obj_json['contribuable'] = item.contribuable.matricule + ' - ' + item.contribuable.nom
			
			results.append(obj_json)
		data = json.dumps(results)
	else:
		data = 'fail'

	mimetype = 'application/json'
	
	return HttpResponse(data, mimetype)


#----------------------------------------------------------------
def parcelle_transfert_autocomplete(request):
  """
  Autocomplete pour la recherche d'un parcelle
  """
  if request.is_ajax():
    term = request.GET.get('term', '')
    query =  Q(matricule__icontains=term)
    lst = Contribuable.objects.filter(query)[:15]
    results = []
    for item in lst:
      print(item.id)
      obj_json = {}
      obj_json['id'] = item.id
      obj_json['value'] = item.nom+' '+item.matricule
      results.append(obj_json)
      
    data = json.dumps(results)
  else:
    data = 'fail'

  mimetype = 'application/json'

  return HttpResponse(data, mimetype)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def foncier_parcelle_create_expertise(request, pk):
	"""
	Cette fonctionnalité est utilisée seulement dans la parcelle
	"""
	#On prend le dernier expertise par rapport à cette parcelle
	#prendre l'année maximum
	#tel que le parcelle_id et annee sont uniques, il suffit de prendre l'année maximum
	objExpertise = FoncierExpertise() #on créer toujours un nouveau expertise quelque soit la situation (c'est un renouvelement)
	lstCara = FoncierCaracteristique()
	#1er cas , on fait refférence à la derniere année
	queryExpertise = Q(parcelle_id = pk) & Q(date_validate__isnull = False)
	lastExpertise = FoncierExpertise.objects.filter(queryExpertise).order_by('-annee').first()
	if lastExpertise:
		lstCara = FoncierCaracteristique.objects.all().filter(expertise_id=lastExpertise.id) #lastExpertise.id est toujours None peut être dû à la request.method == 'POST'
		objExpertise = lastExpertise
		objExpertise.id = None #(c'est un renouvelement)		
		objExpertise.annee = lastExpertise.annee + 1 # on ajout 1 à la derniere année
	else:
	#2em cas, on fait un nouveau expertise	
		objParcelle = get_object_or_404(FoncierParcelle, pk=pk)	
		objExpertise.parcelle = objParcelle
		objExpertise.annee = timezone.now().year # année en cours

	if request.method == 'POST':
		form = FoncierExpertiseForm(request.POST)
	else:
		form = FoncierExpertiseForm(instance=objExpertise)
	return save_foncier_expertise_form(request, form, FoncierExpertiseTemplate.createParcelle, 'create', lastExpertise, lstCara)

#----------------------------------------------------------------
def save_foncier_expertise_form(request, form, template_name, action, lastExpertise, lstCara):
	data = dict()
	if request.method == 'POST':		
		if form.is_valid():			
			if lastExpertise:
				#1)attachement dossier expertise
				obj = form.save(commit=False)
				user = User.objects.get(pk=request.user.id) # get current user 
				dateTimeNow = datetime.datetime.now(tz=timezone.utc)
				obj.user_create = user
				obj.dossier_expertise = lastExpertise.dossier_expertise #on enregistre le dernier fichier rattaché
				#todo si tout de suite validé			
				obj.save()
				#2)les caracteristiques
				#lastExpertise.id est toujours None peut être dû à la request.method == 'POST'
				#ainsi il faut le charger en parametre(lstCara)
				if lstCara and lstCara.count() > 0:
					for oldObjCara in lstCara:
						newObjCara = FoncierCaracteristique()
						newObjCara.expertise = obj
						newObjCara.impot_batie = oldObjCara.impot_batie
						newObjCara.superficie_batie = oldObjCara.superficie_batie
						newObjCara.save() 

			else:
				OperationsHelpers.execute_action(request, action, form) #c'est un nouveau enregistrement, nouveau parcelle et expertise, cas normal
			
			return redirect('foncier_parcelle_list')
		else:
			return ErrorsHelpers.show(request, form)
	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	return JsonResponse(data)

#----------------------------------------------------------------
@csrf_exempt #pour les methode POST qui necessite crsf_token
def load_impot_by_accessibilite(request):
	"""
	Chercher la liste des Rue ou Avenue d'un quartier
	"""
	id_parcelle = request.POST["id_parcelle"]
	obj_parcelle =FoncierParcelle.objects.get(pk=id_parcelle)
	
	from django.db.models import CharField, Value as V
	from django.db.models.functions import Concat

	if obj_parcelle:
		#obj_impots = FoncierTnbImpot.objects.annotate(screen_name=Concat('tnb_categorie__nom', V(' ') ,'impot'))
		#obj_impots = FoncierTnbImpot.objects.filter(accessibilite = obj_parcelle.accessibilite).values('id', 'tnb_categorie__nom')	
		obj_impots = FoncierTnbImpot.objects.filter(accessibilite = obj_parcelle.accessibilite).values('id', 'tnb_categorie__nom', 'impot')

	#self.tnb_categorie.nom  + " - " + self.accessibilite.nom + " - " + self.impot.__str__()

	data = dict()
	if obj_impots:
		data['success'] = True
		data['impots'] = list(obj_impots) #Liste des impots des surfaces non baties
	else:
		data['success'] = False
		data['impots'] = ''

	return JsonResponse(data)

#----------------------------------------------------------------
def get_montant_note(foncier_expertise):
	"""
	Renvoie le montant total de la note d'imposition de la parcelle
	TERRAIN NON BATI ET BATI(AVEC CONSTRUCTION)
	@obj : 
	"""
	montant_non_bati = 0
	montant_construction = 0
	
	obj = foncier_expertise
	if obj:
		# Traitement du terrain non bâti
		montant_non_bati = round(obj.superficie_non_batie * obj.impot_non_batie.impot)

		# Traitement des contructions (terrain bâti)
		lst_car = FoncierCaracteristique.objects.filter(expertise = obj)
		for car in lst_car:
			montant_construction += round(car.superficie_batie * car.impot_batie.impot)

	return (montant_non_bati + montant_construction), montant_non_bati, montant_construction 
