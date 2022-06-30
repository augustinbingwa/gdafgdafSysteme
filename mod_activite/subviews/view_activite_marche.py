from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.db.models import Q

from mod_activite.models import Marche
from mod_activite.forms import MarcheForm, MarchePrintForm
from mod_activite.templates import *

from mod_helpers.models import Chrono
from mod_helpers.hlp_paginator import PaginatorHelpers
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_notification import NotificationHelpers
from mod_helpers.hlp_report import ReportHelpers
from mod_helpers.hlp_session import SessionHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import NoteArchive
from mod_helpers.hlp_accroissement import AccroissementHelpers
from mod_helpers.hlp_validators import *

from mod_crm.models import *

from mod_finance.models import *

from mod_parametrage.enums import *

from django.utils import timezone
import datetime

#----------------------------------------------------------------
#------------------ CRUD Activité Standard  ---------------------
#----------------------------------------------------------------
def get_list_by_criteria(request):
	"""
	Renvoie la liste avec criteria
	"""
	total = Marche.objects.count

	# Initialier les variables locales, sesions via variables POST
	am_numero_activite = SessionHelpers.init_variables(request, 'am_numero_activite')
	am_nom = SessionHelpers.init_variables(request, 'am_nom')
	am_marche = SessionHelpers.init_variables(request, 'am_marche')
	am_place = SessionHelpers.init_variables(request, 'am_place')
	am_contribuable = SessionHelpers.init_variables(request, 'am_contribuable')
	am_contribuable_nom = SessionHelpers.init_variables(request, 'am_contribuable_nom')
	am_user_create = SessionHelpers.init_variables(request, 'am_user_create')
	am_status = SessionHelpers.init_variables(request, 'am_status')

	# Initialier les variables locales, sesions via variables POST pour la période
	du = SessionHelpers.init_variables(request, 'am_du')
	au = SessionHelpers.init_variables(request, 'am_au')

	# Définir les parametres de recherche
	query = SessionHelpers.get_query(None, Q(numero_activite__icontains=am_numero_activite))
	query = SessionHelpers.get_query(query, Q(taxe__libelle__icontains=am_nom))
	query = SessionHelpers.get_query(query, Q(allocation_place_marche__droit_place_marche__nom_marche__nom__icontains=am_marche))
	query = SessionHelpers.get_query(query, Q(allocation_place_marche__droit_place_marche__numero_place__icontains=am_place))
	query = SessionHelpers.get_query(query, Q(allocation_place_marche__contribuable__matricule__icontains=am_contribuable))
	query = SessionHelpers.get_query(query, Q(allocation_place_marche__contribuable__nom__icontains=am_contribuable_nom))
	query = SessionHelpers.get_query(query, Q(user_create__username__icontains=am_user_create))

	if am_status=='1': #Valide
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=False))
	elif am_status=='2': #En attente
		query = SessionHelpers.get_query(query, Q(date_validate__isnull=True))
	
	# Charger la liste
	if query:
		lst = Marche.objects.filter(query,actif=True)
	else:
		lst = Marche.objects.filter(actif=True)

	# Si période valide
	if is_date_fr_valid(du) and is_date_fr_valid(au):
		du = date_picker_to_date_string(du)
		au = date_picker_to_date_string(au, True)
	
		#if is_date_valid(du) and is_date_valid(au):
		lst = lst.filter(date_validate__range=[du, au]).order_by('-date_validate')	

	# Renvoyer le résultat de la requete filtrée avec paginator
	return PaginatorHelpers.get_list_paginator_entity_filter(request, lst), total

#------------------------------------------------------------
def get_context(request):
	"""
	Renvoie les info du context
	"""
	# Lire les notifications
	lst_notification = NotificationHelpers.get_list(request)

	# Charger la liste
	lst, total = get_list_by_criteria(request)

	# Sauvegader le context
	context = {
		'total': total,
		'lst': lst,

		'am_numero_activite': request.session['am_numero_activite'],
		'am_nom': request.session['am_nom'],
		'am_marche': request.session['am_marche'],
		'am_place': request.session['am_place'],
		'am_contribuable': request.session['am_contribuable'],
		'am_contribuable_nom': request.session['am_contribuable_nom'],
		'am_user_create': request.session['am_user_create'],
		'am_status': request.session['am_status'],

		'am_du': request.session['am_du'],
		'am_au': request.session['am_au'],

		'lst_notification':lst_notification,
		'user' : User.objects.get(pk=request.user.id),
	}

	return context

