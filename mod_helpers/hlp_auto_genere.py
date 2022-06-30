from django.shortcuts import get_object_or_404
from mod_foncier.submodels.model_foncier_expertise import FoncierExpertise
from mod_foncier.submodels.model_foncier_parcelle import FoncierParcelle
from mod_foncier.submodels.model_foncier_caracteristique import FoncierCaracteristique
from mod_parametrage.models import Accroissement,Penalite
from mod_finance.models import NoteImposition
from mod_activite.models import *
from mod_transport.models import *
from mod_parametrage.models import *
from mod_parametrage.enums import *
import datetime 
from datetime import date

from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone

from django.utils.timezone import make_aware

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_operations import OperationsHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.hlp_accroissement import AccroissementHelpers
from mod_helpers.hlp_penalite import *
from mod_helpers.models import Chrono
from mod_foncier.templatetags.foncier_filter import get_montant_note
from django.contrib.humanize.templatetags.humanize import intcomma


def auto_genere_expertise(expertise=0):
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	currentYear = datetime.datetime.now().year
	user = User.objects.first()
	if expertise != 0:
		obj = get_object_or_404(FoncierExpertise, pk=expertise)
		check_next_year = obj.annee + 1
		expert = FoncierExpertise.objects.filter(annee=check_next_year, parcelle_id=obj.parcelle_id)
		if not expert:
			print(expert.annee,'annee ******************************************************************************************')
			if check_next_year <= currentYear:
				diff_year = currentYear - obj.annee
				montant_non_bati = round(obj.superficie_non_batie * obj.impot_non_batie.impot)
				montant_construction = 0
				accroissement = 0
				lst_car = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
				for car in lst_car:
					montant_construction += round(car.superficie_batie * car.impot_batie.impot)
				taux_accroisement = obj.has_accroissement
				somme_taxe = montant_non_bati + montant_construction
				if taux_accroisement > 0:
					accroissement = (somme_taxe * taux_accroisement) / 100

				if diff_year > 0:
					for x in range(diff_year):
						try:
							if check_next_year + x != currentYear:
								dossier = obj.dossier_expertise
								if not dossier:
									check_previous_year = obj.annee - 1
									get_previous_exp = FoncierExpertise.objects.filter(annee=check_previous_year,parcelle_id=obj.parcelle_id)
									for gpe in get_previous_exp:
										dossier = gpe.dossier_expertise
										exp_doss = get_object_or_404(FoncierExpertise, pk=expertise)
										exp_doss.dossier_expertise = dossier
										exp_doss.save()
							else:
								dossier = None

							experti = FoncierExpertise(
								annee=check_next_year + x,
								dossier_expertise=dossier,
								superficie_non_batie=obj.superficie_non_batie,
								date_validate=date_validate,
								impot_non_batie_id=obj.impot_non_batie_id,
								accroissement_montant=accroissement,
								accroissement_taux=taux_accroisement,
								montant_tb=montant_construction,
								montant_tnb=montant_non_bati,
								parcelle_id=obj.parcelle_id,
								user_create_id=user.id,
								date_declaration=dateTimeNow)
							experti.save()
							# newrow = FoncierExpertise.objects.all().order_by('-id')[:1]
							year = check_next_year + x
							newrow = FoncierExpertise.objects.filter(annee=year,parcelle_id=obj.parcelle_id)
							for nwr in newrow:
								caracteur = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
								for cara in caracteur:
									caract = FoncierCaracteristique(
										superficie_batie=cara.superficie_batie,
										expertise_id=nwr.id,
										impot_batie_id=cara.impot_batie_id)
									caract.save()
						except:
							pass
				else:
					try:
						experti = FoncierExpertise(
							annee=check_next_year,
							superficie_non_batie=obj.superficie_non_batie,
							date_create=dateTimeNow,
							impot_non_batie_id=obj.impot_non_batie_id,
							parcelle_id=obj.parcelle_id,
							user_create_id=1,
							date_declaration=dateTimeNow)
						experti.save()
						newrow = FoncierExpertise.objects.filter(annee=check_next_year, parcelle_id=obj.parcelle_id)
						for nwr in newrow:
							caracteur = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
							for cara in caracteur:
								caract = FoncierCaracteristique(
									superficie_batie=cara.superficie_batie,
									expertise_id=nwr.id,
									impot_batie_id=cara.impot_batie_id)
								caract.save()
					except:
						pass

def update_expertise(expertise_id):
	obj = get_object_or_404(FoncierExpertise, pk=expertise_id)
	montant_tnb = round(obj.superficie_non_batie * obj.impot_non_batie.impot)
	montant_tb = 0
	lst_car = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
	for car in lst_car:
		montant_tb += round(car.superficie_batie * car.impot_batie.impot)
	obj.montant_tnb = montant_tnb
	obj.montant_tb = montant_tb
	print(montant_tnb,montant_tb,'montant_tnb et montant_tb *****************************************************')
	obj.save()

def update_expert():
	expertise = FoncierExpertise.objects.all()
	for expr in expertise:
		if expr.impot_non_batie_id != 9 and expr.superficie_non_batie != 0 and expr.montant_tnb == 0 and expr.montant_tb == 0:
			print(expr.id,expr.annee)
			update_expertise(expr.id)

###########################  debut ############################################
# generation automatique des expertise et les note d'imposition pour les années imposer precedemment
def auto_genere_prevue_expertise(expertise_id):
	dateTimeNow = datetime.datetime.now()
	obj = get_object_or_404(FoncierExpertise, pk=expertise_id)
	genere_note_impot_foncier(expertise_id)
	if int(obj.nbr_anne) > 1:
		for x in range(int(obj.nbr_anne) - 1):
			get_anne = int(obj.annee) - 1 - x
			try:
				with transaction.atomic():
					solde_batie = 0
					solde = 0
					accroissement_taux = 0
					datecreate = str(dateTimeNow)
					date_create = tuple([int(x) for x in datecreate[:10].split('-')])
					date_to_set = date(date_create[0], date_create[1], date_create[2])
					for acc in Accroissement.objects.filter(is_taux_annee_ecoulee=True):
						accroissement_taux = acc.taux

					check_caracteur = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
					for cara in check_caracteur:
						solde_batie = cara.superficie_batie * cara.impot_batie.impot

					montant = (obj.superficie_non_batie * obj.impot_non_batie.impot) + solde_batie
					if montant > 0 and accroissement_taux > 0:
						solde = round((montant * accroissement_taux)/100)


					experti = FoncierExpertise(
						annee=get_anne,
						dossier_expertise=obj.dossier_expertise,
						superficie_non_batie=obj.superficie_non_batie,
						date_create=dateTimeNow,
						impot_non_batie_id=obj.impot_non_batie_id,
						parcelle_id=obj.parcelle_id,
						user_create_id=obj.user_create_id,
						date_declaration=date_to_set,
						accroissement_montant=solde,
						accroissement_taux=accroissement_taux,
						montant_tb=obj.montant_tb,
						montant_tnb=obj.montant_tnb,
					)
					experti.save()

					newrow = FoncierExpertise.objects.filter(annee=get_anne,parcelle_id=obj.parcelle_id)

					for nwr in newrow:
						caracteur = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
						for cara in caracteur:
							caract = FoncierCaracteristique(
								superficie_batie=cara.superficie_batie,
								expertise_id=nwr.id,
								impot_batie_id=cara.impot_batie_id)
							caract.save()
						genere_note_impot_foncier_prevue_year(nwr.id)
			except :
				pass

def genere_note_impot_foncier_prevue_year(expertise_id):
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	if expertise_id:
		# Récuperer l'identifiant de la parcelle
		obj = get_object_or_404(FoncierExpertise, pk=expertise_id)
		if obj:
			montant_non_bati = obj.superficie_non_batie * obj.impot_non_batie.impot
			# Traitement des contructions (terrain bâti)
			montant_construction = 0
			lst_car = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
			for car in lst_car:
				montant_construction += car.superficie_batie * car.impot_batie.impot

			somme_taxe = montant_non_bati + montant_construction
			# 2 - Générer le nouveau numéro chrono
			new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
			obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
			obj_chrono.last_chrono = new_chrono
			# Calculer le montant de l'impot (terrain non bati et construction)
			taux_accroisement = 0
			accroissement = 0
			taux_penalite = 0
			penalite = 0

			for acc in Accroissement.objects.filter(is_taux_annee_ecoulee=True):
				taux_accroisement = acc.taux

			if somme_taxe > 0 and taux_accroisement > 0:
				accroissement = (somme_taxe * taux_accroisement)/100

			MONTANT_DU = somme_taxe + accroissement

			if somme_taxe > 0:
				obj_chrono.save()
				# 3 - Créer l'objet Note d'imposition
				ni = NoteImposition()

				# Référence de la note d'imposition (chronologique)
				ni.reference = new_chrono

				# Contribuable qui se trouve sur l'allocation de la place dans le marché (contrat préalable) IMPORTANT !!!
				ni.contribuable = obj.parcelle.contribuable

				# Entity Modèle : 'BaseActivite'
				ni.entity = ENTITY_IMPOT_FONCIER

				# Identifiant de l'entity : 'FoncierExpertise'
				ni.entity_id = obj.id

				# Période de paiement
				ni.periode = PeriodeHelpers.getCurrentPeriode(obj.parcelle.taxe.periode_type)

				# Année de paiement (Très important pour la gestion des périodes)
				ni.annee = obj.annee

				# Taxe sur activité, Objet taxe (Type : Note d'imposition)
				ni.taxe = obj.parcelle.taxe
				# print("Impôt foncier de la parcelle n°" + obj.parcelle.numero_parcelle + ".Avec un taux d'accroissement de 50%, pour un montant de " + accroissement + " Bif sur un montant de " + MONTANT_DU + "Bif")
				# Libellé de la note (Par défaut = libellé de la taxe)
				ni.libelle = "Impôt foncier de la parcelle n° " + str(obj.parcelle.numero_parcelle) + ".Avec un taux d'accroissement de " + str(taux_accroisement) + "%, pour un montant de " + str(accroissement) + " Bif sur un montant de " + str(MONTANT_DU) + "Bif"

				# Montant total de la taxe à payer (parametre taxe le terrain non batit et construction) avec accroisment
				ni.taxe_montant = round(MONTANT_DU)

				# Traçabilité (date_create est créée depuis le model)
				ni.date_update = dateTimeNow
				ni.date_validate = dateTimeNow

				ni.user_create_id = obj.user_create_id
				ni.user_update_id = obj.user_create_id
				ni.user_validate_id = obj.user_create_id
				ni.user_penalite_id = obj.user_create_id
				# Sauvegarder la note d'imposition (taxe sur l'allocation)
				ni.save()
				# dateTimeNow = datetime.datetime.now(tz=timezone.utc)
				# obj.update(date_ecriture=dateTimeNow,user_ecriture=user)
				obj.date_validate = dateTimeNow
				obj.user_validate_id = obj.user_create_id
				obj.date_ecriture = dateTimeNow
				obj.user_ecriture_id = obj.user_create_id
				obj.save()

				obj.accroissement_taux = taux_accroisement
				obj.accroissement_montant = accroissement
				obj.penalite_taux = taux_penalite
				obj.penalite_montant = penalite

				obj.save()
