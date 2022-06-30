from django import template
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q, F, Sum #taxe_montant__gte=F('montant_total')
from django.contrib.auth.models import User

from mod_finance.models import NoteImposition, AvisImposition, NoteImpositionPaiement
from mod_foncier.models import *
# from mod_foncier.subviews.view_foncier_helpers import *
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers

from mod_parametrage.enums import *

register = template.Library()

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

#------------------------------------------------------------
@register.filter()
def filter_status_validate(obj, obj_note=None):
	"""
	Filter : pour le status des parcelles privées, ...
	"""
	objToRet= "<span class='badge badge-warning'>Brouillon</span>"	

	if isinstance(obj, FoncierExpertise):
		if obj_note and obj_note.is_payed:
			paiement = NoteImpositionPaiement.objects.filter(note_imposition=obj_note).first()
			if paiement:
				if obj.date_ecriture:
					objToRet = "<span class='badge badge-dark'>Générée: " + obj.date_ecriture.strftime("%d/%m/%Y") + " </span><br><span class='badge badge-dark'>Payée " + paiement.date_validate.strftime("%d/%m/%Y") + "</span>"
				else:
					objToRet = "<span class='badge badge-dark'>Payée " + paiement.date_validate.strftime("%d/%m/%Y") + "</span>"
			else:
				# ERROR = QUELQU'UN A MODIFIÉ À LA MAIN LE MONTANT DE LA BASE !!!
				objToRet = "<span class='badge badge-warning'>ERREUR !!!</span>"
		elif obj.date_ecriture:
			objToRet = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span><br><span class='badge badge-info'>Générée: " + obj.date_ecriture.strftime("%d/%m/%Y") + "</span>"
		elif obj.date_validate:
			if si_exonere(obj):
				objToRet = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span><br><span class='badge badge-dark'>Éxonéré</span>"
			else:
				objToRet = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span><br><span class='badge badge-danger'>Non générée</span>"
	else:
		if obj.date_validate:
			objToRet = "<span class='badge badge-success'>Validée: " + obj.date_validate.strftime("%d/%m/%Y") + "</span>"
		else:
			if isinstance(obj, FoncierParcelle):
				if obj.fichier_declaration:
					objToRet = "<span class='badge badge-warning'>En attente</span>"
			else:
				objToRet = "<span class='badge badge-warning'>En attente</span>"

	return mark_safe(objToRet)

#------------------------------------------------------------
@register.filter()
def numero_police_is_none(value):
	"""
	Filter : prendre la référence de l'activité
	"""
	if value is None:
		return ''
	
	return ', N°' + value

#------------------------------------------------------------
@register.filter()
def foncier_bool(value):
	"""
	:param value: boolean
	:return: Oui/Non
	"""
	res = "Non"
	if value:
		res = "Oui"

	return res

#------------------------------------------------------------
@register.filter()
def foncier_bool_safe(value):
	"""
	:param value: boolean
	:return: Oui/Non
	"""
	res = "<span class='badge badge-warning'>Non</span>"
	if value:
		res = "<span class='badge badge-primary'>Oui</span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def foncier_load_caracteristique(value):
	"""
	:param value: id expertise
	:return: liste caracteristique
	"""
	lstCara = FoncierCaracteristique.objects.all().filter(expertise_id=value)

	return lstCara

#------------------------------------------------------------
@register.filter()
def foncier_expertise_existe(value):
	"""
	:param value: id expertise
	:return: liste caracteristique
	"""
	objParcelle = FoncierExpertise.objects.all().filter(parcelle_id=value)
	if objParcelle:
		return True

	return False

#------------------------------------------------------------
@register.filter()
def get_info_parcelle(obj_parcelle):
	"""
	Renvoyer l'adresse complete 
	Numero parcelle + COMMUNE - ZONE - QUARTIER, rueavenue, police
	"""
	res = ''
	if isinstance(obj_parcelle, FoncierParcelle):
		res = obj_parcelle.numero_parcelle + ' - ' + str(obj_parcelle.adresse)
		if obj_parcelle.numero_rueavenue:
			 res += ', ' +  obj_parcelle.numero_rueavenue.nom 
		if obj_parcelle.numero_police:
			res += ' n°' + obj_parcelle.numero_police

	return res

