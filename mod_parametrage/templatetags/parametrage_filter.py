from django import template
from django.utils.safestring import mark_safe

from mod_parametrage.models import Notification
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers

from mod_activite.models import *
from mod_transport.models import *

from datetime import datetime

register = template.Library()

#------------------------------------------------------------
@register.filter()
def filter_status_validate(date_validate):
	"""
	Filter : pour le status des activités
	Si validé -> 
	Si Cloturé -> Clôturé
	Cloturé > Validé
	"""
	res= "<span class='badge badge-warning'>Envoyé</span>"	

	if date_validate:
		res = "<span class='badge badge-success'>Récu le <br>"+ format(date_validate, '%d/%m/%Y') + " </span>"
	
	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_adresse_exacte(obj):
	"""
	Renvoyer l'adresse exacte si rue_avenue n'existe pas
	"""
	if not obj.contribuable.numero_rueavenue:
		if obj.contribuable.adresse_exacte is not None:
			return obj.contribuable.adresse_exacte.capitalize()

	return ''

#------------------------------------------------------------
@register.filter()
def get_numero_police(numero_police):
	"""
	Renvoyer le numero de police formaté si existe
	"""
	if numero_police:
		return ' n°' + numero_police

	return ''

#------------------------------------------------------------
@register.filter()
def get_entity_nb(value):
	"""
	Filter : renvoie la note le quittance de l'entity modèle (numero de carte, ref de l'activité, etc.)
	Qui se trouve dant GobalesVariables
	"""
	res = ''

	if isinstance(value, VehiculeProprietaire):
		res = GlobalVariablesHelpers.get_global_variables('NB', 'CARTE_PROPRIETE').valeur
	elif isinstance(value, VehiculeActivite) or isinstance(value, Standard) or isinstance(value, Marche):
		res = GlobalVariablesHelpers.get_global_variables('NB', 'CARTE_PROFESSIONNELLE').valeur
	else:
		res = GlobalVariablesHelpers.get_global_variables('NB', 'QUITTANCE_ACTIVITE_TRANSP').valeur

	return res

#------------------------------------------------------------
@register.filter()
def get_file_upload_old(file):
	"""
	Filter : pour le file upload
	"""
	res = 'Seléctionner un fichier ...'
	if file:
		res = "<i class='fa fa-file-o'></i>&nbsp;<span class='text text-success'></span>" + str(file)

	return mark_safe(res)

@register.filter()
def get_file_upload(file, placehoulder=None):
	"""
	Filter : pour le status des véhicule, activité véhicule, ...
	"""
	res = 'Seléctionner un fichier'
	if placehoulder:
		res = 'Seléctionner &lt; <strong><em>' + placehoulder + '</strong></em> &gt; ...'

	if file:
		if placehoulder:
			res = "<i class='fa fa-eye'></i>&nbsp;<span class='text-success' title='Visualiser'><em>" + placehoulder + "</em></span>&nbsp;<span class='text text-success'></span>" #+ str(file)
		else:
			res = "<i class='fa fa-eye'></i>&nbsp;<span class='text text-success'></span>" + str(file)

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_file_upload_url(file):
	"""
	Filter : pour l'upload du fichier
	"""
	if file:
		return file.url

	return 