#------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def activite_marche_list(request):
	"""
	Liste des activités dans le marché
	"""
	# Enregistrer l'url de la liste en cours (important pour les AJAX: Validation, Update etc )
	request.session['url_list'] = request.get_full_path()

	return render(request, MarcheTemplate.index, context=get_context(request))

#----------------------------------------------------------------
@login_required(login_url="login/")
def activite_marche_create(request):
	"""
	Création d'une activité dans le marché
	"""
	if request.method == 'POST':
		form = MarcheForm(request.POST)
	else:
		form = MarcheForm()
	
	return save_activite_marche_form(request, form, MarcheTemplate.create, 'create')

#----------------------------------------------------------------
@login_required(login_url="login/")
def activite_marche_update(request, pk):
	"""
	Modification d'une activité dans le marché
	"""
	obj = get_object_or_404(Marche, pk=pk)
	if request.method == 'POST':
		form = MarcheForm(request.POST, instance=obj)
	else:
		form = MarcheForm(instance=obj)

	return save_activite_marche_form(request, form, MarcheTemplate.update, 'update')

#----------------------------------------------------------------
@login_required(login_url="login/")
def activite_marche_delete(request, pk):
	"""
	Suppression d'une activité dans le marché
	"""
	obj = get_object_or_404(Marche, pk=pk)
	data = dict()
	if request.method == 'POST':
		obj.delete()
		
		data['form_is_valid'] = True		    
		data['html_content_list'] = render_to_string(MarcheTemplate.list, context=get_context(request))
		data['url_redirect'] = request.session['url_list']
	else:
		context = {'obj': obj}
		data['html_form'] = render_to_string(MarcheTemplate.delete, context, request=request)

	return JsonResponse(data)