#------------------------------------------------------------
@register.filter()
def get_impot_non_batie(obj_expertise):
	"""
	Renvoyer l'info de l'impot non bati
	"""
	res = ''
	if obj_expertise and isinstance(obj_expertise, FoncierExpertise):
		res = obj_expertise.impot_non_batie.tnb_categorie.nom  + " - " + obj_expertise.impot_non_batie.accessibilite.nom + " - <strong>" + obj_expertise.impot_non_batie.impot.__str__().replace('.',',') + " Bif</strong>"
	
	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_montant_tnb(obj_expertise):
	"""
	Renvoyer le total de non bati
	"""
	res = 0
	if isinstance(obj_expertise, FoncierExpertise):
		res = round(obj_expertise.superficie_non_batie * obj_expertise.impot_non_batie.impot)

	return res

#------------------------------------------------------------
@register.filter()
def get_impot_batie(obj_caracteristique):
	"""
	Renvoyer l'info de l'impot bati
	"""
	res = ''
	if isinstance(obj_caracteristique, FoncierCaracteristique):
		res = "<strong>" + obj_caracteristique.impot_batie.impot.__str__().replace('.',',') + " Bif</strong> - " + obj_caracteristique.impot_batie.categorie.nom  + ' - ' + obj_caracteristique.impot_batie.type_confort.nom + " - " + obj_caracteristique.impot_batie.accessibilite.nom
	
	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_total_montant_caracteristique(obj_expertise):
	"""
	Renvoie le montant total des caractérisques d'une construction (ou expertise)
	"""
	total = 0
	lst = FoncierCaracteristique.objects.filter(expertise = obj_expertise)
	for car in lst:
		total += (car.superficie_batie * car.impot_batie.impot)

	return total

#------------------------------------------------------------
def get_montant_minimale_declaration():
	"""
	Renvoie le montant minimale de la déclaration (VariableGobaes)
	"""
	return  int(GlobalVariablesHelpers.get_global_variables("FONCIER", "MONTANT_MINIMALE_NOTE").valeur)

#------------------------------------------------------------
@register.filter()
def get_libelle_minimale_declaration(value):
	"""
	Renvoie le montant minimale de la déclaration (VariableGobaes)
	"""
	return GlobalVariablesHelpers.get_global_variables("FONCIER", "MONTANT_MINIMALE_NOTE").description

#------------------------------------------------------------
@register.filter()
def get_last_imposition(obj):
	"""
	obj : Parcelle Privée
	"""
	res = ''
	if obj and isinstance(obj, FoncierParcelle):
		exp = FoncierExpertise.objects.filter(parcelle__id=obj.id).order_by('-annee')
		if exp:
			res = "&nbsp;<span class='badge badge-primary'>&nbsp;Imposée le " + str(exp[0].annee) + "&nbsp;</span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_aperçu_montant_total_note_imposition(obj):
	"""
	Renvoie le montant total de la note à payer (mode aperçu)
	"""
	total = 0
	if isinstance(obj, FoncierExpertise):
		try:
			# IMPORTANT en mode création
			total = round(obj.impot_non_batie.impot * obj.superficie_non_batie)
			total += get_total_montant_caracteristique(obj)
			total += get_montant_accroissement(obj)
		except:
			pass

	return total

#------------------------------------------------------------
@register.filter()
def si_exonere(obj):
	"""
	Renvoie True si la déclaration est exoneré (total < 1000 voir variable globale)
	"""
	if isinstance(obj, FoncierExpertise):
		return get_aperçu_montant_total_note_imposition(obj) < get_montant_minimale_declaration()

	return False

#------------------------------------------------------------
@register.filter()
def show_note(note):
	if note:
		note = "<i title='" + note + "' class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>"
	else:
		note = ''
	
	return mark_safe(note)

#------------------------------------------------------------
@register.filter()
def show_me(obj, current_user):
	"""
	Filtere : Colorie l'icone commentaire (note)
	"""
	note = ''
	if obj.note:
		if obj.demande_annulation_validation:
			note = "<i class='fa fa-commenting' aria-hidden='true' style='color:red;'></i>&nbsp;" # Danger (Demande dd'annulation de validatio d'un objet)
		else:
			note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#FFAD07'></i>&nbsp;" # Warning
	else:
		note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#808080'></i>&nbsp;" # info

	res = "<span class='text-dark'>" + note + str(obj.user_create) + "</span>"
	if obj.user_create == current_user:
		res= "<span class='text-primary'>" + note + str(obj.user_create) + "</span>"
	
	res += "<br><span class='text-muted'><small>" + obj.date_create.strftime("%d/%m/%Y %H:%M") + "</small></span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def is_ni_payed(obj):
	"""
	Filter : SI la note d'imposition est déjà payé 
	obj : l'objet qui possède la propriété (nombre_impression)
	"""
	entity = 0
	
	if isinstance(obj, FoncierParcelle):
		entity = ENTITY_FONCIER_PARCELLE
		if entity > 0:
			ni = NoteImposition.objects.get(entity=entity, entity_id=obj.id)
			if ni:
				return ni.is_payed

	return False

