from django.db import models
from django.conf import settings

#----------------------------------------------------------------------
#------------------------	MODELE NARCHIVE NOTE	-------------------
#----------------------------------------------------------------------

class NoteArchive(models.Model):
	"""
	Modele Note archive
	"""
	# Référence de l'Entity Modèle (voir parametrage.enum)
	entity = models.CharField(max_length=255)
	
	# Identifiant de l'entity
	entity_id = models.IntegerField()

	# Note envoyée par un autre user ou lui même
	note = models.CharField(max_length=255)

	user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
		related_name='%(class)s_requests_note')
	
	date_note = models.DateTimeField()

	# Réponse de la note par l'user de création
	reponse_note = models.CharField(max_length=255, blank=True, null=True)

	# Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
	demande_annulation_validation = models.BooleanField(default=False)

	# Traçabilité de l'annulation
	date_cancel = models.DateTimeField(null=True)
	user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
		related_name='%(class)s_requests_cancel', null=True)

	date_create = models.DateTimeField(auto_now_add=True)
	user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')

	class Meta:
		ordering = ('-id', )

	def __str__(self):
		return self.note
