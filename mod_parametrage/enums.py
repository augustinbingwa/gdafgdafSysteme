MONNAIE = 'BIF'

"""
-------------------- GSTION DES NOTIFICATIONS -----------------------
"""
MSG_SIMPLE = 0
MSG_ENTITY = 1
choix_notification = (
	(MSG_SIMPLE, 'Message simple'), 
	(MSG_ENTITY, "Demande d'autorisation"),
)

"""
--------------CHOIX POUR LA GESTION DES CONTRIBUABLES----------------
"""
#Identitité des personnes physiques
CNI=0
PASSEPORT=1

choix_identite = (
	(CNI, 'CNI'), 
	(PASSEPORT, 'Passeport'),
)

#sexe pour personnes physiques
FEMININ = 0
MASCULIN = 1

choix_sexe = (
	(FEMININ, 'F'), 
	(MASCULIN, 'M'),
)

"""
------------- CHOIX DE TARIF ------------------
"""
#choix tarif
FORFAITAIRE = 0
POURCENTAGE = 1
VARIABLE = 2

choix_tarif = (
	(FORFAITAIRE, "Forfaitaire"),	#Ex : 50 000 fbu
	(POURCENTAGE, "Pourcentage"),	#Ex : 5% du prix de la chambre ou tikcet de spectacle
	(VARIABLE, "Variable"), 	#Ex : Entre 500 et 50000 d'amende administrative
)

"""
------------- CHOIX CONTRIBUABLE PERSONNE MORALE -------------
# Impact sur Pour les panneau publicitaires (les tarifs sont différents)
"""
COMMERCIAL = 0
LUCRATIF = 1
ASSOCIATION = 2

choix_caractere = ( 
	(COMMERCIAL, 'Commercial'), 
	(LUCRATIF, 'Sans but lucratif'),
	(ASSOCIATION, 'Co-propriétaire - Succession - etc.'),
)

"""
------------- CHOIX D'ESPACE / PUBLICITE ------------------
"""
#Type d'espace de l'activité
PRIVE = 0
PUBLIQUE = 1

choix_espace = ( 
	(PRIVE, 'Privé'), 
	(PUBLIQUE, 'Public'),)

#Publicité
MUR = 0
CLOTURE = 1

choix_publicite = (
	(MUR, 'Mur'), 
	(CLOTURE, 'Clôture'),
) 

"""
------------------ CHOIX TYPE D'IMPOSTION -----------------
"""
#Type imposition
AI = 0
NI = 1

choix_imposition = (
	(AI, "Avis d'imposition"), 
	(NI, "Note d'imposition"),
)

"""
------------------------- MENU POUR AVIS IMPOSTION ------------------
"""

AVIS_ACTIVITE_STANDARD = 0				# BaseActivite (Standard)
AVIS_ACTIVITE_MARCHE = 1				# BaseActivite (Marché)
AVIS_ACTIVITE_EXCEPTIONNELLE = 2		# ActiviteExceptionnel
AVIS_VISITE_TOURISTIQUE = 3				# VisiteSiteTouristique
AVIS_ACTIVITE_TRANSPORT = 4				# VehiculeActivite, VehiculeProprietaire, VehiculeActiviteDuplicata, VehiculeProprietaireDuplicata
AVIS_BATIMENTS_MUNICIPAUX = 5			# BatimentMunicipal
AVIS_ALLOCATION_ESPACE_PUBLIQUE = 6		# AllocationEspacePublique


"""
-- CHOIX POUR LA CLASSIFICATION DES TAXES : Réf: Taxe.taxe_filter ---
"""
#constante pour le filtrage des taxes
TAXE_AI_AUTRE = 0							#les autres taxes : Avis d'imposition 
TAXE_AI_ADMINISTRATIF = 1 					#les Taxes pour administratif : Avis d'imposition 
TAXE_AI_DOCUMENT_FINANCIER = 2 				#les Taxes sur les documents financiers : Avis d'imposition (Activité, Transport, ...)