#------------------------------------------------------------
@register.filter()
def nombre_enreg_by_user(lst, user):
	"""
	Renvoie le nombre d'enregistrements par utilisateur
	"""
	nombre = 0
	nombre_valid = 0

	obj = None
	if lst:
		obj = lst[0]
	
	if obj:
		if isinstance(obj, FoncierParcelle):
			nombre = FoncierParcelle.objects.filter(user_create=user).count()
			nombre_valid = FoncierParcelle.objects.filter(user_create=user, date_validate__isnull=False).count()

		if isinstance(obj, FoncierParcellePublique):
			nombre = FoncierParcellePublique.objects.filter(user_create=user).count()
			nombre_valid = FoncierParcellePublique.objects.filter(user_create=user, date_validate__isnull=False).count()

		if isinstance(obj, FoncierExpertise):
			nombre = FoncierExpertise.objects.filter(user_create=user).count()
			nombre_valid = FoncierExpertise.objects.filter(user_create=user, date_validate__isnull=False).count()
		
	if nombre>0:
		if nombre_valid==1:
			res_valid = " dont <strong style='color:#000;'>" + str(nombre_valid) + '</strong> a été validé'
		elif nombre_valid>1:
			res_valid = " dont <strong style='color:#000;'>" + str(nombre_valid) + '</strong> ont été validés'
		else:
			res_valid = ''
		res = "<label class='fa fa-check text-muted'>&nbsp; <em style='color:#4588B3;'>"+ str(user).capitalize() +"</em>, vous avez créé <strong style='color:#000;'>" + str(nombre) + "</strong> éléments" + res_valid + "</label>"
	else:
		res = ''

	return mark_safe(res)

#------------------------------------------------------------
#-------------------------- PRINT ---------------------------
#------------------------------------------------------------
@register.filter()
def specific_mul(x, y):
	return x * y

@register.filter()
def is_print_number_achieved(obj):
	"""
	Filter : Connaitre SI le nombre d'impressions effectuées est atteint 
	obj : l'objet qui possède la propriété (nombre_impression)
	"""
	obj_gv = GlobalVariablesHelpers.get_global_variables("PRINT", "MAX_NUMBER")
	nbr_print = 0

	if isinstance(obj, FoncierParcelle):
		nbr_print = obj.nombre_impression
			
	if obj_gv and nbr_print >= int(obj_gv.valeur):
		return True
	
	return False

#------------------------------------------------------------
@register.filter()
def get_total_batie(lst_batie):
	"""
	Renvoie le total des montants des construction
	"""
	total = 0
	for elt in lst_batie:
		if isinstance(elt, FoncierCaracteristique):
			total += elt.impot_batie.impot * elt.superficie_batie

	return total

#------------------------------------------------------------
@register.filter()
def get_note_imposition(obj):
	"""
	Renvoie l'id de la note d'imposition non payé pour l'impression
	"""
	if isinstance(obj, FoncierExpertise):
		try:
			note = NoteImposition.objects.get(entity=ENTITY_IMPOT_FONCIER, entity_id=obj.id)
			return note
		except:
			pass

	return None

#------------------------------------------------------------
@register.filter()
def set_disabled_a_print(obj):
	"""
	OBSOLETE MAIS IMPORTANT !!!!!!
	renvoie le css 'disabled' pour a-href (print direct si l'id de la note n'existe pas)
	"""
	res = ''
	if isinstance(obj, NoteImposition):
		if obj.is_payed:
			res = 'disabled_a_print'

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_label_non_bati(accessibilite):
	"""
	Renvoie les informations non bati
	"""
	res = ""
	obj = FoncierImpot.objects.get(accessibilite__id=accessibilite)
	if obj:
		res = str(obj.categorie) + " " + str(obj.type_confort) + " " + str(obj.accessibilite)

	return ""

#------------------------------------------------------------
#---------------------- TABLEAU DE BORD ---------------------
#------------------------------------------------------------
@register.filter()
def nombre_impot_foncier(value):
	"""
	Filter : renvoie le nombre total des impot focnier (parcelle, declaration)
	"""
	nombre = 0
	
	if value==1:
		# PARCELLE
		nombre = FoncierParcelle.objects.filter(date_validate__isnull=False).count()
	elif value==2:
		# DECLARATION
		nombre = FoncierExpertise.objects.filter(date_validate__isnull=False).count()

	return nombre