###########################  fin   ############################################
def auto_genere_expertise_and_note():
	dateTimeNow = datetime.datetime.now()
	user = User.objects.first()
	expertise = FoncierExpertise.objects.all().order_by('-id')
	for exper in expertise:
		if not exper.dossier_expertise:
			obj = get_object_or_404(FoncierExpertise, pk=exper.id)
			if obj:
				check_previous_year = obj.annee - 1
				previous_note = FoncierExpertise.objects.get(annee=check_previous_year)
				obj.dossier_expertise = previous_note.dossier_expertise
				obj.date_validate = dateTimeNow
				obj.user_validate = user
				obj.save()
				genere_note_impot_foncier(obj.id)

# creation des note d'imposition annuel pour d'autre activite
def create_note_annuel():
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	user = User.objects.first()
	note_imposition = NoteImposition.objects.all()
	for note in note_imposition:
		obj = get_object_or_404(NoteImposition, pk=note.id)
		check_next_year = obj.annee + 1
		exist_not = NoteImposition.objects.filter(entity=obj.entity,entity_id=obj.entity_id,annee=check_next_year,contribuable_id=obj.contribuable_id)
		if not exist_not and check_next_year <= currentYear:
			diff_year = currentYear - obj.annee
			if diff_year > 0:
				for x in range(diff_year):
					# ceartion de note d'imposition ACTIVITE STANDARD
					############################################################################
					if obj.entity == 1:
						activite = BaseActivite.objects.get(id=obj.entity_id)
						if activite.actif:
							try:
								if obj.taxe.tarif > 0:
									new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
									obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
									obj_chrono.last_chrono = new_chrono
									obj_chrono.save()

									get_annee = check_next_year + x
									ni = NoteImposition()
									ni.reference = new_chrono   # Référence de la note d'imposition (chronologique)
									ni.contribuable = obj.contribuable   # Contribuable qui se trouve sur l'allocation de la place dans le marché (contrat préalable) IMPORTANT !!!
									ni.entity = ENTITY_ACTIVITE_STANDARD   # Entity Modèle : 'BaseActivite'
									ni.entity_id = obj.id   # Identifiant de l'entity : 'Srandard'
									ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)   # Période de paiement
									ni.annee = check_next_year + x # Année de paiement (Très important pour la gestion des périodes)
									ni.taxe = obj.taxe  # Taxe sur activité, Objet taxe (Type : Note d'imposition)
									taux_accroisement = AccroissementHelpers.has_accroissement_taxe(get_annee, dateTimeNow) # ACCROISEMENT

									accroissement = 0
									if taux_accroisement > 0:
										accroissement = (obj.taxe.tarif * taux_accroisement) / 100

									MONTANT_DU = obj.taxe.tarif + accroissement  # Montant dû

									if activite.solde_depart > 0:   # Solde de depart
										MONTANT_DU += activite.solde_depart

									ni.taxe_montant = MONTANT_DU # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
									ni.accroissement_taux = taux_accroisement
									ni.accroissement_montant = accroissement

									# Traçabilité (date_create est créée depuis le model)
									ni.date_update = dateTimeNow
									ni.date_validate = dateTimeNow

									ni.user_create = user
									ni.user_update = user
									ni.user_validate = user

									# Sauvegarder la note d'imposition (taxe sur l'allocation)
									ni.save()

									activite.date_ecriture = dateTimeNow
									activite.user_ecriture = user
									activite.save()
							except:
								pass

					# ceartion de note d'imposition ACTIVITE MARCHE
					############################################################################
					if obj.entity == 2:
						activite = BaseActivite.objects.get(id=obj.entity_id)
						if activite.actif:
							try:
								if obj.taxe.tarif > 0:
									OperationsHelpers.execute_action_ecriture(request, activite)
									new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
									obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
									obj_chrono.last_chrono = new_chrono
									obj_chrono.save()

									get_annee = check_next_year + x
									ni = NoteImposition()
									ni.reference = new_chrono  # Référence de la note d'imposition (chronologique)
									ni.contribuable = obj.contribuable  # Contribuable qui se trouve sur l'allocation de la place dans le marché (contrat préalable) IMPORTANT !!!
									ni.entity = ENTITY_ACTIVITE_MARCHE  # Entity Modèle : 'BaseActivite'
									ni.entity_id = obj.id  # Identifiant de l'entity : 'Srandard'
									ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)  # Période de paiement
									ni.annee = check_next_year + x  # Année de paiement (Très important pour la gestion des périodes)
									ni.taxe = obj.taxe  # Taxe sur activité, Objet taxe (Type : Note d'imposition)
									taux_accroisement = AccroissementHelpers.has_accroissement_taxe(get_annee,dateTimeNow)  # ACCROISEMENT

									accroissement = 0
									if taux_accroisement > 0:
										accroissement = (obj.taxe.tarif * taux_accroisement) / 100

									MONTANT_DU = obj.taxe.tarif + accroissement  # Montant dû

									if activite.solde_depart > 0:  # Solde de depart
										MONTANT_DU += activite.solde_depart

									ni.taxe_montant = MONTANT_DU  # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
									ni.accroissement_taux = taux_accroisement
									ni.accroissement_montant = accroissement

									# Traçabilité (date_create est créée depuis le model)
									ni.date_create = dateTimeNow
									ni.date_validate = dateTimeNow

									ni.user_create = user
									ni.user_validate = user

									ni.save()  # Sauvegarder la note d'imposition (taxe sur l'allocation)

									activite.date_ecriture = dateTimeNow
									activite.user_ecriture = user
									activite.save()
							except:
								pass

					# ceartion de note d'imposition ALLOCATION ESPACE PUBLIQUE
					############################################################################
					if obj.entity == 5:
						allocation = AllocationEspacePublique.objects.get(id=obj.entity_id)
						if not allocation.date_fin:
							try:
								if obj.taxe.tarif > 0:
									OperationsHelpers.execute_action_ecriture(request, allocation)
									new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
									obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
									obj_chrono.last_chrono = new_chrono
									obj_chrono.save()

									get_annee = check_next_year + x
									ni = NoteImposition()
									ni.reference = new_chrono  # Référence de la note d'imposition (chronologique)
									ni.contribuable = obj.contribuable  # Contribuable
									ni.entity = ENTITY_ALLOCATION_ESPACE_PUBLIQUE   # Entity Modèle : 'AllocationEspacePublique'
									ni.entity_id = obj.entity_id  # Identifiant de l'entity : 'AllocationEspacePublique'
									ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)  # Période de paiement
									ni.annee = check_next_year + x  # Année de paiement (Très important pour la gestion des périodes)
									ni.taxe = obj.taxe  # Taxe sur activité, Objet taxe (Type : Note d'imposition)
									montant_total = allocation.superficie * obj.taxe.tarif  # Montant total de la taxe à payer (montant par m² x tarif)

									taux_accroisement = AccroissementHelpers.has_accroissement_taxe(get_annee, dateTimeNow) # ACCROISEMENT
									accroissement = 0
									if taux_accroisement > 0:
										accroissement = (montant_total * taux_accroisement) / 100

									MONTANT_DU = montant_total + accroissement
									if allocation.solde_depart > 0:  # Solde de depart
										MONTANT_DU += allocation.solde_depart
									ni.taxe_montant = MONTANT_DU  # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
									ni.accroissement_taux = taux_accroisement
									ni.accroissement_montant = accroissement

									# Traçabilité (date_create est créée depuis le model)
									ni.date_create = dateTimeNow
									ni.date_validate = dateTimeNow

									ni.user_create = user
									ni.user_validate = user
									ni.save()  # Sauvegarder la note d'imposition (taxe sur l'allocation de l'espace)

									allocation.date_ecriture = dateTimeNow
									allocation.user_ecriture = user
									allocation.save()

							except:
								pass

					# ceartion de note d'imposition ALLOCATION PANNEAU PUBLICITAIRE
					############################################################################
					if obj.entity == 6:
						allocation = AllocationPanneauPublicitaire.objects.get(id=obj.entity_id)
						if obj.taxe.tarif > 0:
							if not allocation.date_fin:
								try:
									if obj.taxe.tarif > 0:
										OperationsHelpers.execute_action_ecriture(request, allocation)
										new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
										obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
										obj_chrono.last_chrono = new_chrono
										obj_chrono.save()

										get_annee = check_next_year + x
										ni = NoteImposition()  # 3 - Créer l'objet Note d'imposition
										ni.reference = new_chrono  # Référence de la note d'imposition (chronologique)
										ni.contribuable = obj.contribuable  # Contribuable
										ni.entity = ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE  # Entity Modèle : 'AllocationPanneauPublicitaire'
										ni.entity_id = obj.entity_id  # Identifiant de l'entity : 'AllocationPanneauPublicitaire'
										ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)  # Période de paiement
										ni.annee = check_next_year + x  # Année de paiement (Très important pour la gestion des périodes)
										ni.taxe = obj.taxe  # Taxe sur activité, Objet taxe (Type : Note d'imposition)
										montant_total = allocation.superficie * obj.taxe.tarif  # Montant total de la taxe à payer (montant par m² x tarif)
										taux_accroisement = AccroissementHelpers.has_accroissement_taxe(get_annee, dateTimeNow)   # ACCROISEMENT
										accroissement = 0
										if taux_accroisement > 0:
											accroissement = (montant_total * taux_accroisement) / 100

										MONTANT_DU = montant_total + accroissement
										if allocation.solde_depart > 0:  # Solde de depart
											MONTANT_DU += allocation.solde_depart
										ni.taxe_montant = MONTANT_DU  # Montant total de la taxe à payer (parametre taxe d'allocation panneau publicitaire)
										ni.accroissement_taux = taux_accroisement
										ni.accroissement_montant = accroissement

										# Traçabilité (date_create est créée depuis le model)
										ni.date_create = dateTimeNow
										ni.date_validate = dateTimeNow

										ni.user_create = user
										ni.user_validate = user

										# Sauvegarder la note d'imposition (taxe sur l'allocation de l'espace)
										ni.save()

										allocation.date_ecriture = dateTimeNow
										allocation.user_ecriture = user
										allocation.save()
								except:
									pass

					# ceartion de note d'imposition PUBLICITE MUR LOTURE
					############################################################################
					if obj.entity == 7:
							allocation = PubliciteMurCloture.objects.get(id=obj.entity_id)
							if obj.taxe.tarif > 0:
								if not allocation.date_fin:
									try:
										OperationsHelpers.execute_action_ecriture(request, allocation)
										new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
										obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
										obj_chrono.last_chrono = new_chrono
										obj_chrono.save()

										get_annee = check_next_year + x
										ni = NoteImposition()  # 3 - Créer l'objet Note d'imposition
										ni.reference = new_chrono  # Référence de la note d'imposition (chronologique)
										ni.contribuable = obj.contribuable  # Contribuable
										ni.entity = ENTITY_PUBLICITE_MUR_CLOTURE  # Entity Modèle : 'PubliciteMurCloture'
										ni.entity_id = obj.entity_id  # Identifiant de l'entity : 'PubliciteMurCloture'
										ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)  # Période de paiement
										ni.annee = check_next_year + x  # Année de paiement (Très important pour la gestion des périodes)
										ni.taxe = obj.taxe  # Taxe sur activité, Objet taxe (Type : Note d'imposition)
										montant_total = allocation.superficie * obj.taxe.tarif  # Montant total de la taxe à payer (montant par m² x tarif)
										taux_accroisement = AccroissementHelpers.has_accroissement_taxe(get_annee, dateTimeNow)  # ACCROISEMENT
										accroissement = 0
										if taux_accroisement > 0:
											accroissement = (montant_total * taux_accroisement) / 100

										MONTANT_DU = montant_total + accroissement

										if allocation.solde_depart > 0:  # Solde de depart
											MONTANT_DU += allocation.solde_depart

										ni.taxe_montant = MONTANT_DU  # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
										ni.accroissement_taux = taux_accroisement
										ni.accroissement_montant = accroissement

										# Traçabilité (date_create est créée depuis le model)
										ni.date_create = dateTimeNow
										ni.date_validate = dateTimeNow

										ni.user_create = user
										ni.user_validate = user

										# Sauvegarder la note d'imposition (taxe sur la publicité)
										ni.save()

										allocation.date_ecriture = dateTimeNow
										allocation.user_ecriture = user
										allocation.save()
									except:
										pass

					# ceartion de note d'imposition VEHICULE PROPRIETE
					############################################################################
					# if obj.entity == 13:
					#         vehicule = VehiculeProprietaire.objects.get(id=obj.entity_id)
					#         if vehicule.vehicule.sous_categorie.taxe_proprietaire:
					#             if vehicule.vehicule.actif:
					#                 try:
					#                     # 3 - Créer et Valider la note d'imposition (taxe sur le proriétaire)
					#                     # Générer le nouveau numéro chrono
					#                     new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
					#                     obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
					#                     obj_chrono.last_chrono = new_chrono
					#                     obj_chrono.save()

					#                     ni = NoteImposition()  # Créer l'objet Note d'imposition
					#                     ni.reference = new_chrono  # Référence de la note d'imposition (chronologique)
					#                     ni.contribuable = obj.contribuable  # Contribuable
					#                     ni.entity = ENTITY_VEHICULE_PROPRIETE  # Entity Modèle : 'VehiculeProprietaire'
					#                     ni.entity_id = obj.entity_id  # Identifiant de l'entity : 'VehiculeProprietaire'
					#                     ni.periode = PeriodeHelpers.getCurrentPeriode(vehicule.vehicule.sous_categorie.taxe_proprietaire.periode_type)  # Période de paiement
					#                     ni.annee = check_next_year + x  # Année de paiement (Très important pour la gestion des périodes)
					#                     ni.taxe = vehicule.vehicule.sous_categorie.taxe_proprietaire  # Taxe sur activité, Objet taxe (Type : Note d'imposition)
					#                     ni.taxe_montant = vehicule.vehicule.sous_categorie.taxe_proprietaire.tarif  # Montant total de la taxe à payer (parametre taxe)
					#                     ni.accroissement_taux = taux_accroisement
					#                     ni.accroissement_montant = accroissement

					#                     # Traçabilité (date_create est créée depuis le model)
					#                     ni.date_create = dateTimeNow
					#                     ni.date_validate = dateTimeNow
					#
					#                     ni.user_create = user
					#                     ni.user_validate = user
					#
					#                     # Sauvegarder la note d'imposition (taxe sur le propriétaire)
					#                     ni.save()
					#
					#                     vehicule.date_ecriture = dateTimeNow
					#                     vehicule.user_ecriture = user
					#                     vehicule.save()

					#                 except:
					#                     pass