TAXE_BASE_ACTIVITE = 3						#les taxes sur activité (standard/marche) : Note d'imposition

TAXE_ACTIVITE_EXCEPTIONNELLE = 4			#les Taxes sur les activités exceptionnelles : Avis d'imposition
TAXE_VISITE_SITE_TOURISTIQUE = 5			#les Taxes sur les visites des sites touristiques : Avis d'imposition
TAXE_ALLOCATION_ESPACE_PUBLIQUE = 6			#les Taxes sur les Allocation espace publique : Note d'imposition
TAXE_ALLOCATION_PANNEAU_PUBLICITAIRE = 7	#les Taxes sur les panneaux publicitaires : Note d'imposition
TAXE_PUBLICITE_MUR_CLOTURE = 8				#les Taxes sur les murs de publication (affichage) : Note d'impositionv

TAXE_ALLOCATION_PLACE_MARCHE = 9			#Allocation de place dans le marché
TAXE_BATIMENTS_MUNICIPAUX = 10				#Location batiments municipaux

TAXE_IMPOT_FONCIER = 11						#les Taxes sur les impots fonciers Note d'imposition

TAXE_TRANSPORT_ACTIVITE_ = 12				#les Taxes sur les activités des transports rémunérés : Note d'imposition
TAXE_TRANSPORT_DROIT_STATIONNEMENT = 13		#les Taxes sur le droit de stationnement : Note d'imposition
TAXE_TRANSPORT_IMPOT_PROPRIETE = 14		#les Taxes sur les impôts propriété de véhicule : Note d'imposition
TAXE_BETAILS_IMPOT_PROPRIETE = 15			#les Taxes sur les impôts propriétés de gros betails : Note d'imposition

choix_taxe_filter = (
	(TAXE_AI_AUTRE, "Autres Avis d'imposition"), 
	(TAXE_AI_ADMINISTRATIF, "Avis d'impositon - Administratif"),
	(TAXE_AI_DOCUMENT_FINANCIER, "Avis d'impositon - Transport"),
	(TAXE_BASE_ACTIVITE, 'Activite Standard-Marché'), 
	(TAXE_ACTIVITE_EXCEPTIONNELLE, "Avis d'imposition - Activité exceptionnelle"), 
	(TAXE_VISITE_SITE_TOURISTIQUE, "Avis d'imposition - Visite site touristique"), 
	(TAXE_ALLOCATION_ESPACE_PUBLIQUE, 'Allocation Espace publique'), 
	(TAXE_ALLOCATION_PANNEAU_PUBLICITAIRE, 'Allocation panneau publicitaire'), 
	(TAXE_PUBLICITE_MUR_CLOTURE, 'Publicité sur les murs/clôtures'), 
	(TAXE_IMPOT_FONCIER, "Impôts fonciers"),
	(TAXE_ALLOCATION_PLACE_MARCHE, "Allocation de place dans le marché"),
	(TAXE_BATIMENTS_MUNICIPAUX, "Location batiments municipaux"),
	(TAXE_TRANSPORT_ACTIVITE_, 'Activité sur les transports rémunérés'), 
	(TAXE_TRANSPORT_DROIT_STATIONNEMENT, 'Droit de stationnement'), 
	(TAXE_TRANSPORT_IMPOT_PROPRIETE, 'Taxes sur les véhicule de propriété'),
	(TAXE_BETAILS_IMPOT_PROPRIETE, "Taxes sur les gros bétails"), #(EN ATTENTE DE CONCEPTION)
)

"""
-------------- CHOIX DES ENTITY POUR L'AVIS et NOTE D'IMPOSITION ------------
"""
# Identifiant de l'entité 'entity qui est le nom Django-Model : 

