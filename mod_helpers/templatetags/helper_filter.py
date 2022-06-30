from django import template
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.conf import settings

import re

from num2words import num2words # CHIFFER TO LETTRE
from mod_helpers.models import UserProfile

register = template.Library()

#------------------------------------------------------------
@register.filter()
def get_info_object(obj):
	"""
	Renvoie quelques info  de la classe (via l'instance obj)
	"""
	info = re.findall('[A-Z][^A-Z]*', obj.__class__.__name__)
	res = ''
	for elt in info:
		res += ' ' + str(elt)

	res = "'<strong><em>" + res.strip().capitalize() + "</em></strong>'"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter(name='has_group')
def has_group(user, group_name):
	"""
	GESTION DES MENUS BASES PAR GROUP
	"""
	if not user:
		return False

	group = Group.objects.get(name=group_name)

	return True if group in user.groups.all() else False

#------------------------------------------------------------
@register.filter(name='get_user_annulation')
def get_user_annulation(obj_entity):
	"""
	AFFICHER L'UTILISATEUR QUI A ANNULÉ LA VALIDATION AINSI QUE LA DATE ET HEURE
	"""
	res = ''
	user = ''
	time = ''

	if obj_entity:
		if obj_entity.user_cancel:
			user = 'Annulé par ' + str(obj_entity.user_cancel).capitalize()
		else:
			if not obj_entity.date_validate and obj_entity.demande_annulation_validation:
				user = "Annulé par l'Administrateur"

		if obj_entity.date_cancel:
			time = ' le ' + obj_entity.date_cancel.strftime("%d/%m/%Y à %H:%M:%S")
		else:
			if not obj_entity.date_validate and obj_entity.demande_annulation_validation:
				time = ' le ' + obj_entity.date_note.strftime("%d/%m/%Y à %H:%M:%S")
			
		res = "<span class='text-danger'><em>" + user + time + "</em></span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_user_current_group(user):
    """
    Renvoie le nom du group de l'utilisateur en cours
    """
    try:
        service = user.groups.all()[0].name.split('_')[1]
        res = "<strong class='text-secondary'>Service " + service.capitalize() + "</strong>" 
    except:
        res = "<strong class='text-secondary'>Administrateur</strong>"

    return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def show_me_dashboard(user, request):
    """
    Filtere : Afficher les producitons des ustilisateurs dans les tableau de bord
    """
    if request.user==user:
        res = "&nbsp;<span class='text-primary'><strong>" + str(user).capitalize() + "</strong><span>"
    elif user in request.online_now: #MiddleWare : User online
        res = "&nbsp;<span class='text-dark'><strong>" + str(user).capitalize() + "</strong><span>"
    else:
        res = "&nbsp;<span class='text-secondary'><strong>" + str(user).capitalize() + "</strong><span>"

    return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_all_groups_by_user(user):
	"""
	Renvoie la liste des groups sous forme d'une chaine de caractère
	"""
	res = ''
	for group in user.groups.all().order_by('name'):
		if not res:
			res = group.name
		else:
			res += ', ' + group.name

	if user.is_superuser:
		res = "<span class='text-primary'>SUPER ADMIN<span>"
	elif user.is_staff:
		res = "<span class='text-warning'>EQUIPE<span>"
	
	if res=='':	
		res = "<span class='text-secondary'>Non défini<span>"
	else:
		res = "<span class='text-dark'>" + res + "<span>"

	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_my_groups(user):
	"""
	Renvoie la liste des groups sous forme d'une chaine de caractère
	"""
	res = ''
	for group in user.groups.all().order_by('name'):
		if not res:
			res = group.name
		else:
			res += ', ' + group.name

	if user.is_superuser:
		res = "SUPER ADMIN"
	elif user.is_staff:
		res = "EQUIPE"
	
	if res=='':	
		res = "Non défini"
	
	return mark_safe(res)

#------------------------------------------------------------
@register.filter()
def get_user_name(user):
	"""
	Renvoie la fonction de l'user
	"""
	res = ''
	if user and isinstance(user, User):
		if user.last_name:
			res = user.last_name + ' '
		if user.first_name:
			res += user.first_name
		if not res:
			res = user.username.capitalize()

	return res

#------------------------------------------------------------
@register.filter()
def get_user_avatar(user):
	"""
	Renvoie le chemin complète de l'avatar de l'utilisateur'
	"""
	res = '/static/img/photo.jpg' #'/static/img/avatars/homme.jpg'
	if isinstance(user, User):
		try:
			obj = UserProfile.objects.get(user=user)
			if obj:
				return settings.MEDIA_URL + str(obj.avatar)
		except:
			pass

	return res

#------------------------------------------------------------
@register.filter()
def get_user_tel(user):
	"""
	Renvoie le ted de l'user
	"""
	res = ''
	if isinstance(user, User):
		try:
			obj = UserProfile.objects.get(user=user)
			if obj:
				return obj.tel
		except:
			pass

	return res

#------------------------------------------------------------
@register.filter()
def get_user_email(user):
	"""
	Renvoie l'email de l'user
	"""
	res = ''
	if isinstance(user, User):
		try:
			obj = UserProfile.objects.get(user=user)
			if obj:
				return obj.email
		except:
			pass

	return res

#------------------------------------------------------------
@register.filter()
def get_user_function(user):
	"""
	Renvoie la fonction de l'user
	"""
	res = ''
	if isinstance(user, User):
		try:
			obj = UserProfile.objects.get(user=user)
			if obj:
				return obj.fonction
		except:
			pass

	return res

#------------------------------------------------------------
@register.filter()
def int_to_letter(value):
	"""
	Renvoie le chiffre en lettre
	"""
	res = "Certifié sincère et véritable, arrêté à la somme de <em>" + num2words(value, lang='fr').capitalize() + " francs burundais. </em>"

	return mark_safe(res)