# mis ajour avec l'annee en cours de tous les note des activites monsuel
def update_note_monsuel_transport():
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	currentMonth = datetime.datetime.now(tz=timezone.utc).month
	activite = VehiculeActivite.objects.all()
	for activ in activite:
		obj = get_object_or_404(VehiculeActivite, pk=activ.id)
		if obj.vehicule.actif:
			note = NoteImposition.objects.filter(entity=12, entity_id=obj.id,annee=currentYear,contribuable_id=obj.contribuable_id).order_by('-annee','-periode_id').first()
			if note :
				# if note.annee < currentYear:
				diff_year = int(currentYear) - int(note.annee)
				if diff_year > 0:
					for x in range(diff_year):
						annee = note.annee + 1 + x
						if x == 0:
							diff_month = 12 - note.periode_id
							if diff_month > 0:
								for y in range(diff_month):
									periode = note.periode_id + y
									note_monsuel_transport(obj, periode, annee)
						else:
							if annee < int(currentYear):
								diff_month = 12
								periode_id = 1
								for y in range(diff_month):
									periode = periode_id + y
									note_monsuel_transport(obj, periode, annee)

							if annee == int(currentYear):
								periode_id = 1
								diff_month = int(currentMonth)
								for y in range(diff_month):
									periode = periode_id + y
									note_monsuel_transport(obj, periode, annee)
				if diff_year == 0:
					periode_id = 1
					diff_month = int(currentMonth)
					for y in range(diff_month):
						periode = periode_id + y
						note_monsuel_transport(obj, periode, currentYear)

# mis ajour avec l'annee en cours de tous les note des taxes monsuel
def update_note_monsuel_taxe():
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	currentMonth = datetime.datetime.now(tz=timezone.utc).month
	allocation = AllocationPlaceMarche.objects.all()
	for alloc in allocation:
		obj = get_object_or_404(AllocationPlaceMarche, pk=alloc.id)
		if not obj.date_fin:
			note = NoteImposition.objects.filter(entity=8, entity_id=obj.id,annee=currentYear,contribuable_id=obj.contribuable_id).order_by('-annee','-periode_id').first()
			if note :
				diff_year = int(currentYear) - int(note.annee)
				if diff_year > 0:
					for x in range(diff_year):
						annee = note.annee + 1 + x
						if x == 0:
							diff_month = 12 - note.periode_id
							if diff_month > 0:
								for y in range(diff_month):
									periode = note.periode_id + y
									note_monsuel_taxe(obj, periode, annee)
						else:
							if annee < int(currentYear):
								diff_month = 12
								periode_id = 1
								for y in range(diff_month):
									periode = periode_id + y
									note_monsuel_taxe(obj, periode, annee)

							if annee == int(currentYear):
								periode_id = 1
								diff_month = int(currentMonth)
								for y in range(diff_month):
									periode = periode_id + y
									note_monsuel_taxe(obj, periode, annee)

				if diff_year == 0:
					periode_id = 1
					diff_month = int(currentMonth)
					for y in range(diff_month):
						periode = periode_id + y
						note_monsuel_taxe(obj, periode, currentYear)

def note_monsuel_transport(obj,periode=0,annee=0):
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	currentMonth = datetime.datetime.now(tz=timezone.utc).month
	user = User.objects.first()
	if not obj.vehicule.compte_propre:
		if obj.vehicule.sous_categorie.taxe_activite.tarif > 0:
			if obj.vehicule.actif:
				print(obj,'****************************************')
				try:
					new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
					obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
					obj_chrono.last_chrono = new_chrono
					obj_chrono.save()

					ni = NoteImposition()  # Créer l'objet Note d'imposition pour l'activité de transport
					ni.reference = new_chrono  # Référence de la note d'imposition (chronologique)
					ni.contribuable = obj.contribuable  # Contribuable
					ni.entity = ENTITY_DROIT_STATIONNEMENT  # Entity Modèle : 'VehiculeProprietaire'
					ni.entity_id = obj.id  # Identifiant de l'entity : 'VehiculeActivite'
					if periode == 0:
						periode = currentMonth  #PeriodeHelpers.getCurrentPeriode(obj.vehicule.sous_categorie.taxe_activite.periode_type)  # Si période multiple (soit : trimestriel, ou annuel), alors localiser la période en cours
					ni.periode_id = periode
					if annee == 0:
						annee = currentYear
					ni.annee = annee  # Année de paiement (Très important pour la gestion des périodes)
					ni.taxe = obj.vehicule.sous_categorie.taxe_activite  # Taxe sur activité, Objet taxe (Type : Note d'imposition)
					MONTANT_DU = obj.vehicule.sous_categorie.taxe_activite.tarif  # Montant dû
					if obj.solde_depart > 0:  # Solde de depart
						MONTANT_DU += obj.solde_depart
					ni.taxe_montant = MONTANT_DU  # Montant total de la taxe à payer (parametre taxe)

					ni.date_create = dateTimeNow
					ni.date_validate = dateTimeNow
					ni.user_create = user
					ni.user_validate = user
					ni.save()

					obj.date_ecriture = dateTimeNow
					obj.user_ecriture = user
					obj.save()
				except:
					pass