#----------------------------------------------------------------
def save_activite_marche_form(request, form, template_name, action):
	"""
    Sauvegarde des informations d'une activité dans le marché
	"""
	data = dict()
	if request.method == 'POST':
		if form.is_valid():			
			msg = OperationsHelpers.execute_action(request, action, form, CHRONO_ACTIVITE_MARCHE, 'numero_activite')
			if msg:
				return ErrorsHelpers.show_message(request, msg)

			data['form_is_valid'] = True
			data['html_content_list'] = render_to_string(MarcheTemplate.list, context=get_context(request))
			data['url_redirect'] = request.session['url_list']
		else:
			return ErrorsHelpers.show(request, form)

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def activite_marche_validate(request):
	"""
	Valider les informations de l'activité cas dans les marchés
	"""
	#Récuperer l'identifiant de l'activité
	ID = request.POST["id"]
	obj = get_object_or_404(Marche, pk=ID)
	
	try:
		with transaction.atomic():
			if obj.note and obj.date_note:
				arc = NoteArchive()
				arc.entity = EntityHelpers.get_entity_class_name(obj) # Npm de l'entité classe
				arc.entity_id = obj.id
				arc.note = obj.note
				arc.user_note = obj.user_note
				arc.date_note = obj.date_note
				arc.reponse_note = obj.reponse_note
				arc.demande_annulation_validation = obj.demande_annulation_validation
				arc.date_cancel = obj.date_cancel
				arc.user_cancel = obj.user_cancel
				arc.user_create = User.objects.get(pk=request.user.id)
				arc.save()

				# 2 Effacer la trace de la notification
				obj.note = None
				obj.user_note = None
				obj.date_note = None
				obj.reponse_note = None
				obj.demande_annulation_validation = False
				obj.date_cancel = None
				obj.user_cancel = None

			# Sauvegarder l'objet allocation
			OperationsHelpers.execute_action_validate(request, obj)
	except:
		return ErrorsHelpers.show_message(request, 'Erreur de validation')

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(MarcheTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt #pour les methode POST qui necessite crsf_token
def activite_marche_ecriture(request):
	"""
	Valider les informations de l'activité cas dans les marchés
	TRANSACTION : AI, NI
	"""
	#Récuperer l'identifiant de l'activité
	ID = request.POST["id"]
	obj = get_object_or_404(Marche, pk=ID)

	# get current user 
	user = User.objects.get(pk=request.user.id) 

	# get current datetime 
	dateTimeNow = datetime.datetime.now()

	try:
		with transaction.atomic():
			#---------------------------------------------------------------------
			# 1 - Générer l'écriture de l'objet principal
			OperationsHelpers.execute_action_ecriture(request, obj)

			if obj.ai_cout_carte.tarif>0:
				#---------------------------------------------------------------------
				# 2 - Créer et Valider l'avis d'imposition pour le coût de la carte d'activité professionnelle
				# Générer le nouveau numéro chrono
				new_chrono = ChronoHelpers.get_new_num(CHRONO_AVIS_IMPOSITION)
				obj_chrono = Chrono.objects.get(prefixe = CHRONO_AVIS_IMPOSITION)
				obj_chrono.last_chrono = new_chrono 
				obj_chrono.save()

				#---------------------------------------------------------------------
				# 3 - Créer l'objet AvisImposition SI TAXE POSITIF
				ai = AvisImposition()

				# Référence de l'avis d'imposition (chronologique)
				ai.reference = new_chrono

				# Contribuable
				ai.contribuable = obj.allocation_place_marche.contribuable

				# Cout de la carte, Objet taxe (Type : Avis d'imposition)
				ai.taxe = obj.taxe

				# coût de la carte, ai.taxe_montant : Tarif de la taxe (Type : Avis d'imposition) (Formule : tarif * nombre_copie), nombre copie = 1
				ai.montant_total = ai.taxe_montant = obj.ai_cout_carte.tarif

				# Entity Modèle : 'BaseActivite'
				ai.entity = ENTITY_ACTIVITE_MARCHE

				# Identifiant de l'entity : 'BaseActivite.id'
				ai.entity_id = obj.id

				# Libellé
				ai.libelle = 'Carte professionnelle n°' + obj.numero_activite + ' dans le marché de ' + obj.allocation_place_marche.droit_place_marche.nom_marche.nom + ', place n°' + obj.allocation_place_marche.droit_place_marche.numero_place

				# Traçabilité (date_create est créée depuis le model)
				# Traçabilité (date_create est créée depuis le model)
				ai.date_update = dateTimeNow

				ai.user_create = user
				ai.user_update = user

				# Sauvegarder l'avis d'imposition (coût de la carte d'activité)
				ai.save()

			if obj.taxe.tarif>0:
				#---------------------------------------------------------------------
				# 4 - Créer et Valider la note d'imposition (taxe sur l'activité dans le marché) si TAXE POSITIF
				# Générer le nouveau numéro chrono
				new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
				obj_chrono = Chrono.objects.get(prefixe = CHRONO_NOTE_IMPOSITION)
				obj_chrono.last_chrono = new_chrono 
				obj_chrono.save();

				# 5 - Créer l'objet Note d'imposition
				ni = NoteImposition()

				# Référence de la note d'imposition (chronologique)
				ni.reference = new_chrono

				# Contribuable qui se trouve sur l'allocation de la place dans le marché (contrat préalable) IMPORTANT !!!
				ni.contribuable = obj.allocation_place_marche.contribuable

				# Entity Modèle : 'BaseActivite'
				ni.entity = ENTITY_ACTIVITE_MARCHE

				# Identifiant de l'entity : 'Marche'
				ni.entity_id = obj.id

				# Période de paiement
				ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)

				# Année de paiement (Très important pour la gestion des périodes)
				ni.annee = dateTimeNow.year

				 # Taxe sur activité, Objet taxe (Type : Note d'imposition)
				ni.taxe = obj.taxe

				# ACCROISEMENT
				taux_accroisement = AccroissementHelpers.has_accroissement(dateTimeNow.year, dateTimeNow)
				accroissement = 0
				if taux_accroisement>0:
					accroissement = (obj.taxe.tarif * taux_accroisement) / 100

				MONTANT_DU = obj.taxe.tarif + accroissement

				# Solde de depart
				if obj.solde_depart>0:
					MONTANT_DU += obj.solde_depart

				# Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
				ni.taxe_montant = MONTANT_DU
				
				# Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
				ni.taxe_montant = obj.taxe.tarif

				# Traçabilité (date_create est créée depuis le model)
				ni.date_update = dateTimeNow
				ni.date_validate = dateTimeNow

				ni.user_create = user
				ni.user_update = user
				ni.user_validate = user

				# Sauvegarder la note d'imposition (taxe sur l'allocation)
				ni.save()
			else:
				return ErrorsHelpers.show_message(request, "Erreur, le montant de la note d'imposition doit être positif")
	except IntegrityError as e:
		return ErrorsHelpers.show_message(request, "Erreur de génération de l'écriture " + str(e))

	data = dict()
	data['url_redirect'] = request.session['url_list']
	data['html_content_list'] = render_to_string(MarcheTemplate.list, context=get_context(request))
	
	return JsonResponse(data)