ENTITY_ACTIVITE_STANDARD = 1				# BaseActivite (réf: Standard)
ENTITY_ACTIVITE_MARCHE = 2					# BaseActivite (réf: Marché)
ENTITY_ACTIVITE_EXCEPTIONNELLE = 3			# ActiviteExceptionnel (Dans AvisImposition uniquement)
ENTITY_VISITE_SITE_TOURISTIQUE = 4			# VisiteSiteTouristique (Dans AvisImposition uniquement)
ENTITY_ALLOCATION_ESPACE_PUBLIQUE = 5		# AllocationEspacePublique
ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE = 6	# AllocationPanneauPublicitaire
ENTITY_PUBLICITE_MUR_CLOTURE = 7			# PubliciteMurCloture
ENTITY_ALLOCATION_PLACE_MARCHE = 8			# Allocation de Place dans le Marche
ENTITY_BATIMENTS_MUNICIPAUX = 9				# Location batiments municipaux
ENTITY_IMPOT_FONCIER = 10					# Impôt foncier (FoncierExpertise)
ENTITY_VEHICULE_ACTIVITE = 11				# VehiculeActivite
ENTITY_DROIT_STATIONNEMENT = 12				# VehiculeActivite (!!! Important !!!) : Il depend de l'activité
ENTITY_VEHICULE_PROPRIETE = 13				# VehiculeProprietaire
ENTITY_ACTIVITE_STANDARD_DUPLICATA = 14     # StandardDuplicata (Dans AvisImposition uniquement)
ENTITY_ACTIVITE_MARCHE_DUPLICATA = 15       # MarcheDuplicata (Dans AvisImposition uniquement)
ENTITY_VEHICULE_ACTIVITE_DUPLICATA = 16		# VehiculeActiviteDuplicata (Dans AvisImposition uniquement)
ENTITY_VEHICULE_PROPRIETE_DUPLICATA = 17	# VehiculeProprietaireDuplicata (Dans AvisImposition uniquement)

ENTITY_BETAILS_PROPRIETE = 18				# BetailPropriete (EN ATTENTE DE CONCEPTION)

# ENTITY POUR LES DOCUMENTS
ENTITY_ATTESTATION = 19						# attestaion (Dans AvisImposition uniquement) applicable sur tous les testations
ENTITY_ACTE = 20							# acte (Dans AvisImposition uniquement) applicable sur tous les actes


choix_entity_imposition = {
	(ENTITY_ACTIVITE_STANDARD,				'Django-Model:Standard'),
	(ENTITY_ACTIVITE_MARCHE, 				'Django-Model:Marche'),
	(ENTITY_ACTIVITE_EXCEPTIONNELLE, 		'Django-Model:ActiviteExceptionnel'),
	(ENTITY_VISITE_SITE_TOURISTIQUE, 		'Django-Model:VisiteSiteTouristique'),
	(ENTITY_ALLOCATION_ESPACE_PUBLIQUE, 	'Django-Model:AllocationEspacePublique'),
	(ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE,'Django-Model:AllocationPanneauPublicitaire'),
	(ENTITY_PUBLICITE_MUR_CLOTURE, 			'Django-Model:PubliciteMurCloture'),
	(ENTITY_ALLOCATION_PLACE_MARCHE, 		'Django-Model:AllocationPlaceMarche'),
	(ENTITY_BATIMENTS_MUNICIPAUX, 			'Django-Model:Location batiments municipaux'),
	(ENTITY_IMPOT_FONCIER, 					'Django-Model:FoncierParcelle'),
	(ENTITY_VEHICULE_ACTIVITE, 				'Django-Model:VehiculeActivite'),
	(ENTITY_DROIT_STATIONNEMENT, 			'Django-Model:VehiculeActivite'),
	(ENTITY_VEHICULE_PROPRIETE, 			'Django-Model:VehiculeProprietaire'),
	(ENTITY_ACTIVITE_STANDARD_DUPLICATA, 	'Django-Model:BaseActiviteDuplicata'),
	(ENTITY_ACTIVITE_MARCHE_DUPLICATA, 		'Django-Model:FoncierParcelleDuplicata'),
	(ENTITY_VEHICULE_ACTIVITE_DUPLICATA, 	'Django-Model:VehiculeActiviteDuplicata'),
	(ENTITY_VEHICULE_PROPRIETE_DUPLICATA, 	'Django-Model:VehiculeProprietaireDuplicata'),
	(ENTITY_BETAILS_PROPRIETE, 				'Django-Model:BetailsPropriete'),
	(ENTITY_ATTESTATION, 				    'Django-Model:Attestation'),
	(ENTITY_ACTE, 				            'Django-Model:Acte'),
}