def note_monsuel_taxe(obj,periode=0,annee=0):
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	user = User.objects.first()
	if obj.droit_place_marche.cout_place > 0:
		try:
			# Générer le nouveau numéro chrono
			new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
			obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
			obj_chrono.last_chrono = new_chrono
			obj_chrono.save()

			ni = NoteImposition() # 3 - Créer l'objet Note d'imposition
			ni.reference = new_chrono # Référence de la note d'imposition (chronologique)
			ni.contribuable = obj.contribuable # Contribuable
			ni.entity = ENTITY_ALLOCATION_PLACE_MARCHE # Entity Modèle : 'AllocationPlaceMarche'
			ni.entity_id = obj.entity_id # Identifiant de l'entity : 'AllocationPlaceMarche'
			if periode == 0:
				ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)
			else:
				ni.periode_id = periode # Période de paiement
			if annee == 0:
				annee = currentYear
			ni.annee = annee
			ni.taxe = obj.taxe # Taxe sur activité, Objet taxe (Type : Note d'imposition)
			MONTANT_DU = obj.droit_place_marche.cout_place # Montant dû
			if obj.caution_montant > 0: # si CAUTION n'est pas encore payee
				MONTANT_DU += obj.caution_montant
				ni.libelle += '. Avec une caution de ' + str(obj.caution_nombre_mois) + ' mois pour un montant de ' + str(intcomma(obj.caution_montant)) + 'Bif.'
			if obj.solde_depart > 0:  # Solde de depart
				MONTANT_DU += obj.solde_depart
			ni.taxe_montant = MONTANT_DU  # Montant total de la taxe à payer (parametre taxe dans DroitPlaceMarche)
			ni.date_create = dateTimeNow  # Traçabilité (date_create est créée depuis le model)
			ni.date_validate = dateTimeNow

			ni.user_create = user
			ni.user_validate = user

			# Sauvegarder la note d'imposition (taxe sur l'allocation de la place)
			ni.save()

			obj.date_ecriture = dateTimeNow
			obj.user_ecriture = user
			obj.save()
		except:
			pass

# mis ajour avec l'annee en cours de tous les note des activites trimestriel
def upgrad_note_trimetriel_transport():
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	currentMonth = datetime.datetime.now(tz=timezone.utc).month
	activite = VehiculeActivite.objects.all()

	for activ in activite:
		obj = get_object_or_404(VehiculeActivite, pk=activ.id)
		if obj.vehicule.actif:
			note = NoteImposition.objects.filter(entity=11, entity_id=obj.id, annee=currentYear, contribuable_id=obj.contribuable_id).order_by('-annee','-periode_id').first()
			if note:
				if note.annee == currentYear:
					diff_year = int(currentYear) - int(note.annee)
					if diff_year > 0:
						if note.periode_id < 19:
							for x in range(diff_year):
								annee = note.annee + 1 + x
								if x == 0:
									if note.periode_id == 13:
										for y in range(3):
											periode_id = 14
											periode = periode_id + y
											activite_to_update(obj,periode,annee)
									if note.periode_id == 14:
										for y in range(2):
											periode_id = 15
											periode = periode_id + y
											activite_to_update(obj,periode,annee)
									if note.periode_id == 14:
										for y in range(1):
											periode_id = 16
											periode = periode_id + y
											activite_to_update(obj,periode,annee)
								else:
									if annee < currentYear:
										for y in range(4):
											periode_id = 13
											periode = periode_id + y
											activite_to_update(obj,periode,annee)

									if annee == currentYear:
										periode_id = 13
										if int(currentMonth) < 4:
											for y in range(1):
												periode = periode_id + y
												activite_to_update(obj, periode, annee)

										if 3 < int(currentMonth) < 7:
											for y in range(2):
												periode = periode_id + y
												activite_to_update(obj, periode, annee)

										if 6 < int(currentMonth) < 10:
											for y in range(3):
												periode = periode_id + y
												activite_to_update(obj, periode, annee)

										if 9 < int(currentMonth) < 13:
											for y in range(4):
												periode = periode_id + y
												activite_to_update(obj, periode, annee)

						if note.periode_id == 19:
							for x in range(diff_year):
								annee = note.annee + 1 + x
								activite_to_update(obj, 0, annee)
					if diff_year == 0:
						print(note, note.annee, note.periode_id)
						if note.periode_id < 19:
							periode_id = 13
							if int(currentMonth) < 4:
								for y in range(1):
									periode = periode_id + y
									activite_to_update(obj, periode, 0)

							if 3 < int(currentMonth) < 7:
								for y in range(2):
									periode = periode_id + y
									activite_to_update(obj, periode, 0)

							if 6 < int(currentMonth) < 10:
								for y in range(3):
									periode = periode_id + y
									activite_to_update(obj, periode, 0)

							if 9 < int(currentMonth) < 13:
								for y in range(4):
									periode = periode_id + y
									activite_to_update(obj, periode, 0)
						if note.periode_id == 19:
							activite_to_update(obj, 0, 0)

def activite_to_update(obdj,periode=0,annee=0):
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	user = User.objects.first()
	if not obj.vehicule.compte_propre:
		if obj.vehicule.sous_categorie.taxe_activite.tarif > 0:
			try:
				new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
				obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
				obj_chrono.last_chrono = new_chrono
				obj_chrono.save()

				ni = NoteImposition()  # Créer l'objet Note d'imposition pour l'activité de transport
				ni.reference = new_chrono  # Référence de la note d'imposition (chronologique)
				ni.contribuable = obj.contribuable  # Contribuable
				ni.entity = ENTITY_VEHICULE_ACTIVITE  # Entity Modèle : 'VehiculeProprietaire'
				ni.entity_id = obj.id  # Identifiant de l'entity : 'VehiculeActivite'
				if periode == 0:
					periode = PeriodeHelpers.getCurrentPeriode(obj.vehicule.sous_categorie.taxe_activite.periode_type)  # Si période multiple (soit : trimestriel, ou annuel), alors localiser la période en cours
					ni.periode = periode
				else:
					ni.periode_id = periode
				if annee == 0:
					annee = currentYear
				ni.annee = annee  # Année de paiement (Très important pour la gestion des périodes)
				ni.taxe = obj.vehicule.sous_categorie.taxe_activite  # Taxe sur activité, Objet taxe (Type : Note d'imposition)
				MONTANT_DU = obj.vehicule.sous_categorie.taxe_activite.tarif  # Montant dû
				if obj.solde_depart > 0:  # Solde de depart
					MONTANT_DU += obj.solde_depart
				ni.taxe_montant = MONTANT_DU  # Montant total de la taxe à payer (parametre taxe)

				ni.date_create = dateTimeNow
				ni.date_validate = dateTimeNow
				ni.user_create = user
				ni.user_validate = user
				ni.save()

				obj.date_ecriture = dateTimeNow
				obj.user_ecriture = user
				obj.save()
			except:
				pass

# creation des note de chaque trimestre de l'annee encour
def create_note_trimetriel():
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	user = User.objects.first()
	activite = VehiculeActivite.objects.all()
	for activ in activite:
		obj = get_object_or_404(VehiculeActivite, pk=activ.id)
		if obj.vehicule.actif:
			exist_not = NoteImposition.objects.filter(entity=11, entity_id=obj.id, annee=currentYear, contribuable_id=obj.contribuable_id).order_by('-annee','-periode_id').first()
			for note in exist_not:
				if not obj.vehicule.compte_propre:
					if obj.vehicule.sous_categorie.taxe_activite.tarif > 0:
						try:
							new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
							obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
							obj_chrono.last_chrono = new_chrono

							ni = NoteImposition()   # Créer l'objet Note d'imposition pour l'activité de transport
							ni.reference = new_chrono   # Référence de la note d'imposition (chronologique)
							ni.contribuable = obj.contribuable   # Contribuable
							ni.entity = ENTITY_VEHICULE_ACTIVITE  # Entity Modèle : 'VehiculeProprietaire'
							ni.entity_id = obj.entity_id  # Identifiant de l'entity : 'VehiculeActivite'
							ni.periode = PeriodeHelpers.getCurrentPeriode(obj.vehicule.sous_categorie.taxe_activite.periode_type) # Si période multiple (soit : trimestriel, ou annuel), alors localiser la période en cours
							ni.annee = currentYear   # Année de paiement (Très important pour la gestion des périodes)
							ni.taxe = obj.vehicule.sous_categorie.taxe_activite   # Taxe sur activité, Objet taxe (Type : Note d'imposition)
							MONTANT_DU = obj.vehicule.sous_categorie.taxe_activite.tarif  # Montant dû
							if obj.solde_depart > 0:  # Solde de depart
								MONTANT_DU += obj.solde_depart
							ni.taxe_montant = MONTANT_DU  # Montant total de la taxe à payer (parametre taxe)
							ni.date_create = dateTimeNow
							ni.date_validate = dateTimeNow
							ni.user_create = user
							ni.user_validate = user

							obj.date_ecriture = dateTimeNow
							obj.user_ecriture = user

							if note.annee < currentYear and note.periode.periode_type_id == 4:
								obj_chrono.save()
								ni.save()
								obj.save()

							if note.periode.periode_type_id == 2:
								obj_chrono.save()
								ni.save()
								obj.save()
						except:
							pass

