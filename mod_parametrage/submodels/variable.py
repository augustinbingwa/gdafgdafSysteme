from django.db import models

#----------------------------------------------------------------------
#-------------- Paramétrage globale de l'application ------------------
#-------------------- -------------------------------------------------

class GlobalVariables(models.Model):
	"""
	Modele Qui contient toutes les vaiables globales de l'application.
	"""
	group = models.CharField(max_length=50, verbose_name="Group")
	cle = models.CharField(max_length=50, verbose_name="Clé")
	valeur = models.TextField(max_length=1024, verbose_name="Valeur")
	description = models.TextField(max_length=1024, verbose_name="Description")

	class Meta:
		# group + cle doit être 'unique'
		index_together = unique_together = [['group', 'cle']]

		ordering = ('group', 'cle')
		
	def __str__(self):
		return u"{ '%s' : '%s' }" % (self.cle, self.valeur)