"""
-------------- TRANSPORT TYPE DE ROUE ------------
"""
SANS_ROUE = 0
DEUX_TROIS_ROUE = 1 
QUATRE_ROUE = 2

choix_type_roue = ( 
	(SANS_ROUE, 'pas de roue'), 		# Bateau ???
	(DEUX_TROIS_ROUE, '2 ou 3 roues'), 	# Moto - Bajaj - Vélo // Trasport rémunéré optionnel 
	(QUATRE_ROUE, '4 roues'), 			# Camion - Voiture - Bus - ... // Ils sont obligatoirement rémunéré
)

"""
-------------- PARAMETRAGE NUMERO AUTO, modele 'mod_chrono' ------------
"""
CHRONO_PERSONNE_PHYSIQUE = '180' 			# 'Personne Physique'
CHRONO_PERSONNE_MORALE = '181' 				# 'Personne Morale'

CHRONO_ACTIVITE_STANDARD =  'AS' 			# 'Activité Standard'
CHRONO_ACTIVITE_MARCHE = 'AM' 				# 'Activité dans le marché'

CHRONO_ACTIVITE_EXCEPTIONNELLE = 'AE' 		# 'Activité Exceptionnelle'
CHRONO_VISITE_SITE_TOURISTIQUE =  'VST' 	# 'Visite des Sites touristique'

CHRONO_ALLOCATION_PANNEAU_PUBLICITAIRE = 'APP' # 'Allocation des panneaux publicitaires'
CHRONO_PUBLICITE_MUR_CLOTURE = 'PMC' 		# 'Publicité sur les clôtures et murs

CHRONO_PARCELLE_PRIVE =  'PPV' 				# 'Parcelle Privée'
CHRONO_PARCELLE_PUBLIQUE =  'PPQ' 			# 'Espace ou Parcelle Publique'
CHRONO_ALLOCATION_ESPACE_PUBLIQUE = 'AEP' 	# 'Allocation espace/parcelle publique'

CHRONO_ACTIVITE_TRANSPORT =  'AT' 			# 'Activité de transport'
CHRONO_DROIT_STATIONNEMENT = 'DS' 			# 'Carte de Stationnement'
CHRONO_CARTE_PROPRIETE_VEHICULE = 'CPV' 	# 'Carte de Propriété de Véhicule'

CHRONO_CARTE_PROPRIETE_BETAILS = 'CPB' 		# "Carte de Propriété de Bétails"

CHRONO_AVIS_IMPOSITION =  'AI' 				# 'Avis d'imposition'
CHRONO_NOTE_IMPOSITION =  'NI'				# 'Note d'imposition'
CHRONO_ATTESTATION_NON_REDEVABILITE =  'ANR'	# 'Attestion de non_redevabilite'

"""
-------------- PARAMETRAGE DES PERIODES ------------
"""

# ----- CATEGORIE DE PERIODE -------
MENSUELLE = 1
TRIMSTRIELLE = 2
SEMESTRIELLE = 3
ANNUELLE = 4

choix_periode_categories = {
	(0, 'Autre'),
	(MENSUELLE, 'Mensuelle'),
	(TRIMSTRIELLE, 'Trimestrielle'),
	(SEMESTRIELLE, 'Semestrielle'),
	(ANNUELLE, 'Annuelle'),
}

# ----- ELEMENTS DE PERIODE -------

JANVIER = 1
FEVRIER = 2
MARS = 3
AVRIL = 4
MAI = 5
JUIN = 6
JUILLET = 7
AOUT = 8
SEPTEMBRE = 9
OCTOBRE = 10
NOVEMBRE = 11
DECEMBRE = 12