# creation des note de chaque mois de l'annee encour
def create_note_monsuel():
	# transport VehiculeActivite entity 12
	currentYear = datetime.datetime.now(tz=timezone.utc).year
	activite = VehiculeActivite.objects.all()
	for activ in activite:
		note = NoteImposition.objects.filter(entity=12, entity_id=activ.id, annee=currentYear,contribuable_id=activ.contribuable_id).order_by('-annee','-periode_id').first()
		if note:
			if note.annee == currentYear:
				obj = get_object_or_404(VehiculeActivite, pk=activ.id)
				note_monsuel_transport(obj)

	# AllocationPlaceMarche entity 8
	# allocation = AllocationPlaceMarche.objects.all()
	# for alloc in allocation:
	#     obj = get_object_or_404(AllocationPlaceMarche, pk=alloc.id)
	#     note_monsuel_taxe(obj)

def genere_note_impot_foncier(expertiseid=0):
	user = User.objects.first()
	currentYear = datetime.datetime.now().year
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	if expertiseid != 0:
		# Récuperer l'identifiant de la parcelle
		obj = get_object_or_404(FoncierExpertise, pk=expertiseid)
		# if obj.annee < currentYear:
		if obj:
			montant_non_bati = round(obj.superficie_non_batie * obj.impot_non_batie.impot)
			# Traitement des contructions (terrain bâti)
			montant_construction = 0
			lst_car = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
			
			for car in lst_car:
				montant_construction += round(car.superficie_batie * car.impot_batie.impot)
				

			somme_taxe = montant_non_bati + montant_construction
			check_note = NoteImposition.objects.filter(entity=10, entity_id=obj.id, annee=currentYear)
			if not check_note:
				print(somme_taxe,'get function ok ******************************************')
				# ---------------------------------------------------------------------
				# 2 - Générer le nouveau numéro chrono
				new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
				obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
				obj_chrono.last_chrono = new_chrono
				# Calculer le montant de l'impot (terrain non bati et construction)
				taux_accroisement = 0
				MONTANT_DU = 0
				accroissement = 0
				if obj.annee < currentYear:
					acc = Accroissement.objects.get(is_taux_annee_ecoulee=True)
					taux_accroisement = acc.taux

				else:
					taux_accroisement = obj.has_accroissement

				# Si accroissement existe
				if somme_taxe > 0 and taux_accroisement > 0:
					accroissement = (somme_taxe * taux_accroisement) / 100

				print(taux_accroisement)


				MONTANT_DU = somme_taxe + accroissement 
				if somme_taxe > 0:
					print('note creted *************************************************************')
					obj_chrono.save()
					# 3 - Créer l'objet Note d'imposition
					ni = NoteImposition()

					# Référence de la note d'imposition (chronologique)
					ni.reference = new_chrono

					# Contribuable qui se trouve sur l'allocation de la place dans le marché (contrat préalable) IMPORTANT !!!
					ni.contribuable = obj.parcelle.contribuable

					# Entity Modèle : 'BaseActivite'
					ni.entity = ENTITY_IMPOT_FONCIER

					# Identifiant de l'entity : 'FoncierExpertise'
					ni.entity_id = obj.id

					# Période de paiement
					ni.periode = PeriodeHelpers.getCurrentPeriode(obj.parcelle.taxe.periode_type)

					# Année de paiement (Très important pour la gestion des périodes)
					ni.annee = obj.annee

					# Taxe sur activité, Objet taxe (Type : Note d'imposition)
					ni.taxe = obj.parcelle.taxe

					# Libellé de la note (Par défaut = libellé de la taxe)
					ni.libelle = 'Impôt foncier de la parcelle n°' + obj.parcelle.numero_parcelle

					if taux_accroisement > 0:
						ni.libelle += ". Avec un taux d'accroissement de " + str(
							taux_accroisement) + '%, pour un montant de ' + str(
							intcomma(int(accroissement))) + ' Bif sur un montant de ' + str(
							intcomma(int(somme_taxe))) + ' Bif'

					# Montant total de la taxe à payer (parametre taxe le terrain non batit et construction) avec accroisment
					ni.taxe_montant = round(MONTANT_DU)

					# Traçabilité (date_create est créée depuis le model)
					ni.date_update = dateTimeNow
					ni.date_validate = dateTimeNow

					ni.user_create = user
					ni.user_update = user
					ni.user_validate = user

					# Sauvegarder la note d'imposition (taxe sur l'allocation)
					ni.save()

					# dateTimeNow = datetime.datetime.now(tz=timezone.utc)
					# obj.update(date_ecriture=dateTimeNow,user_ecriture=user)
					obj.date_validate = dateTimeNow
					obj.user_validate_id = user.id
					obj.date_ecriture = dateTimeNow
					obj.user_ecriture_id = user.id

					obj.accroissement_taux = taux_accroisement
					obj.accroissement_montant = round(accroissement)					
					obj.save()

def autogenere_note_impot_foncier():
	expertise = FoncierExpertise.objects.all()
	for exper in expertise:
		genere_note_impot_foncier(exper.id)
	return

def autogenere_note_impot_foncier_current_year():
	currentYear = datetime.datetime.now().year
	datetimeNow = datetime.datetime.now(tz=timezone.utc)
	expertise = FoncierExpertise.objects.all()
	for exper in expertise:
		print(exper.id,exper.annee,'***************************************************************')
		if exper.annee == currentYear:
			note_get = NoteImposition.objects.filter(entity=10, entity_id=exper.id, annee=exper.annee,contribuable_id=exper.parcelle.contribuable.id)
			if not note_get:
				objexp = get_object_or_404(FoncierExpertise, pk=exper.id)
				objexp.date_declaration = date(datetimeNow.year,datetimeNow.month,datetimeNow.day)
				objexp.save()
				genere_note_impot_foncier(exper.id)
				print('operation is ok ***************************************************************')
				
# creation d'expertise pour l'annee encour
def genere_expertise():
	expertise = FoncierExpertise.objects.all()
	for exper in expertise:
		auto_genere_expertise(exper.id)
	return

# gestion de creation automatique des note d'imposition et application des penalites
def autogenere_note_impot():
	datetimeNow = datetime.datetime.now()
	currentYear = datetime.datetime.now().year
	currentMonth = datetime.datetime.now().month
	currentDay = datetime.datetime.now().day
	currentMinute = datetime.datetime.now().minute
	currentSecond = datetime.datetime.now().second

	time_end = datetime.datetime(currentYear, currentMonth, currentDay, 12, 0, 0)
	time_end_1 = datetime.datetime(currentYear, 1, 1, 4, 55, 0)
	time_end_2 = datetime.datetime(currentYear, currentMonth, 1, 5, 30, 0)

	time_end_3 = datetime.datetime(currentYear, 1, 1, 6, 0, 0)
	time_end_4 = datetime.datetime(currentYear, 4, 1, 6, 0, 0)
	time_end_5 = datetime.datetime(currentYear, 7, 1, 6, 0, 0)
	time_end_6 = datetime.datetime(currentYear, 10, 1, 6, 0, 0)

	time_end_7 = datetime.datetime(currentYear, 1, 1, 1, 55, 0)
	time_end_8 = datetime.datetime(currentYear, 4, 26, 16, 30, 0)
	time_end_9 = datetime.datetime(currentYear, currentMonth, 26, 11, 30, 0)
	
	
	
	# Génération des notes d'imposition annuel ************************************************************************************************
	# temp de  creation des notes pour AS, AM, AEP, APP, PMC et CPV
	time_to_start_auto_generer_note_annuelle = datetime.datetime(currentYear, 1, 1, 2, 0, 0)
	if time_to_start_auto_generer_note_annuelle < datetimeNow < time_end_1:
		create_note_annuel()
		print('job is run time_to_start_auto_generer_note_annuelle')

	
	# # Génération des notes d'imposition mensuel ************************************************************************************************
	# # temp de  creation des notes pour AT et APM
	time_to_start_auto_generer_note_mensuelle = datetime.datetime(currentYear, currentMonth, 1, 5, 0, 0)
	if time_to_start_auto_generer_note_mensuelle < datetimeNow < time_end_2:
		create_note_monsuel()
		print('job is run time_to_start_auto_generer_note_mensuelle')

	# # Génération des notes d'imposition trimestriel **********************************************************************************************
	# # temps de creation des note pour AT
	time_to_start_trim1 = datetime.datetime(currentYear, 1, 1, 5, 31, 0)
	time_to_start_trim2 = datetime.datetime(currentYear, 4, 1, 0, 0, 0)
	time_to_start_trim3 = datetime.datetime(currentYear, 7, 1, 0, 0, 0)
	time_to_start_trim4 = datetime.datetime(currentYear, 10, 1, 0, 0, 0)
	if time_to_start_trim1 < datetimeNow < time_end_3 or time_to_start_trim2 < datetimeNow < time_end_4 or time_to_start_trim3 < datetimeNow < time_end_5 or time_to_start_trim4 < datetimeNow < time_end_6:
		create_note_trimetriel()
		print('job is run time_to_start_auto_generer_note_ trimestriel')

	# # Génération des expertises de l'annee suivante **********************************************************************************************
	# # temp de  creation des expertise
	time_to_start_auto_generer_expertise = datetime.datetime(currentYear, 1, 1, 0, 0, 0)
	if time_to_start_auto_generer_expertise < datetimeNow < time_end_7:
		#genere_expertise()
		print('job is run ttime_to_start_auto_generer_expertise')

	# # # Génération des notes d'impôt fincier de l'exercice en cour
	# # temp de  creation des notes d'impôt foncier pour exercice d'annee en cour
	time_to_start_auto_generer_note_foncier = datetime.datetime(currentYear, 4, 26, 11, 23, 0)
	if time_to_start_auto_generer_note_foncier < datetimeNow < time_end_8:
		print('job is run time_to_start_auto_generer_note_foncier')
		autogenere_note_impot_foncier_current_year()

	
	# # temp pour applique les penalite
	time_to_start_apply_penalite = datetime.datetime(currentYear, currentMonth, 26, 11, 35, 0)
	if time_to_start_apply_penalite < datetimeNow < time_end_9:
		print('job is run time_to_start_apply_penalite')
		applique_penalite()

	print('run ok')

	# applique_penalite_transport()
	# create_note_monsuel()
	# update_note_monsuel_transport()
	#upgrad_note_trimetriel_transport()

