
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from django.utils import timezone
import datetime

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.models import Chrono

'''
Cette classe est l'ensemble des groupes d'action à savoir : create, update, validate, print ...
'''
class OperationsHelpers():
	'''
	Cette fonction permet d'éxecuter les actions.
	Actions : create, update, validate, print
	Form : Contribuable, Activité, etc. (Toute forme ayant comme champs de numero chronologique)
	'''
	def execute_action(request, action, form, prefixe='', num_chrono=''):
		"""
		Setting the user on create, update, validate
		"""
		try:
			with transaction.atomic():
				obj = form.save(commit=False)
				user = User.objects.get(pk=request.user.id) # get current user 
				dateTimeNow = datetime.datetime.now(tz=timezone.utc)

				if action == 'create':
					obj.user_create = user

					# Sauvegarder le nouveau numéro chrono
					if prefixe.strip() != '' and num_chrono.strip() != '' :
						new_chrono = form.cleaned_data[num_chrono]
						
						# 1 - load l'objet chrono
						obj_chrono = Chrono.objects.get(prefixe=prefixe)

						# 2 - Récuperer le nouveau numéero chrono
						obj_chrono.last_chrono = new_chrono

						# 3 Sauvegarder le numero
						obj_chrono.save();

				if action == 'update':
					obj.date_update = dateTimeNow
					obj.user_update = user

				if action == 'validate':
					obj.date_validate = dateTimeNow
					obj.user_validate = user

				if action == 'print':
					obj.date_print = dateTimeNow
					obj.user_print = user

				# Sauvegarder l'objet principal
				obj.save()

		except IntegrityError as e:
			return str(e) # Autre erreur

		return None # Save OK

	def execute_action_validate(request, obj):
		"""
		Generer la traçabilité de la validation
		"""
		user = User.objects.get(pk=request.user.id) # get current user 
		dateTimeNow = datetime.datetime.now(tz=timezone.utc)
		
		obj.date_validate = dateTimeNow
		obj.user_validate = user
		obj.save()
		
		return

	def execute_action_ecriture(request, obj):		
		"""
		Generer la traçabilité de l'ecriture
		"""
		user = User.objects.get(pk=request.user.id) # get current user 
		dateTimeNow = datetime.datetime.now(tz=timezone.utc)
		
		obj.date_ecriture = dateTimeNow
		obj.user_ecriture = user
		obj.save()
		
		return
		
	def execute_action_print(request, obj):
		"""
		Generer la traçabilité de l'impression
		"""
		user = User.objects.get(pk=request.user.id) # get current user 
		dateTimeNow = datetime.datetime.now(tz=timezone.utc)
		
		obj.date_print = dateTimeNow
		obj.user_print = user
		obj.save()

		return