PREMIER_TRIMESTRE = 13
DEUXIEME_TRIMESTRE = 14
TROISIEME_TRIMESTRE = 15
QUATRIEME_TRIMESTRE = 16

PREMIER_SEMESTRE = 17
DEUXIEME_SEMESTRE = 18

ANNEE = 19

choix_periode_elements = {
	(JANVIER, 'JANVIER'),
	(FEVRIER, 'FEVRIER'),
	(MARS, 'MARS'),
	(AVRIL, 'AVRIL'),
	(MAI, 'MAI'),
	(JUIN, 'JUIN'),
	(JUILLET, 'JUILLET'),
	(AOUT, 'AOUT'),
	(SEPTEMBRE, 'SEPTEMBRE'),
	(OCTOBRE, 'OCTOBRE'),
	(NOVEMBRE, 'NOVEMBRE'),
	(DECEMBRE, 'DECEMBRE'),
	(PREMIER_TRIMESTRE, '1er TRIMESTRE'),
	(DEUXIEME_TRIMESTRE, '2e TRIMESTRE'),
	(TROISIEME_TRIMESTRE, '3e TRIMESTRE'),
	(QUATRIEME_TRIMESTRE, '4e TRIMESTRE'),
	(PREMIER_SEMESTRE, '1er SEMESTRE'),
	(DEUXIEME_SEMESTRE, '2e SEMESTRE'),
	(ANNEE, 'ANNEE'),
}

"""
-------------- CHOIX POUR USAGE DE LA PARCELLE PUBLIQUE ----------------
"""
USAGE_NEANT =0
USAGE_ACTIVITE =1
USAGE_PANNEAU =2

choix_usage_parcelle_public = (
	(USAGE_NEANT, 'Disponible'), 
	(USAGE_ACTIVITE, 'Activité'), 
	(USAGE_PANNEAU, 'Panneau'),
)

"""
------------ CHOIX DES ENTITE POUR LA GESTION DES PENALITE - MODULE --------------
"""
PENALITE_ACTIVITE_STANDARD = 1
PENALITE_ACTIVITE_MARCHE = 2
PENALITE_ALLOCATION_ESPACE_PUBLIQUE = 3
PENALITE_ALLOCATION_PANNEAU_PUBLICITAIRE = 4
PENALITE_PUBLICITE_MUR_CLOTURE = 5
PENALITE_VEHICULE_ACTIVITE = 6
PENALITE_DROIT_STATIONNEMENT = 7
PENALITE_VEHICULE_PROPRIETE = 8
PENALITE_IMPOT_FONCIER = 9

choix_penalite_module = {
	(PENALITE_ACTIVITE_STANDARD,				'Penalité Activité Standard'),
	(PENALITE_ACTIVITE_MARCHE, 					'Penalité Marché'),
	(PENALITE_ALLOCATION_ESPACE_PUBLIQUE, 		'Penalité Allocation Espace Publique'),
	(PENALITE_ALLOCATION_PANNEAU_PUBLICITAIRE,	'Penalité Allocation Panneau Publicitaire'),
	(PENALITE_PUBLICITE_MUR_CLOTURE, 			'Penalité Publicité Mur et Clôture'),
	(PENALITE_VEHICULE_ACTIVITE, 				'Penalité Véhicule Activité'),
	(PENALITE_DROIT_STATIONNEMENT, 				'Penalité Véhicule Stationnement'),
	(PENALITE_VEHICULE_PROPRIETE, 				'Penalité Véhicule Propriétaire'),
	(PENALITE_IMPOT_FONCIER, 					'Penalité Impôt Foncier'),
}

"""
------------ CHOIX DES ENTITE POUR LA GESTION DES PENALITE - PERIODE --------------
"""
PENALITE_PERIODE_ANT = 1	# Periode anticipe
PENALITE_PERIODE_PE = 2		# Periode ecoulee

choix_penalite_periode = {
	(PENALITE_PERIODE_ANT, 'Anticipé'),
	(PENALITE_PERIODE_PE, 'Ecoulée'),
}