def applique_penalite_current_year():
	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 10 and note.taxe_montant_paye < note.taxe_montant:
			print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
			obj = get_object_or_404(NoteImposition, pk=note.id)
			objExper = FoncierExpertise.objects.filter(id=obj.entity_id)
			if objExper:
				objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
				penalite = 0
				penalite_taux = 0
				intere = 0
				intere_taux = 0
				if not obj.date_penalite:
					print(obj.reference,'reference ***************************************************')
					if obj.annee == dateTimeNow.year:
						check_penalite = Penalite.objects.all()
						for plt in check_penalite:
							# Test si date de declaration subit un accroissement
							# if plt.date_debut.month <= dateTimeNow.month <= plt.date_fin.month:
							if plt.is_taux_annee_ecoulee == 1:
								penalite_taux = int(plt.taux)
					else:
						get_ptl = Penalite.objects.get(is_taux_annee_ecoulee=1)
						penalite_taux = get_ptl.taux

					if penalite_taux > 0:
						solde = obj.taxe_montant - obj.taxe_montant_paye							
						penalite = (solde * penalite_taux) / 100

						obj.taxe_montant =  obj.taxe_montant + round(penalite)
						obj.date_penalite = dateTimeNow
						obj.save()

						objExpr.penalite_taux = penalite_taux
						objExpr.penalite_montant = penalite
						objExpr.save()

						print(obj.reference, obj.taxe_montant, penalite, obj.annee,'reference,taxe_montant,penalite,montant_intere,annee****************************')

				else:
					date = dateTimeNow.strftime("%m")
					# if obj.date_penalite.month < int(date):
					print('addpenalite **********************************************************************')
					get_ptl = Penalite.objects.get(is_taux_annee_ecoulee=2)
					intere_taux = get_ptl.taux

					solde = obj.taxe_montant - obj.taxe_montant_paye
					intere = (solde * intere_taux) / 100
					intere_montant = objExpr.intere_montant + round(intere)
					taux_interer = objExpr.intere_taux + intere_taux
					
					obj.taxe_montant = obj.taxe_montant + round(intere)
					obj.date_penalite = dateTimeNow
					obj.save()
					
					objExpr.intere_taux = taux_interer
					objExpr.intere_montant = intere_montant
					objExpr.save()

		# if note.entity == 1 or note.entity == 2 or note.entity == 5 or note.entity == 6 or note.entity == 7 and note.taxe_montant_paye == 0.00:
		# 	obj = get_object_or_404(NoteImposition, pk=note.id)
		# 	taux_penalite,taux_interer = PenaliteHelpers.has_penalite(obj.annee, dateTimeNow,obj)
		# 	penalite = 0
		# 	if not obj.date_penalite:
		# 		if taux_penalite > 0:
		# 			solde = obj.taxe_montant - obj.taxe_montant_paye
		# 			if solde > 0:
		# 				penalite = (solde * taux_penalite) / 100

		# 		count = 0
		# 		montant = obj.taxe_montant + penalite
		# 		montant_penalite = 0
		# 		if taux_interer > 0:
		# 			while(count<taux_interer):
		# 				count = count + 1
		# 				interer = montant / 100
		# 				montant = montant + interer
		# 				montant_penalite += interer

		# 		montant_intere = montant
		# 		obj.taxe_montant = montant_intere
		# 		obj.date_penalite = dateTimeNow
		# 		print(taux_penalite,taux_interer)
		# 		if taux_penalite > 0 or taux_interer >0:
		# 			obj.save()
		# 			objExpr.penalite_taux = taux_penalite
		# 			objExpr.penalite_montant = penalite
		# 			objExpr.intere_taux = taux_interer
		# 			objExpr.intere_montant = montant_penalite
		# 			objExpr.save()
		# 			print(obj.reference, obj.taxe_montant, penalite, montant_intere, obj.annee,'reference,taxe_montant,penalite,montant_intere,annee****************************')
		# 	else:
		# 		date = dateTimeNow.strftime("%m")
		# 		if obj.date_penalite.month < int(date):
		# 			solde_diff = obj.taxe_montant - obj.taxe_montant_paye
		# 			montant_intere = (solde_diff * taux_interer) / 100
		# 			interer = objExpr.intere_montant + montant_intere
		# 			taux_interer = objExpr.intere_taux + taux_interer
		# 			if solde_diff > 0:
		# 				obj.taxe_montant = obj.taxe_montant + montant_intere
		# 				obj.date_penalite = dateTimeNow
		# 				obj.save()
		# 				if objExpr.intere_taux == 0:
		# 					objExpr.penalite_taux = taux_penalite
		# 					objExpr.penalite_montant = penalite
		# 				objExpr.intere_taux = taux_interer
		# 				objExpr.intere_montant = interer
		# 				objExpr.save()

def applique_penalite():
	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 10 and note.taxe_montant_paye < note.taxe_montant:
			print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
			obj = get_object_or_404(NoteImposition, pk=note.id)
			# objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
			objExper = FoncierExpertise.objects.filter(id=obj.entity_id)
			if objExper:
				objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
				penalite = 0
				if not obj.date_penalite:
					print(obj.reference,'reference ***************************************************')
					for plt in Penalite.objects.filter(is_taux_annee_ecoulee=1):
						taux_penalite = plt.taux

					if taux_penalite > 0:
						solde = obj.taxe_montant - obj.taxe_montant_paye
						if solde > 0:
							penalite = (solde * taux_penalite) / 100

					count = 0
					montant = obj.taxe_montant + penalite
					montant_penalite = 0
					if taux_interer > 0:
						while(count<taux_interer):
							count = count + 1
							interer = montant / 100
							montant = montant + interer
							montant_penalite += interer

					montant_intere = montant
					obj.taxe_montant = montant_intere
					obj.date_penalite = dateTimeNow
					print(taux_penalite,taux_interer)
					if taux_penalite > 0 or taux_interer >0:
						obj.save()
						objExpr.penalite_taux = taux_penalite
						objExpr.penalite_montant = penalite
						objExpr.intere_taux = taux_interer
						objExpr.intere_montant = montant_penalite
						objExpr.save()
						print(obj.reference, obj.taxe_montant, penalite, montant_intere, obj.annee,'reference,taxe_montant,penalite,montant_intere,annee****************************')

				else:
					date = dateTimeNow.strftime("%m")
					# if obj.date_penalite.month < int(date):
					print('addpenalite **********************************************************************')
					solde_diff = obj.taxe_montant - obj.taxe_montant_paye
					montant_intere = (solde_diff * taux_interer) / 100
					interer = objExpr.intere_montant + montant_intere
					taux_interer = objExpr.intere_taux + taux_interer
					if solde_diff > 0:
						obj.taxe_montant = obj.taxe_montant + montant_intere
						obj.date_penalite = dateTimeNow
						obj.save()
						if objExpr.intere_taux == 0:
							objExpr.penalite_taux = taux_penalite
							objExpr.penalite_montant = penalite
						objExpr.intere_taux = taux_interer
						objExpr.intere_montant = interer
						objExpr.save()

		# if note.entity == 1 or note.entity == 2 or note.entity == 5 or note.entity == 6 or note.entity == 7 and note.taxe_montant_paye == 0.00:
		# 	obj = get_object_or_404(NoteImposition, pk=note.id)
		# 	taux_penalite,taux_interer = PenaliteHelpers.has_penalite(obj.annee, dateTimeNow,obj)
		# 	penalite = 0
		# 	if not obj.date_penalite:
		# 		if taux_penalite > 0:
		# 			solde = obj.taxe_montant - obj.taxe_montant_paye
		# 			if solde > 0:
		# 				penalite = (solde * taux_penalite) / 100

		# 		count = 0
		# 		montant = obj.taxe_montant + penalite
		# 		montant_penalite = 0
		# 		if taux_interer > 0:
		# 			while(count<taux_interer):
		# 				count = count + 1
		# 				interer = montant / 100
		# 				montant = montant + interer
		# 				montant_penalite += interer

		# 		montant_intere = montant
		# 		obj.taxe_montant = montant_intere
		# 		obj.date_penalite = dateTimeNow
		# 		print(taux_penalite,taux_interer)
		# 		if taux_penalite > 0 or taux_interer >0:
		# 			obj.save()
		# 			objExpr.penalite_taux = taux_penalite
		# 			objExpr.penalite_montant = penalite
		# 			objExpr.intere_taux = taux_interer
		# 			objExpr.intere_montant = montant_penalite
		# 			objExpr.save()
		# 			print(obj.reference, obj.taxe_montant, penalite, montant_intere, obj.annee,'reference,taxe_montant,penalite,montant_intere,annee****************************')
		# 	else:
		# 		date = dateTimeNow.strftime("%m")
		# 		if obj.date_penalite.month < int(date):
		# 			solde_diff = obj.taxe_montant - obj.taxe_montant_paye
		# 			montant_intere = (solde_diff * taux_interer) / 100
		# 			interer = objExpr.intere_montant + montant_intere
		# 			taux_interer = objExpr.intere_taux + taux_interer
		# 			if solde_diff > 0:
		# 				obj.taxe_montant = obj.taxe_montant + montant_intere
		# 				obj.date_penalite = dateTimeNow
		# 				obj.save()
		# 				if objExpr.intere_taux == 0:
		# 					objExpr.penalite_taux = taux_penalite
		# 					objExpr.penalite_montant = penalite
		# 				objExpr.intere_taux = taux_interer
		# 				objExpr.intere_montant = interer
		# 				objExpr.save()

def applique_penalite_transport():
	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 11 and note.taxe_montant_paye < note.taxe_montant:
			obj = get_object_or_404(NoteImposition, pk=note.id)
			value = PenaliteHelpers.has_penalite_transport(obj.annee, dateTimeNow, obj)

			montant = 0
			if not obj.date_penalite:
				if value > 0:
					montant = obj.taxe_montant + value

				obj.taxe_montant = montant
				obj.penalite_montant = value
				obj.date_penalite = dateTimeNow
				obj.save()

		if note.entity == 12 and note.taxe_montant_paye < note.taxe_montant:
			obj = get_object_or_404(NoteImposition, pk=note.id)
			value = PenaliteHelpers.has_penalite_transport(obj.annee, dateTimeNow, obj)

			penalite = 0
			if not obj.date_penalite:
				if value > 0:
					penalite = (obj.taxe_montant * value)/100

				obj.taxe_montant = obj.taxe_montant + penalite
				obj.penalite_taux = value
				obj.penalite_montant = penalite
				obj.date_penalite = dateTimeNow
				obj.save()

