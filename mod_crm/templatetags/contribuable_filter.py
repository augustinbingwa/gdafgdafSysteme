
from django import template
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.conf import settings

from mod_crm.models import *
from mod_activite.models import *
from mod_foncier.models import *
from mod_transport.models import *
from mod_parametrage.enums import *

register = template.Library()

#------------------------------------------------------------
@register.filter()
def filter_status_validate(obj):
	"""
	Filter : pour le status des contribuables
	"""
	objToRet= "<span class='badge badge-danger'>Non validé</span>"
	if obj:
		if obj.date_validate:
			objToRet =  "<span class='badge badge-success'>Validé: " + obj.date_validate.strftime("%d/%m/%Y") + "</span>"
		else:
			# Ca personne physique
			if isinstance(obj, PersonnePhysique):
				if obj.identite_file and obj.photo_file:
					objToRet = "<span class='badge badge-warning'>En attente</span>"
			elif isinstance(obj, PersonneMorale):
				# Cas personne morale
				if obj.type_caractere == COMMERCIAL:
					if obj.nif_file and obj.rc_file:
						objToRet = "<span class='badge badge-warning'>En attente</span>"
				else:
					if obj.nif_file:
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
	
	return 'N°' + value

#------------------------------------------------------------
@register.filter()
def get_photo_passeport(value):
	if value:
		return settings.MEDIA_URL + str(value)

	return '/static/img/photo.jpg'

#------------------------------------------------------------
@register.filter()
def nombre_contribuables(value):
	"""
	Filter : renvoie le nombre nombre des contribuables enregistrés sur le système
	"""
	nombre = 0

	if value==1:
		# Physique
		nombre = PersonnePhysique.objects.filter(date_validate__isnull=False).count()
	elif value==2:
		# Morale
		nombre = PersonneMorale.objects.filter(date_validate__isnull=False).count()
	elif value==3:
		# Physique et/ou Morale dans TRANSPOT (VEHICULES)
		nombre = Vehicule.objects.filter(date_validate__isnull=False).values('contribuable').distinct().count()
	elif value==4:
		# Physique et/ou Morale dans ACTIVITE STANDARD
		nombre = Standard.objects.filter(date_validate__isnull=False).values('contribuable').distinct().count()
	elif value==5:
		# Physique et/ou Morale dans ACTIVITE MARCHE
		nombre = AllocationPlaceMarche.objects.filter(date_validate__isnull=False).values('contribuable').distinct().count()
	elif value==6:
		# Physique et/ou Morale dans IMPOT FONCIER
		nombre = FoncierParcelle.objects.filter(date_validate__isnull=False).values('contribuable').distinct().count()
	else:
		# Tous
		nombre = Contribuable.objects.filter(date_validate__isnull=False).all().count()
	
	return nombre

#------------------------------------------------------------
@register.filter()
def filter_value_none(value):
	"""
	Filter : pour la vaeur nulle, afficher vide
	"""
	if value is None:
		return ''
	return value
#------------------------------------------------------------
@register.filter()
def filter_adresse_none(value):
	"""
	Filter : pour la valeur nulle, afficher vide
	"""
	if value is None:
		return ''
	return '/' + value

#------------------------------------------------------------
@register.filter()
def filter_type_caractere(value):
	"""
	Filtere : afficher commercial ou organisme
	"""
	objToRet= "<span class='text text-info'>Organisme</span>"
	if value == 0:
		objToRet= "<span class='text text-primary'>Commercial</span>"
	elif value == 2:
		objToRet= "<span class='text text-success'>Association</span>"

	return mark_safe(objToRet) 

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
		if obj.date_validate and obj.date_cancel:
			note = "<i class='fa fa-commenting' aria-hidden='true' style='color:#2C75FF;'></i>&nbsp;"	
		elif obj.demande_annulation_validation:
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
def phone_format(tel):
	"""
	Convertir le numero du tel en +xxx xxxxxxx
	"""
	if tel is None or tel=='':
		return ''
	
	first = tel[0:4]
	second = tel[4:20]
	res = "<span class='fa fa-phone text-dark'>&nbsp;" + first + ' ' + second + "</span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def email_format(email):
	"""
	Convertir le numero du tel en +xxx xxxxxxx
	"""
	if email is None or email=='':
		return ''
	
	res = "<a href='#'class='text-primary'><i class='fa fa-envelope'></i>&nbsp;" + email + "</a>"

	return mark_safe(res)

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
	
	if obj and isinstance(obj, PersonnePhysique):
		nombre = PersonnePhysique.objects.filter(user_create=user).count()
		nombre_valid = PersonnePhysique.objects.filter(user_create=user, date_validate__isnull=False).count()

	elif obj and isinstance(obj, PersonneMorale):
		nombre = PersonneMorale.objects.filter(user_create=user).count()
		nombre_valid = PersonneMorale.objects.filter(user_create=user, date_validate__isnull=False).count()
	
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
@register.filter()
def get_contribuable_physique_by_user(user, status):
	"""
	Renvoie le nombre de controbuables physiques par utilisateur
	"""
	nombre = 0
	if user and isinstance(user, User):
		if status==1:
			nombre = PersonnePhysique.objects.filter(user_create=user).count()
		elif status==2:
			nombre = PersonnePhysique.objects.filter(user_create=user, date_validate__isnull=False).count()

	return nombre

#------------------------------------------------------------
@register.filter()
def get_contribuable_morale_by_user(user, status):
	"""
	Renvoie le nombre de controbuables morales par utilisateur
	"""
	nombre = 0
	if user and isinstance(user, User):
		if status==1:
			nombre = PersonneMorale.objects.filter(user_create=user).count()
		elif status==2:
			nombre = PersonneMorale.objects.filter(user_create=user, date_validate__isnull=False).count()

	return nombre