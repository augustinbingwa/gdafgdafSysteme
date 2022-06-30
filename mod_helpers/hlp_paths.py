from uuid import uuid4
import os

class PathsHelpers():
	PHOTO_USER_FOLDER = 'photo_user_folder/' #path des photos des utilisateurs (image photo passport (4*4))


	PHOTO_FOLDER = 'photo_folder/' #path des photos des contribuables (image photo passport (4*4))
	IDENTITE_FOLDER = 'identite_folder/' #path des Identite (CNI, Passport) des contribuables(pdf ou image scanné, etc)
	NIF_FOLDER = 'nif_folder/' #path des nif des contribuables physiques et morales (pdf ou image scanné, etc)
	RC_FOLDER = 'rc_folder/' #path des registres de commerce des contribuables
	BORDEREAU_FOLDER = 'bordereau_folder/' #path des boredereau de versement
	
	#répertoire activité cas marché
	ALLOCATION_PLACE_MARCHE_CONTRAT_FOLDER = 'allocation_place_marche_contrat_folder/' #path des contrats allocation place marché 

	#répertoire activité standard
	ACTIVITE_STANDARD_AUTORISATION_FOLDER = 'activite_standard_autorisation_folder/' #path des autorisations des activités standard 	
	
	#Répertoire visite sites touristiques
	BORDERAU_FOLDER_SITE_TOURISTIQUE = 'borderau_folder_site_touristique/' #path des bordereau des visites des sites touristiques

	#Répertoire activité exceptionnelle
	BORDERAU_FOLDER_ACTIVITE_EXCEPTIONNELLE = 'borderau_folder_activite_exceptionnelle/' #path des bordereaudes activités exceptionnelles

	#Répertoire site standard
	BORDERAU_FOLDER_STANDARD = 'borderau_folder_standard/' #path des ordereau standard (activité)

	#Répertoire occupation de l'espace publique
	ESP_LETTRE_EXP_TMP = 'esp_lettre_exp_tmp_folder/' #path des Lettre de demande de l’exploitation temporaire
	ESP_RAP_VIS_TER = 'esp_rap_vis_ter_folder/' #path des Rapport de visite du terrain

	#Répertoire panneau publicitaire
	PANNEAU_LETTRE_EXP_TMP = 'esp_lettre_exp_tmp_folder/' #path des Lettre de demande de l’exploitation temporaire
	PANNEAU_RAP_VIS_TER = 'esp_rap_vis_ter_folder/' #path des Rapport de visite du terrain

	#Répertoire pour les publicité sur les mur/clôtures
	MUR_CLOTURE_LETTRE_EXP_TMP = 'esp_lettre_exp_tmp_folder/' #path des Lettre de demande de l’exploitation temporaire
	MUR_CLOTURE_RAP_VIS_TER = 'esp_rap_vis_ter_folder/' #path des Rapport de visite du terrain

	#répertoire pour formulaire d'arrêt 
	FORMULAIRE_ARRET = 'formulaire_arret_folder/' #Un formulaire d'arrêt d'activité à remplir mannuellement et à joindre
	FORMULAIRE_CARTE_ARRET = 'formulaire_carte_arret_folder/' #Un formulaire d'arrêt d'activité à remplir mannuellement et à joindre

	#path des boredereau de versement d'avis d'imposition
	BORDEREAU_AI_FOLDER = 'bordereau_ai_folder/'

	#path des boredereau de versement des notes d'imposition
	BORDEREAU_NI_FOLDER = 'bordereau_ni_folder/'

	#path des boredereau de versement des notes d'imposition EXTERNE
	BORDEREAU_NI_FOLDER_EXTERNE = 'bordereau_ni_folder_externe/'

	#path des La numérisation ou scan de déclaration à l’impôt foncier. Département IMPOSITION
	DECLARATION_FONCIER_FOLDER  = 'declaration_foncier_folder/'

	#path des Demande d’une attestation d’appartenance de parcelle.
	CONTRAT_VENTE_FOLDER = 'contrat_vente_folder/'
	PARCELLE_HISTORIQUE  = 'parcelle_historique_folder/'
	ATTESTATION_VENTE_FOLDER = 'attestation_vente_folder/'
	ATTESTATION_COMPO_FAMILIALE_FOLDER = 'attestation_compo_familiale_folder/'
	CERTIFICAT_CONFORMITE_FOLDER = 'certificat_conformite_folder/'
	PV_ARPENTAGE_BORNAGE_FOLDER = 'pv_arpentage_bornage_folder/'
	PV_CONSEIL_FAMILLE_FOLDER = 'pv_conseil_famille_folder/'
	ACTE_NOTORITE_FOLDER = 'acte_notorite_folder/'

	#path des Demande d’une Convention d’exploitation temporaire d’un Espace publique (CONTRAT)
	LETTRE_DEMANDE_EXP_TEMP_FOLDER = 'lettre_demande_exp_temp_folder/' #Lettre de demande de l’exploitation temporaire
	RAP_VISITE_TERRAIN_FOLDER  = 'rap_visite_terrain_folder/' #Rapport de visite du terrain

	
	#path Expertise et rapport d’expertise
	ANR_EXPERTISE_FOLDER = 'lettre_demande_espace_exp_folder/' #Lettre de demande de l’exploitation temporaire
	LETTRE_DEMANDE_ESPACE_EXP_FOLDER  = 'anr_expertise_folder/' #Rapport de visite du terrain

	# ----------------Module : TRANSPORT ---------------------
	#répertoire du scan des cartes roses des véhicules
	VEHICULE_CARTEROSE_FOLDER = 'vehicule_carterose_folder/'
	VEHICULE_ACTIVITE_CARTEROSE_FOLDER = 'vehicule_activite_carterose_folder/'
	VEHICULE_ACTIVITE_AUTORISATION_FOLDER = 'vehicule_activite_autorisation_folder/' # Autorisation de trasport du Ministere de commerce

	#répertoire du scan des formulaires d'arrêt de service des véhicules
	VEHICULE_ACTIVITE_FORMULAIRE_ARRET_FOLDER = 'vehicule_activite_formulaire_arret_folder/'
	
	#répertoire pour les QR Code des cartes des activités de transport rémunéré des véhicules
	VEHICULE_CARTE_ACTIVITE_TRANSPORT_QR_FOLDER = 'vehicule_carte_activite_transport_qr_folder/'

	#répertoire pour les QR Code des duplicats des cartes des activités de transport rémunéré des véhicules
	VEHICULE_CARTE_ACTIVITE_TRANSPORT_DUPLICATA_QR_FOLDER = 'vehicule_carte_activite_transport_duplicata_qr_folder/'

	#répertoire pour les QR Code des cartes des propritaires des véhicules
	VEHICULE_CARTE_PROPRIETAIRE_QR_FOLDER = 'vehicule_carte_proprietaire_qr_folder/'

	#répertoire pour les QR Code des duplicats des cartes des propritaires des véhicules
	VEHICULE_CARTE_PROPRIETAIRE_DUPLICATA_QR_FOLDER = 'vehicule_carte_proprietaire_duplicata_qr_folder/'

	#répertoire pour les QR Code des cartes de stationnement
	VEHICULE_CARTE_STATIONNEMENT_QR_FOLDER = 'vehicule_carte_stationnement_qr_folder/'

	#répertoire pour les QR Code des duplicatas des cartes de stationnement
	VEHICULE_CARTE_STATIONNEMENT_DUPLICATA_QR_FOLDER = 'vehicule_carte_stationnement_duplicata_qr_folder/'
	REPORT_BANK_FILE = 'fichier_rapport_bank/'

	# ----------------Méthode : Rename -----------------------
	def path_and_rename(instance, filename, upload_to):
		"""
		Méthode utiliséé pour remplacer automatiquement le nom de fichier par l'ID encours
		"""
		ext = filename.split('.')[-1]
		# get filename
		if instance.pk:
			filename = '{}.{}'.format(instance.pk, ext)
		else:
			# set filename as random string
			filename = '{}.{}'.format(uuid4().hex, ext)
		# return the whole path to the file
		return os.path.join(upload_to, filename)