def remove_penalite():
	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 10 and note.date_validate:
			date_debut = date(2022, 4, 1)
			date_fin = date(2022, 4, 4)
			datevalidete = str(note.date_validate)
			date_validete = tuple([int(x) for x in datevalidete[:10].split('-')])
			date_to_test = date(date_validete[0],date_validete[1],date_validete[2])
			if note.taxe_montant_paye < note.taxe_montant and date_debut <= date_to_test <= date_fin and note.user_validate_id != 1 and note.annee <= dateTimeNow.year:
				print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
				obj = get_object_or_404(NoteImposition, pk=note.id)
				objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
				datecreate = str(objExpr.date_create)
				date_create = tuple([int(x) for x in datecreate[:10].split('-')])
				date_to_test_expert = date(date_create[0],date_create[1],date_create[2])

				if date_debut <= date_to_test_expert <= date_fin:
					montant_non_bati = round(objExpr.superficie_non_batie * objExpr.impot_non_batie.impot)
					montant_bati = 0
					lst_car = FoncierCaracteristique.objects.filter(expertise_id=objExpr.id)
					sbt = impobt = 0
					for car in lst_car:
						montant_bati += round(car.superficie_batie * car.impot_batie.impot)
						sbt = car.superficie_batie
						impobt = car.impot_batie.impot

					montant_accroissement = (montant_non_bati + montant_bati) * 0.5
					montant_penalite = (montant_non_bati + montant_bati + montant_accroissement) * 0.1
					# montant_intere = (montant_non_bati + montant_bati + montant_accroissement + montant_penalite) * 0.01
					solde = montant_non_bati + montant_bati + montant_accroissement + montant_penalite
					obj.taxe_montant = round(solde)
					obj.user_penalite_id = obj.user_create_id
					obj.date_penalite = dateTimeNow
					obj.save()

					objExpr.accroissement_montant = round(montant_accroissement)
					objExpr.accroissement_taux = 50.0
					objExpr.penalite_taux = 10.0
					objExpr.penalite_montant = round(montant_penalite)
					objExpr.intere_taux = 0.0
					objExpr.intere_montant = 0  #round(montant_intere)
					objExpr.save()

					print(obj.reference, solde, obj.annee,objExpr.superficie_non_batie,objExpr.impot_non_batie.impot,sbt,impobt,'reference,taxe_montant,penalite,montant_intere,annee****************************')

def update_penalite():
	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 10 and note.date_validate:
			date_debut = date(2022, 1, 1)
			date_fin = date(2022, 4, 2)
			datevalidete = str(note.date_validate)
			date_validete = tuple([int(x) for x in datevalidete[:10].split('-')])
			date_to_test = date(date_validete[0],date_validete[1],date_validete[2])
			if note.taxe_montant_paye < note.taxe_montant and date_debut <= date_to_test <= date_fin and note.annee == dateTimeNow.year:
				print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
				obj = get_object_or_404(NoteImposition, pk=note.id)
				objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
				# datecreate = str(objExpr.date_create)
				# date_create = tuple([int(x) for x in datecreate[:10].split('-')])
				#  date_to_test_expert = date(date_create[0],date_create[1],date_create[2])
				# if date_debut <= date_to_test_expert <= date_fin:
				montant_non_bati = round(objExpr.superficie_non_batie * objExpr.impot_non_batie.impot)
				montant_bati = 0
				lst_car = FoncierCaracteristique.objects.filter(expertise_id=objExpr.id)
				sbt = impobt = 0
				for car in lst_car:
					montant_bati += round(car.superficie_batie * car.impot_batie.impot)
					sbt = car.superficie_batie
					impobt = car.impot_batie.impot

				# montant_accroissement = (montant_non_bati + montant_bati) * 0.5
				# montant_penalite = (montant_non_bati + montant_bati + montant_accroissement) * 0.1
				montant_penalite = (montant_non_bati + montant_bati) * 0.1
				# montant_intere = (montant_non_bati + montant_bati + montant_accroissement + montant_penalite) * 0.01
				# solde = montant_non_bati + montant_bati + montant_accroissement + montant_penalite
				solde = montant_non_bati + montant_bati + montant_penalite
				obj.taxe_montant = round(solde)
				obj.user_penalite_id = obj.user_create_id
				obj.date_penalite = dateTimeNow
				obj.save()

				# objExpr.accroissement_montant = round(montant_accroissement)
				# objExpr.accroissement_taux = 50.0
				objExpr.penalite_taux = 10.0
				objExpr.penalite_montant = round(montant_penalite)
				# objExpr.intere_taux = 0.0
				# objExpr.intere_montant = 0  #round(montant_intere)
				objExpr.save()

				print(obj.reference, solde, obj.annee,objExpr.superficie_non_batie,objExpr.impot_non_batie.impot,sbt,impobt,'reference,taxe_montant,penalite,montant_intere,annee****************************')

def enlever_penalite():
	# dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	# get_note = NoteImposition.objects.all()
	get_note = NoteImposition.objects.filter(entity=10,date_penalite='2022-04-02',annee=2022)
	for note in get_note:
		print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
		obj = get_object_or_404(NoteImposition, pk=note.id)
		objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)

		montant_non_bati = round(objExpr.superficie_non_batie * objExpr.impot_non_batie.impot)
		montant_bati = 0
		lst_car = FoncierCaracteristique.objects.filter(expertise_id=objExpr.id)
		for car in lst_car:
			montant_bati += round(car.superficie_batie * car.impot_batie.impot)
		solde = montant_non_bati + montant_bati
		obj.taxe_montant = round(solde)
		obj.user_penalite_id = None
		obj.date_penalite = None
		obj.save()

		objExpr.penalite_taux = 0.0
		objExpr.penalite_montant = 0
		objExpr.save()

		print(obj.reference, solde,'reference,taxe_montant,penalite,montant_intere,annee****************************')

def change_montant_note():
	obj = NoteImposition.objects.all()
	for note in obj:
		if note.taxe_montant < 1000:
			note_get = get_object_or_404(NoteImposition, pk=note.id)
			note_get.taxe_montant = 0.0
			note_get.taxe_montant_paye = 0.0
			note_get.save()
			print(note.reference,'save now it ok ***************************************************************************************')

def initialisation_acc_pena():
	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 10 and note.date_validate:
			date_debut = date(2022, 1, 1)
			date_fin = date(2022, 4, 11)
			datevalidete = str(note.date_validate)
			date_validete = tuple([int(x) for x in datevalidete[:10].split('-')])
			date_to_test = date(date_validete[0],date_validete[1],date_validete[2])
			if note.taxe_montant_paye < note.taxe_montant and date_debut <= date_to_test <= date_fin and note.annee <= dateTimeNow.year:
				print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
				try:
					obj = get_object_or_404(NoteImposition, pk=note.id)
					objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
					datecreate = str(objExpr.date_create)
					date_create = tuple([int(x) for x in datecreate[:10].split('-')])
					date_to_test_expert = date(date_create[0],date_create[1],date_create[2])

					if date_debut <= date_to_test_expert <= date_fin:
						montant_non_bati = round(objExpr.superficie_non_batie * objExpr.impot_non_batie.impot)
						montant_bati = 0
						lst_car = FoncierCaracteristique.objects.filter(expertise_id=objExpr.id)
						sbt = impobt = 0
						for car in lst_car:
							montant_bati += round(car.superficie_batie * car.impot_batie.impot)
							

						montant_accroissement = 0
						accroissement_taux = 0.0
						if obj.annee < dateTimeNow.year:
							accroissement_taux = 50.0
							montant_accroissement = (montant_non_bati + montant_bati) * 0.5

						solde = montant_non_bati + montant_bati + montant_accroissement 
						obj.taxe_montant = round(solde)
						obj.user_penalite_id = None
						obj.date_penalite = None
						obj.save()

						objExpr.accroissement_montant = round(montant_accroissement)
						objExpr.accroissement_taux =accroissement_taux
						objExpr.penalite_taux = 0.0
						objExpr.penalite_montant = 0
						objExpr.intere_taux = 0.0
						objExpr.intere_montant = 0  
						objExpr.save()

						print(obj.reference, solde, obj.annee,objExpr.superficie_non_batie,objExpr.impot_non_batie.impot,'reference,taxe_montant,penalite,montant_intere,annee****************************')
				except:
					pass

def add_penalite_for_year_equal_current_year():
	# verification is ok
	dateTimeNow = datetime.datetime.now(tz=timezone.utc)
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 10 and note.date_validate:
			date_debut = date(2022, 1, 1)
			date_fin = date(2022, 4, 11)
			datevalidete = str(note.date_validate)
			date_validete = tuple([int(x) for x in datevalidete[:10].split('-')])
			date_to_test = date(date_validete[0],date_validete[1],date_validete[2])
			if note.taxe_montant_paye < note.taxe_montant and date_debut <= date_to_test <= date_fin and note.annee == dateTimeNow.year :
				print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
				try:
					obj = get_object_or_404(NoteImposition, pk=note.id)
					objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
					montant_non_bati = round(objExpr.superficie_non_batie * objExpr.impot_non_batie.impot)
					montant_bati = 0
					lst_car = FoncierCaracteristique.objects.filter(expertise_id=objExpr.id)
					sbt = impobt = 0
					for car in lst_car:
						montant_bati += round(car.superficie_batie * car.impot_batie.impot)

					# montant_accroissement = (montant_non_bati + montant_bati) * 0.5
					montant_penalite = ((montant_non_bati + montant_bati) * 10)/100
					# montant_penalite = (obj.taxe_montant * 10)/100
					#montant_intere = (montant_non_bati + montant_bati + montant_accroissement + montant_penalite) * 0.01
					# solde = montant_non_bati + montant_bati + montant_accroissement + montant_penalite
					solde = montant_non_bati + montant_bati + montant_penalite
					obj.taxe_montant = round(solde)
					obj.user_penalite_id = obj.user_create_id
					obj.date_penalite = dateTimeNow
					obj.save()

					objExpr.accroissement_montant = 0
					objExpr.accroissement_taux = 0.0
					objExpr.penalite_taux = 10.0
					objExpr.penalite_montant = round(montant_penalite)
					objExpr.intere_taux = 1.0
					objExpr.intere_montant = 0  #round(montant_intere)
					objExpr.save()

					print(obj.reference, solde, obj.annee,objExpr.superficie_non_batie,objExpr.impot_non_batie.impot,'reference,taxe_montant,penalite,montant_intere,annee****************************')

				except Exception as e:
					pass

