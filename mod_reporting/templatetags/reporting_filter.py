
from django import template
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count

from mod_crm.models import *
from mod_activite.models import *
from mod_foncier.models import *
from mod_transport.models import *

register = template.Library()

#------------------------------------------------------------
#--------------------- MODULE REPORTING ---------------------
#------------------------------------------------------------
@register.filter()
def nombre_contribuable_created_by_user(user):
	"""
	Renvoie le nombre de contribuable créées par l'utilisateur
	"""
	nombre = Contribuable.objects.filter(user_create=user).count()

	return nombre

#------------------------------------------------------------
@register.filter()
def nombre_parcelle_created_by_user(user):
	"""
	Renvoie le nombre de parcelle créées par l'utilisateur
	"""
	nombre = FoncierParcelle.objects.filter(user_create=user).count()

	return nombre

#------------------------------------------------------------
@register.filter()
def nombre_declaration_created_by_user(user):
	"""
	Renvoie le nombre de parcelle créées par l'utilisateur
	"""
	nombre = FoncierExpertise.objects.filter(user_create=user).count()

	return nombre

#------------------------------------------------------------
@register.filter()
def nombre_standard_created_by_user(user):
	"""
	Renvoie le nombre de parcelle créées par l'utilisateur
	"""
	nombre = Standard.objects.filter(user_create=user).count()

	return nombre

#------------------------------------------------------------
@register.filter()
def nombre_marche_created_by_user(user):
	"""
	Renvoie le nombre de parcelle créées par l'utilisateur
	"""
	nombre = Marche.objects.filter(user_create=user).count()

	return nombre