#----------------------------------------------------------------
#---------- PRINT : Impression de la carte de propriété ---------
#----------------------------------------------------------------
@login_required(login_url="login/")
def activite_marche_print(request, pk):
    """
    Mise à jour du numero_carte_physique du modèle Marche(BaseActivite) avant impression
    """
    obj = get_object_or_404(Marche, pk=pk)
    if request.method == 'POST':
        form = MarchePrintForm(request.POST, instance=obj)
    else:
        form = MarchePrintForm(instance=obj) 

    return save_activite_marche_form(request, form, MarcheTemplate.print, 'update') # 'update' : Mise à jour !!! IMPORTANT !!!

#----------------------------------------------------------------
@login_required(login_url="login/")
def activite_marche_print_authorization(request, pk):
    """
    Demander d'autorisation d'impression de la carte (car le nombre MAX_NUMBER est atteint)
    """
    obj = get_object_or_404(Marche, pk=pk)
    if request.method == 'POST':
        form = MarchePrintAuthorizationForm(request.POST, instance=obj)
    else:
        form = MarchePrintAuthorizationForm(instance=obj) 

    return save_activite_marche_form(request, form, MarcheTemplate.print_authorization, 'update') # 'update' : Mise à jour !!! IMPORTANT !!!

#----------------------------------------------------------------
@login_required(login_url="login/")
@csrf_exempt
def activite_marche_print_confirm(request, pk):
    """
    Confirmer l'impression de la carte d'activite professionnelle
    """
    data = dict()
    success = 'true'
    message = ''

    try:
        obj = get_object_or_404(Marche, pk=pk)
        obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
        if obj and obj_gv and obj.nombre_impression >= int(obj_gv.valeur):
            success = 'false'
            message = "Ereur d'impression, vous n'avez que 3 essais d'impression. <br> Veuillez demander l'autorisation d'impression auprès de votre supérieur."
    
    except IntegrityError as e: 
        success = 'false'
        message = "Erreur inattendu, " + str(e)
        
    data['success'] = success
    data['html_form'] = message

    return JsonResponse(data)

#----------------------------------------------------------------
@login_required(login_url="login/")
def activite_marche_print_pdf(request, pk):
    """
    Impression de la carte d'activité professionnelle de transport rémunéré
    """
    # Nom du fichier template html
    filename = 'carte_activite'
    
    obj = Marche.objects.get(pk=pk)
    
    obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
    if obj.nombre_impression >= int(obj_gv.valeur):
        # Empecher le download du PDF
        return activite_marche_print_confirm(request, pk)
    else:
        if obj and obj.date_validate: # + Payement effectué
            # Action save print
            obj.nombre_impression += 1 

            # Action save print
            OperationsHelpers.execute_action_print(request, obj)    

            try:
                # personne physique:
                obj_pp = PersonnePhysique.objects.get(pk=obj.AllocationPlaceMarche.contribuable.id)
                if obj_pp:
                    # photo d'identité
                    photo_url = 'file://' + settings.MEDIA_ROOT + '/' + obj_pp.photo_file.name  
            except:
                photo_url = '-'

            # Definir le context
            context = {'obj': obj, 'qr_options': ReportHelpers.get_qr_options(), 'qr_data':get_qr_data(obj), 'photo_url':photo_url}

            # Generate PDF
            return ReportHelpers.Render(request, filename, context) 

        return ErrorsHelpers.show_message(request, "Erreur d'impression de la carte d'activité de transport")

#----------------------------------------------------------------
def get_qr_data(obj):
    """
    Composition des données du qr code
    """
    if isinstance(obj, Marche):
        return 'ID-card: {} \nMatricule: {} \nNom: {} \nMarque: {} \nPlaque: {} \nChassis: {} \nCatégorie: {} \nValidé: {}'.format(
            obj.numero_activite, 
            obj.contribuable.matricule,
            obj.contribuable.nom,
            obj.allocation_place_marche.droit_place_marche.nom_marche.nom,
            obj.allocation_place_marche.droit_place_marche.numero_place,
            obj.user_print,
            obj.date_validate.strftime('%Y-%m-%d %H:%M:%S'))

    return 'GDAF'