def add_penalite_for_year_different_current_year():
	#############################################################################################################
	# pour les note cree en javier
	#------------------------------
	# de janvier juste à avril
	# on applique une accroissement de 50% et une penalite de 10% pour fevrier et applique un intere de 2% pour 1% de mars et 1% de avril
	#############################################################################################################
	# pour les notes cree en fevrier
	#-------------------------------
	# de fevrier juste à avril
	# on applique une accroissement de 50% et une penalite de 10% pour mars et applique un intere de 1% pour 1% de avril
	#############################################################################################################
	# pour les notes cree en fevrier
	#-------------------------------
	# de mars juste à avril
	# on applique une accroissement de 50% et une penalite de 10% pour avril 
	#############################################################################################################

	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 10 and note.date_validate:
			# pour les notes de janvier check is ok
			# date_debut = date(2022, 1, 1)
			# date_fin = date(2022, 1, 31)

			# pour les notes de fevier
			# date_debut = date(2022, 2, 1)
			# date_fin = date(2022, 2, 28)

			# pour les notes de mars
			date_debut = date(2022, 3, 1)
			date_fin = date(2022, 3, 31)

			datevalidete = str(note.date_validate)
			date_validete = tuple([int(x) for x in datevalidete[:10].split('-')])
			date_to_test = date(date_validete[0],date_validete[1],date_validete[2])
			if note.taxe_montant_paye < note.taxe_montant and date_debut <= date_to_test <= date_fin and note.annee < dateTimeNow.year:
				print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
				try:
					obj = get_object_or_404(NoteImposition, pk=note.id)
					objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
					montant_non_bati = round(objExpr.superficie_non_batie * objExpr.impot_non_batie.impot)
					montant_bati = 0
					lst_car = FoncierCaracteristique.objects.filter(expertise_id=objExpr.id)
					sbt = impobt = 0
					for car in lst_car:
						montant_bati += round(car.superficie_batie * car.impot_batie.impot)

					montant_accroissement = ((montant_non_bati + montant_bati) * 50)/100
					montant_penalite = ((montant_non_bati + montant_bati + montant_accroissement) * 10)/100
					# montant_penalite = (montant_non_bati + montant_bati) * 0.1
					# montant_intere_solde = ((montant_non_bati + montant_bati + montant_accroissement + montant_penalite) * 1)/100
					# montant_intere = ((montant_non_bati + montant_bati + montant_accroissement + montant_penalite) * 1)/100
					# montant_intere = ((montant_non_bati + montant_bati + montant_accroissement + montant_penalite + montant_intere_solde) * 1)/100
					# solde = montant_non_bati + montant_bati + montant_penalite + montant_intere
					# solde = round(montant_non_bati + montant_bati + montant_accroissement + montant_penalite + montant_intere)
					solde =  round(montant_non_bati + montant_bati + montant_accroissement + montant_penalite)
					obj.taxe_montant = round(solde)
					obj.user_penalite_id = obj.user_create_id
					obj.date_penalite = dateTimeNow
					obj.save()

					objExpr.accroissement_montant = round(montant_accroissement)
					objExpr.accroissement_taux = 50.0
					objExpr.penalite_taux = 10.0
					objExpr.penalite_montant = round(montant_penalite)
					objExpr.intere_taux = 0.0
					objExpr.intere_montant = 0 # round(montant_intere)
					objExpr.save()

					print(obj.reference, solde, obj.annee,objExpr.superficie_non_batie,objExpr.impot_non_batie.impot,'reference,taxe_montant,penalite,montant_intere,annee****************************')

				except Exception as e:
					pass

def calcul_taux_intere(obj):

	dateTimeNow = datetime.datetime.now()
	currentYear = dateTimeNow.year
	currentMonth = dateTimeNow.month

	taux_accroisement = 0
	taux_interer = 0
	try:
		objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
		datedeclaration = str(objExpr.date_declaration)
		date_declaration = tuple([int(x) for x in datedeclaration[:10].split('-')])
		
		if date_declaration[1] < 4:
			diff_month = 8
		else:
			diff_month = 12 - date_declaration[1] - 1

		if 3 < date_declaration[1] < 5:
			taux_accroisement = 10

		if date_declaration[1] > 4:
			taux_accroisement = 50
		
		diff_year = int(currentYear) - date_declaration[0]
		 
		taux_interer = diff_month + ((diff_year - 1 )* 12) + int(currentMonth)

		return taux_accroisement, taux_interer
	except Exception as e:
		return taux_accroisement, taux_interer


def update_penalite_intere_for_lest_year():
	# les note a modifir sont de 2014,2015,2016,2017,2018 qui no sont pas encor payer
	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	for note in get_note:
		if note.entity == 10 and note.date_validate:
			date_debut = date(2022, 1, 1)
			date_fin = date(2022, 3, 31)
			datevalidete = str(note.date_validate)
			date_validete = tuple([int(x) for x in datevalidete[:10].split('-')])
			date_to_test = date(date_validete[0],date_validete[1],date_validete[2])
			if note.taxe_montant_paye < note.taxe_montant and note.annee == 2015:
				print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
				try:
					obj = get_object_or_404(NoteImposition, pk=note.id)
					objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
					montant_non_bati = round(objExpr.superficie_non_batie * objExpr.impot_non_batie.impot)
					montant_bati = 0
					lst_car = FoncierCaracteristique.objects.filter(expertise_id=objExpr.id)
					sbt = impobt = 0
					for car in lst_car:
						montant_bati += round(car.superficie_batie * car.impot_batie.impot)

					accroissement = (montant_non_bati + montant_bati) * 0.5

					count = 0
					montant_intere = 0
					montant_penalite = (montant_non_bati + montant_bati + accroissement) * 0.1
					montant = montant_non_bati + montant_bati + accroissement + montant_penalite
					taux_interer = calcul_taux_intere(obj)
					print(obj.reference,taux_interer,date_validete[0],date_validete[1],'****************************************************************************************')
					if taux_interer > 0:
						while(count<taux_interer):
							count = count + 1
							interer = montant / 100
							montant = montant + interer
							montant_intere += interer
					
					solde = montant_non_bati + montant_bati + accroissement + montant_penalite + montant_intere
					obj.taxe_montant = round(solde)
					obj.user_penalite_id = obj.user_create_id
					obj.date_penalite = dateTimeNow
					# obj.save()

					objExpr.accroissement_montant = round(accroissement)
					objExpr.accroissement_taux = taux_accroisement
					objExpr.penalite_taux = 10.0
					objExpr.penalite_montant = round(montant_penalite)
					objExpr.intere_taux = taux_interer
					objExpr.intere_montant = round(montant_intere)
					# objExpr.save()

					print(obj.reference, solde, obj.annee,objExpr.superficie_non_batie,objExpr.impot_non_batie.impot,'reference,taxe_montant,penalite,montant_intere,annee****************************')

				except Exception as e:
					pass


def review_penalite_for_last_year():
	dateTimeNow = datetime.datetime.now()
	get_note = NoteImposition.objects.all()
	
	date_string = "2022-01-01"
	aware = make_aware(datetime.datetime.strptime(date_string, '%Y-%m-%d'))
	for note in get_note:
		if note.entity == 10 and note.date_validate and note.annee < dateTimeNow.year and note.date_create < aware:
			print(note.annee,note.date_create,'job is ok **********************************************')
			obj = get_object_or_404(NoteImposition,pk=note.id)
			if obj.taxe_montant_paye < obj.taxe_montant:
				try:

					objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
					montant_non_bati = round(objExpr.superficie_non_batie * objExpr.impot_non_batie.impot)
					montant_bati = 0
					lst_car = FoncierCaracteristique.objects.filter(expertise_id=objExpr.id)
					
					for car in lst_car:
						montant_bati += round(car.superficie_batie * car.impot_batie.impot)

					taux_accroisement, taux_interer = calcul_taux_intere(obj)
					accroissement_montant = 0
					penalite_montant = 0
					intere_montant = 0
                    
					# accroissement
					if taux_accroisement > 0:
						accroissement_montant = ((montant_non_bati + montant_bati) * taux_accroisement)/100

					# penalite
					penalite_montant = ((montant_non_bati + montant_bati + accroissement_montant) * 10)/100

					count = 0
					montant = montant_non_bati + montant_bati + accroissement_montant + penalite_montant
					if taux_interer > 0:
						while(count<taux_interer):
							count = count + 1
							interer = montant / 100
							montant = montant + interer
							intere_montant += interer

					solde = montant_non_bati + montant_bati + accroissement_montant + penalite_montant + intere_montant
					if taux_accroisement > 0 or taux_interer > 0:
						obj.taxe_montant = round(solde)
						obj.user_penalite_id = 1
						obj.date_penalite = dateTimeNow
						obj.save()

						objExpr.montant_tb = montant_bati
						objExpr.montant_tnb = montant_non_bati

						objExpr.accroissement_montant = accroissement_montant
						objExpr.accroissement_taux = taux_accroisement
						objExpr.penalite_taux = 10.0
						objExpr.penalite_montant = round(penalite_montant)
						objExpr.intere_taux = taux_interer
						objExpr.intere_montant = round(intere_montant)
						objExpr.save()

					print(obj.reference,solde,montant_non_bati , montant_bati , accroissement_montant , penalite_montant , intere_montant)

				except Exception as e:
					pass
				
# add_penalite_for_year_equal_current_year() ok
# add_penalite_for_year_different_current_year() ok
# update_penalite_intere_for_lest_year()
# autogenere_note_impot_foncier_current_year() ok
# applique_penalite_current_year() ok

#review_penalite_for_last_year() ok