#------------------------------------------------------------
@register.filter()
def foncier_get_number_by_user(status, user):
	"""
	Renvoie le nombre de données saisies par utilisateur (SAISIES, VALIDE, GENERE, PAYE)
	1 :  En cours
	2 : Validés
	3 : Générés
	4 : Payés
	5 : imprimés
	enum.entity = ENTITY_IMPOT_FONCIER
	"""
	nombre = 0
	if isinstance(user, User):
		if status == 1:
			nombre = FoncierExpertise.objects.filter(user_create=user).count()
		elif status == 2:
			nombre = FoncierExpertise.objects.filter(user_validate=user).count()
		elif status == 3:
			nombre = FoncierExpertise.objects.filter(user_ecriture=user).count()
		elif status == 4:
			query = Q(entity=ENTITY_IMPOT_FONCIER) & Q(taxe_montant_paye__gte=F('taxe_montant')) & Q(date_validate__isnull=False) & Q(user_validate=user)
			nombre = NoteImposition.objects.filter(query).count()
		elif status == 5:
			query = Q(entity=ENTITY_IMPOT_FONCIER) & Q(taxe_montant_paye__gte=F('taxe_montant')) & Q(numero_carte_physique__isnull=False) & Q(user_validate=user)
			nombre = NoteImposition.objects.filter(query).count()

	return nombre

#------------------------------------------------------------
@register.filter()
def foncier_get_total_user(status):
	"""
	Renvoie le total de données saisies de tous les utilisateurs (SAISIES, VALIDE, GENERE, PAYE)
	1 : Saisies
	2 : Validées
	3 : Générées
	4 : Payées
	5 : imprimés
	enum.entity = ENTITY_IMPOT_FONCIER
	"""
	total = 0
	if status == 1:
		total = FoncierExpertise.objects.count()
	elif status == 2:
		total = FoncierExpertise.objects.filter(date_validate__isnull=False).count()
	elif status == 3:
		total = FoncierExpertise.objects.filter(date_ecriture__isnull=False).count()
	elif status == 4:
		query = Q(entity=ENTITY_IMPOT_FONCIER) & Q(taxe_montant_paye__gte=F('taxe_montant')) & Q(date_validate__isnull=False)
		total = NoteImposition.objects.filter(query).count()
	elif status == 5:
		query = Q(entity=ENTITY_IMPOT_FONCIER) & Q(taxe_montant_paye__gte=F('taxe_montant')) & Q(numero_carte_physique__isnull=False)
		total = NoteImposition.objects.filter(query).exclude(numero_carte_physique__exact='').count()

	return total

#------------------------------------------------------------
@register.filter()
def toto():
	sessions = Session.objects.filter(expire_date__gte=timezone.now())
	return sessions.count()

#------------------------------------------------------------
#---------------------- ACCROISSEMENT -----------------------
#------------------------------------------------------------
@register.filter()
def get_info_accroissement(obj):
	"""
	Renvoie l'info concernant l'accroissement 
	"""
	res = ''
	if isinstance(obj, FoncierExpertise):
		taux_accroisement = obj.has_accroissement
		if taux_accroisement>0:
			total, tnb, tb = get_montant_note(obj)
			accroissement = (total * taux_accroisement) / 100
			MONTANT_DU = accroissement + total
			res = "<span class='text-primary'>Vous avez un accroissement de <em class='text-danger'>" + str(taux_accroisement) + "%</em>, dû au retard de déclaration de l'impôt foncier. Le montant total <em class='text-danger'>À PAYER</em> s'élève à <em class='bg bg-warning text-dark'>&nbsp;<strong>" + str(intcomma(int(MONTANT_DU))) + ".Bif</strong>&nbsp;&nbsp;</em> dont la valeur de l'accroissement est de <em class='text-danger'>" + intcomma(int(accroissement)) + " Bif</em>.</span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_taux_accroissement(obj):
	"""
	Renvoie le taux d'accroissement 
	"""
	res = 0
	if isinstance(obj, FoncierExpertise):
		res = obj.has_accroissement
	
	return res

#------------------------------------------------------------
@register.filter()
def get_montant_accroissement(obj):
	"""
	Renvoie le montant de l'accroissement 
	"""
	res = 0
	if isinstance(obj, FoncierExpertise):
		taux_accroisement = obj.has_accroissement
		if taux_accroisement>0:
			total, tnb, tb = get_montant_note(obj)
			res = (total * taux_accroisement) / 100
			
	return res

#------------------------------------------------------------
@register.filter()
def show_taux_accroissement(obj):
	"""
	Afficher en html le taux d'accroissemnt si POSITIF
	"""
	res = ""

	if isinstance(obj, FoncierExpertise) and obj.accroissement_taux>0:
		res = "<span class='badge badge-warning'>" + str(obj.accroissement_taux) + "%</span>&nbsp;<span><strong>"

	return mark_safe(res)