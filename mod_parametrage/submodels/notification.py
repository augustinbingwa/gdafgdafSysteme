from django.db import models
from django.conf import settings # authetification user model
from mod_parametrage.enums import *

#----------------------------------------------------------------------
#------------------- Paramétrage des notifiations ---------------------
#-------------------- -------------------------------------------------

class Notification(models.Model):
	"""
	Modele Qui contient les information d'une notification
	"""
	# Type de notificaiton (Simple message ou Action sur une entité)
	type = models.IntegerField(choices=choix_notification, default=MSG_SIMPLE) 
	
	# Objet de la demande
	objet = models.CharField(max_length=50, verbose_name="Group")

	#----------------------------------------------------------------
	#------------------- ENTITY MODEL FACULTATIF --------------------	
	#----------------------------------------------------------------
	# Référence de l'Entity Modèle (voir parametrage.enum)
	entity = models.PositiveSmallIntegerField(choices=choix_entity_imposition, null=True)
	
	# Identifiant de l'entity
	entity_id = models.IntegerField(null=True)
	
	#----------------------------------------------------------------
	#----------------------------- ENVOI ----------------------------
	#----------------------------------------------------------------
	# Message à envoyer(Ex : Demande d'autorisation d'impression, message simple, ...)
	message = models.CharField(max_length=255, verbose_name="Group")

	# Demandeur (utilisateur qui demande l'autorisation)
	user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
		related_name='%(class)s_requests_created')

	# date d'envoi de la notification
	date_create = models.DateTimeField(auto_now_add=True)

	#----------------------------------------------------------------
	#-------------------------- DSTINATION --------------------------
	#----------------------------------------------------------------
	# Réponse
	reponse = models.CharField(max_length=255, verbose_name="Group", blank=True, null=True)

	# Validateur (utilisater qui valide l'autorisation) ---> default ADMINISTRATEUR
	user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
		related_name='%(class)s_requests_validate')

	# date validation de la notificaiton (date de réponse)
	date_validate = models.DateTimeField(null=True)
	
	class Meta:
		ordering = ('-date_create', )
		
	def __str__(self):
		return self.objet
