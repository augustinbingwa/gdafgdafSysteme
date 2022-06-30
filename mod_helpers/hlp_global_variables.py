from mod_parametrage.models import GlobalVariables
from django.core.exceptions import ObjectDoesNotExist

#--------------------------------------------------------------------------------
class GlobalVariablesHelpers():
	def save_global_variables():
		"""
		Créer les lignes "variables" suivantes, ceci afin d'assurer l'existance des info
		Event : au lancement de l'applicaiton (runserver)
		Voir (mod_helpers : apps.py et __init__.py)
		"""
		obj = GlobalVariables(group="PRINT", cle="MAX_NUMBER", valeur=3, description="Nombre d'impression maximum sur un papier sécurisé (carte professionnelles, propriétaires, quittances, ...)")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		obj = GlobalVariables(group="PRINT", cle="MAX_TIME", valeur=1, description="Nombre de jours maximum pour faire une re-impression sur un papier sécurisé (carte professionnelles, propriétaires, quittances, ...")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# NIF de la mairie
		obj = GlobalVariables(group="MAIRIE", cle="NIF", valeur=4000339541, description="NIF de la mairie")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# Adresse de la mairie
		obj = GlobalVariables(group="MAIRIE", cle="ADRESSE", valeur="Avenue de l'Université n°1, BP 117 Bujumbura", description="NIF de la mairie")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# Contact de la mairie
		obj = GlobalVariables(group="MAIRIE", cle="CONTACT", valeur="Télephone : +257 2224 6621", description="NIF de la mairie")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# Impôt foncier, date imite de déclaration de l'impot foncier
		obj = GlobalVariables(group="FONCIER", cle="DATE_LIMIT_DECLARATION", valeur="30/03", description="Date limite de déclaration de l'impôt foncier (dd/mm)")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# Impôt foncier, montant mnimal de déclaration de l'impot foncier
		obj = GlobalVariables(group="FONCIER", cle="MONTANT_MINIMALE_NOTE", valeur="1000", description="L'impôt inférieur à 1000 Bif n'est par perçu.")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# Impôt foncier, nombre d'années max d'exhoneration d'une déclaration de construction (à utliser dans la date de mise en valeur d'une déclaration)
		obj = GlobalVariables(group="FONCIER", cle="NOMBRE_ANNEE_MISE_EN_VALEUR", valeur="2", description="Nombre d'années max d'exhoneration d'une déclaration de l'impôt foncier selon la date de mise en valeur d'une construction")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# Date limite de paiement du droit de stationnement
		obj = GlobalVariables(group="STATIONNEMENT", cle="DATE_LIMIT_PAIE_STATIONNEMENT", valeur="05", description="Date limite de paiement du droit de stationnement sera le 05 de chaque mois. (On paie ici le mois échu)")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# Date limite de paiement de la tax sur activité d transport
		obj = GlobalVariables(group="ACTIVITE_TRANSPORT", cle="DATE_LIMIT_PAIE_ACTIVITE_TRANSPORT", valeur="15", description="Date limite de paiement de la taxe sur activité transport, sera le 15 de chaque début du trimestre. (On paie pour le trimestre en cours)")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# NB pour quittance activité de transport
		
		obj = GlobalVariables(group="NB", cle="QUITTANCE_ACTIVITE_TRANSP", valeur="La taxe est payée anticipativement, et dans les 15.", description="Note sur les quittance du transport rémunéré")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()
		

		# NB pour carte de propriété
		obj = GlobalVariables(group="NB", cle="CARTE_PROPRIETE", valeur="En cas de vente, veuillez remettre cette carte.", description="Pour ne plus être redevable, ce message rappelle en cas d'arrêt de paiement de l'impot")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# NB pour toute carte professionnelle
		obj = GlobalVariables(group="NB", cle="CARTE_PROFESSIONNELLE", valeur="En cas d'arrêt d'activité, veuillez remettre cette carte.", description="Pour ne pas ere redevable, ce message rappelle en cas d'arrêt d'activité")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# TRANSPORT
		obj = GlobalVariables(group="TRANSPORT", cle="PLAQUE_DEFAULT", valeur="BJM", description="Plaque par defaut pour les velo/cyclomoteur qui n'ont pas de plaque de l'OBR")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()
		
		# ALLOCATION PLACE MARCHE : Nombre de jour por la caution
		obj = GlobalVariables(group="ALLOCATION_PLACE_MARCHE", cle="CAUTION", valeur="3", description="Nombre de mois de la caution à payer lors de l'allocation de place dans le marché")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# Note d'imposition, date limite de e paiement
		obj = GlobalVariables(group="NI", cle="DATE_LIMITE_PAIEMENT", valeur="30/03", description="Date limite de paiement (dd/mm)")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		# PENALITE
		obj = GlobalVariables(group="PENALITE", cle="VALEUR_PREMIER_MOIS", valeur="10", description="Pénalité pour retard de paiement à la date limite pour le mois %")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		obj = GlobalVariables(group="PENALITE", cle="VALEUR_AUTRES_MOIS", valeur="1", description="Pénalité pour retard de paiement mensuel pour les autres mois %")
		if not GlobalVariables.objects.filter(group=obj.group, cle=obj.cle): 
			obj.save()

		return

	def get_global_variables(group, cle):
		"""
		Chercher l'objet globa variable
		"""
		try:
			obj = GlobalVariables.objects.filter(group=group, cle=cle)[0]
		except ObjectDoesNotExist:
			return None

		return obj