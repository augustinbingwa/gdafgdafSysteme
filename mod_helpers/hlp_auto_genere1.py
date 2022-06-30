from django.shortcuts import get_object_or_404
from mod_foncier.submodels.model_foncier_expertise import FoncierExpertise
from mod_foncier.submodels.model_foncier_parcelle import FoncierParcelle
from mod_foncier.submodels.model_foncier_caracteristique import FoncierCaracteristique
from mod_finance.models import NoteImposition
from mod_activite.models import *
from mod_transport.models import *
from mod_parametrage.enums import *
import datetime,re

from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone

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
            if check_next_year <= currentYear:
                print(check_next_year,'check_next_year ************************************************')
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
                            print('Expertise createde **************************************************')
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
                                    print('Caracteristique createde **************************************************')
                                    caract = FoncierCaracteristique(
                                        superficie_batie=cara.superficie_batie,
                                        expertise_id=nwr.id,
                                        impot_batie_id=cara.impot_batie_id)
                                    caract.save()
                        except:
                            pass
               
def auto_genere_prevue_expertise(expertise=0):
    dateTimeNow = datetime.datetime.now()
    currentYear = datetime.datetime.now().year
    obj = get_object_or_404(FoncierExpertise, pk=expertise)
    check_priviou_year = obj.annee - 1
    expert = FoncierExpertise.objects.filter(entity=obj.entity,entity_id=obj.entity_id,annee=check_priviou_year, parcelle_id=obj.parcelle_id).order_by('-annee')[:1]
    if not expert:
        end_year = 2019
        diff_year = int(currentYear) - end_year
        for x in range(diff_year):
            experti = FoncierExpertise(
                annee=check_next_year - x,
                dossier_expertise=obj.dossier_expertise,
                superficie_non_batie=obj.superficie_non_batie,
                date_create=dateTimeNow,
                impot_non_batie_id=obj.impot_non_batie_id,
                parcelle_id=obj.parcelle_id,
                user_create_id=1,
                date_declaration=dateTimeNow)
            experti.save()
            newrow = FoncierExpertise.objects.filter(annee=check_priviou_year,parcelle_id=obj.parcelle_id).order_by('annee')[:1]
            for nwr in newrow:
                caracteur = FoncierCaracteristique.objects.filter(expertise_id=expertise)
                for cara in caracteur:
                    caract = FoncierCaracteristique(
                        superficie_batie=cara.superficie_batie,
                        expertise_id=nwr.id,
                        impot_batie_id=cara.impot_batie_id)
                    caract.save()

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

def create_note_annuel(obj):
    dateTimeNow = datetime.datetime.now(tz=timezone.utc)
    currentYear = datetime.datetime.now(tz=timezone.utc).year
    check_next_year = obj.annee + 1
    exist_not = NoteImposition.objects.filter(entity=obj.annee,annee=check_next_year,contribuable_id=obj.contribuable_id)
    # next_periode = PeriodeHelpers.getNextPeriode(obj.periode)
    user = User.objects.first()
    if not exist_not and check_next_year <= currentYear:
        diff_year = currentYear - obj.annee
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

                            ni = NoteImposition()

                            # Référence de la note d'imposition (chronologique)
                            ni.reference = new_chrono

                            # Contribuable qui se trouve sur l'allocation de la place dans le marché (contrat préalable) IMPORTANT !!!
                            ni.contribuable = obj.contribuable

                            # Entity Modèle : 'BaseActivite'
                            ni.entity = ENTITY_ACTIVITE_STANDARD

                            # Identifiant de l'entity : 'Srandard'
                            ni.entity_id = obj.id

                            # Période de paiement
                            ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)

                            # Année de paiement (Très important pour la gestion des périodes)
                            ni.annee = check_next_year + x

                            # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                            ni.taxe = obj.taxe

                            # ACCROISEMENT
                            taux_accroisement = AccroissementHelpers.has_accroissement(check_next_year, dateTimeNow)
                            accroissement = 0
                            if taux_accroisement > 0:
                                accroissement = (obj.taxe.tarif * taux_accroisement) / 100

                            # Montant dû
                            MONTANT_DU = obj.taxe.tarif + accroissement

                            # Solde de depart
                            if activite.solde_depart > 0:
                                MONTANT_DU += activite.solde_depart

                            # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
                            ni.taxe_montant = MONTANT_DU

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

                            ni = NoteImposition()

                            # Référence de la note d'imposition (chronologique)
                            ni.reference = new_chrono

                            # Contribuable qui se trouve sur l'allocation de la place dans le marché (contrat préalable) IMPORTANT !!!
                            ni.contribuable = obj.contribuable

                            # Entity Modèle : 'BaseActivite'
                            ni.entity = ENTITY_ACTIVITE_MARCHE

                            # Identifiant de l'entity : 'Srandard'
                            ni.entity_id = obj.id

                            # Période de paiement
                            ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)

                            # Année de paiement (Très important pour la gestion des périodes)
                            ni.annee = check_next_year + x

                            # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                            ni.taxe = obj.taxe

                            # ACCROISEMENT
                            taux_accroisement = AccroissementHelpers.has_accroissement(check_next_year, dateTimeNow)
                            accroissement = 0
                            if taux_accroisement > 0:
                                accroissement = (obj.taxe.tarif * taux_accroisement) / 100

                            # Montant dû
                            MONTANT_DU = obj.taxe.tarif + accroissement

                            # Solde de depart
                            if activite.solde_depart > 0:
                                MONTANT_DU += activite.solde_depart

                            # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
                            ni.taxe_montant = MONTANT_DU

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
                            # obj_chrono.save()

                            ni = NoteImposition()

                            # Référence de la note d'imposition (chronologique)
                            ni.reference = new_chrono

                            # Contribuable
                            ni.contribuable = obj.contribuable

                            # Entity Modèle : 'AllocationEspacePublique'
                            ni.entity = ENTITY_ALLOCATION_ESPACE_PUBLIQUE

                            # Identifiant de l'entity : 'AllocationEspacePublique'
                            ni.entity_id = obj.entity_id

                            # Période de paiement
                            ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)

                            # Année de paiement (Très important pour la gestion des périodes)
                            ni.annee = check_next_year + x

                            # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                            ni.taxe = obj.taxe

                            # Montant total de la taxe à payer (montant par m² x tarif)
                            montant_total = allocation.superficie * obj.taxe.tarif

                            # ACCROISEMENT
                            taux_accroisement = AccroissementHelpers.has_accroissement(check_next_year, dateTimeNow)
                            accroissement = 0
                            if taux_accroisement > 0:
                                accroissement = (montant_total * taux_accroisement) / 100

                            MONTANT_DU = montant_total + accroissement

                            # Solde de depart
                            if allocation.solde_depart > 0:
                                MONTANT_DU += allocation.solde_depart

                            # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
                            ni.taxe_montant = MONTANT_DU
                            # Traçabilité (date_create est créée depuis le model)
                            ni.date_update = dateTimeNow
                            ni.date_validate = dateTimeNow
                            ni.user_create = user
                            ni.user_update = user
                            ni.user_validate = user
                            # Sauvegarder la note d'imposition (taxe sur l'allocation de l'espace)
                            ni.save()

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
                                obj_chrono.save();

                                # ---------------------------------------------------------------------
                                # 3 - Créer l'objet Note d'imposition
                                ni = NoteImposition()

                                # Référence de la note d'imposition (chronologique)
                                ni.reference = new_chrono

                                # Contribuable
                                ni.contribuable = obj.contribuable

                                # Entity Modèle : 'AllocationPanneauPublicitaire'
                                ni.entity = ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE

                                # Identifiant de l'entity : 'AllocationPanneauPublicitaire'
                                ni.entity_id = obj.entity_id

                                # Période de paiement
                                ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)

                                # Année de paiement (Très important pour la gestion des périodes)
                                ni.annee = check_next_year + x

                                # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                                ni.taxe = obj.taxe

                                # Montant total de la taxe à payer (montant par m² x tarif)
                                montant_total = allocation.superficie * obj.taxe.tarif

                                # ACCROISEMENT
                                taux_accroisement = AccroissementHelpers.has_accroissement(check_next_year, dateTimeNow)
                                accroissement = 0
                                if taux_accroisement > 0:
                                    accroissement = (montant_total * taux_accroisement) / 100

                                MONTANT_DU = montant_total + accroissement

                                # Solde de depart
                                if allocation.solde_depart > 0:
                                    MONTANT_DU += allocation.solde_depart

                                # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
                                ni.taxe_montant = MONTANT_DU

                                # Traçabilité (date_create est créée depuis le model)
                                ni.date_update = dateTimeNow
                                ni.date_validate = dateTimeNow

                                ni.user_create = user
                                ni.user_update = user
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
                                obj_chrono.save();

                                # ---------------------------------------------------------------------
                                # 3 - Créer l'objet Note d'imposition
                                ni = NoteImposition()

                                # Référence de la note d'imposition (chronologique)
                                ni.reference = new_chrono

                                # Contribuable
                                ni.contribuable = obj.contribuable

                                # Entity Modèle : 'PubliciteMurCloture'
                                ni.entity = ENTITY_PUBLICITE_MUR_CLOTURE

                                # Identifiant de l'entity : 'PubliciteMurCloture'
                                ni.entity_id = obj.entity_id

                                # Période de paiement
                                ni.periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)

                                # Année de paiement (Très important pour la gestion des périodes)
                                ni.annee = check_next_year + x

                                # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                                ni.taxe = obj.taxe

                                # Montant total de la taxe à payer (montant par m² x tarif)
                                montant_total = allocation.superficie * obj.taxe.tarif

                                # ACCROISEMENT
                                taux_accroisement = AccroissementHelpers.has_accroissement(check_next_year, dateTimeNow)
                                accroissement = 0
                                if taux_accroisement > 0:
                                    accroissement = (montant_total * taux_accroisement) / 100

                                MONTANT_DU = montant_total + accroissement

                                # Solde de depart
                                if allocation.solde_depart > 0:
                                    MONTANT_DU += allocation.solde_depart

                                # Montant total de la taxe à payer (parametre taxe d'activité dans le marché)
                                ni.taxe_montant = MONTANT_DU

                                # Traçabilité (date_create est créée depuis le model)
                                ni.date_update = dateTimeNow
                                ni.date_validate = dateTimeNow

                                ni.user_create = user
                                ni.user_update = user
                                ni.user_validate = user

                                # Sauvegarder la note d'imposition (taxe sur la publicité)
                                ni.save()
                            except:
                                pass

            # ceartion de note d'imposition VEHICULE PROPRIETE
            ############################################################################
            if obj.entity == 13:
                    vehicule = VehiculeProprietaire.objects.get(id=obj.entity_id)
                    if vehicule.vehicule.sous_categorie.taxe_proprietaire:
                        if vehicule.vehicule.actif:
                            try:
                                # ---------------------------------------------------------------------
                                # 3 - Créer et Valider la note d'imposition (taxe sur le proriétaire)
                                # Générer le nouveau numéro chrono
                                new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                obj_chrono.last_chrono = new_chrono
                                obj_chrono.save();

                                # Créer l'objet Note d'imposition
                                ni = NoteImposition()

                                # Référence de la note d'imposition (chronologique)
                                ni.reference = new_chrono

                                # Contribuable
                                ni.contribuable = obj.contribuable

                                # Entity Modèle : 'VehiculeProprietaire'
                                ni.entity = ENTITY_VEHICULE_PROPRIETE

                                # Identifiant de l'entity : 'VehiculeProprietaire'
                                ni.entity_id = obj.entity_id

                                # Période de paiement
                                ni.periode = PeriodeHelpers.getCurrentPeriode(vehicule.vehicule.sous_categorie.taxe_proprietaire.periode_type)

                                # Année de paiement (Très important pour la gestion des périodes)
                                ni.annee = check_next_year + x

                                # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                                ni.taxe = vehicule.vehicule.sous_categorie.taxe_proprietaire

                                # Montant total de la taxe à payer (parametre taxe)
                                ni.taxe_montant = vehicule.vehicule.sous_categorie.taxe_proprietaire.tarif

                                # Traçabilité (date_create est créée depuis le model)
                                ni.date_update = dateTimeNow
                                ni.date_validate = dateTimeNow

                                ni.user_create = user
                                ni.user_update = user
                                ni.user_validate = user

                                # Sauvegarder la note d'imposition (taxe sur le propriétaire)
                                ni.save()

                                vehicule.date_ecriture = dateTimeNow
                                vehicule.user_ecriture = user
                                vehicule.save()
                            except:
                                pass

def create_note_monsuel(obj):
    dateTimeNow = datetime.datetime.now(tz=timezone.utc)
    currentYear = datetime.datetime.now(tz=timezone.utc).year
    currentMonth = datetime.datetime.now(tz=timezone.utc).month
    next_periode = obj.periode_id + 1
    exist_not = NoteImposition.objects.filter(entity=obj.entity,entity_id=obj.entity_id ,periode_id=next_periode, annee=obj.annee)
    user = User.objects.first()
    if not exist_not :
        if obj.entity == 12:
            activite = VehiculeActivite.objects.get(id=obj.entity_id)
            if not activite.vehicule.compte_propre:
                if activite.vehicule.sous_categorie.taxe_activite.tarif > 0:
                    if activite.vehicule.actif:
                        try:
                            # ---------------------------------------------------------------------
                            # 3 - Créer et Valider la note d'imposition (taxe sur l'activité de transport municipal)
                            # Générer le nouveau numéro chrono
                            new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                            obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                            obj_chrono.last_chrono = new_chrono
                            obj_chrono.save();

                            # Créer l'objet Note d'imposition pour l'activité de transport
                            ni = NoteImposition()

                            # Référence de la note d'imposition (chronologique)
                            ni.reference = new_chrono

                            # Contribuable
                            ni.contribuable = obj.contribuable

                            # Entity Modèle : 'VehiculeProprietaire'
                            ni.entity = ENTITY_DROIT_STATIONNEMENT

                            # Identifiant de l'entity : 'VehiculeActivite'
                            ni.entity_id = obj.entity_id
                            if obj.annee <currentYear and obj.periode_id == 12:
                                annee = obj.annee + 1
                                if annee == currentYear:
                                    annee = currentYear
                                periode = 1
                            elif obj.annee == currentYear and next_periode == currentMonth:
                                periode = PeriodeHelpers.getCurrentPeriode(activite.vehicule.sous_categorie.taxe_stationnement.periode_type)
                                annee = currentYear
                            else:
                                annee = obj.annee
                                periode = next_periode

                            # Période de paiement
                            # Si période multiple (soit : mensuel, trimestriel, ou annuel), alors localiser la période en cours

                            ni.periode_id = periode

                            # Année de paiement (Très important pour la gestion des périodes)
                            ni.annee = annee

                            # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                            ni.taxe = activite.vehicule.sous_categorie.taxe_activite

                            # Montant dû
                            MONTANT_DU = activite.vehicule.sous_categorie.taxe_activite.tarif

                            # Solde de depart
                            if activite.solde_depart > 0:
                                MONTANT_DU += activite.solde_depart

                            # Montant total de la taxe à payer (parametre taxe)
                            ni.taxe_montant = MONTANT_DU

                            # Traçabilité (date_create est créée depuis le model)
                            ni.date_update = dateTimeNow
                            ni.date_validate = dateTimeNow

                            ni.user_create = user
                            ni.user_update = user
                            ni.user_validate = user

                            # Sauvegarder la note d'imposition (taxe sur activité)
                            ni.save()
                        except:
                            pass

        if obj.entity == 8:
                allocation = AllocationPlaceMarche.objects.get(id=obj.entity_id)
                if allocation.droit_place_marche.cout_place > 0:
                    if not allocation.date_fin :
                        try:
                            # ---------------------------------------------------------------------
                            # 2 - Créer et Valider la note d'imposition (taxe sur le droit de place)
                            # Générer le nouveau numéro chrono
                            new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                            obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                            obj_chrono.last_chrono = new_chrono
                            obj_chrono.save();

                            # ---------------------------------------------------------------------
                            # 3 - Créer l'objet Note d'imposition
                            ni = NoteImposition()

                            # Référence de la note d'imposition (chronologique)
                            ni.reference = new_chrono

                            # Contribuable
                            ni.contribuable = obj.contribuable

                            # Entity Modèle : 'AllocationPlaceMarche'
                            ni.entity = ENTITY_ALLOCATION_PLACE_MARCHE

                            # Identifiant de l'entity : 'AllocationPlaceMarche'
                            ni.entity_id = obj.entity_id


                            # Année de paiement (Très important pour la gestion des périodes)
                            if obj.annee < currentYear and obj.periode_id == 12:
                                annee = obj.annee + 1
                                if annee == currentYear:
                                    annee = currentYear
                                periode = 1
                            elif obj.annee == currentYear and next_periode == currentMonth:
                                annee = currentYear
                                periode = PeriodeHelpers.getCurrentPeriode(obj.taxe.periode_type)
                            else:
                                annee = obj.annee
                                periode = next_periode

                            # Période de paiement
                            ni.periode_id = periode

                            ni.annee = annee

                            # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                            ni.taxe = obj.taxe

                            # Montant dû
                            MONTANT_DU = allocation.droit_place_marche.cout_place

                            # si CAUTION n'est pas encore payee
                            if allocation.caution_montant > 0:
                                MONTANT_DU += allocation.caution_montant
                                ni.libelle += '. Avec une caution de ' + str(
                                    allocation.caution_nombre_mois) + ' mois pour un montant de ' + str(
                                    intcomma(allocation.caution_montant)) + 'Bif.'

                            # Solde de depart
                            if allocation.solde_depart > 0:
                                MONTANT_DU += allocation.solde_depart

                            # Montant total de la taxe à payer (parametre taxe dans DroitPlaceMarche)
                            ni.taxe_montant = MONTANT_DU

                            # Traçabilité (date_create est créée depuis le model)
                            ni.date_update = dateTimeNow
                            ni.date_validate = dateTimeNow

                            ni.user_create = user
                            ni.user_update = user
                            ni.user_validate = user

                            # Sauvegarder la note d'imposition (taxe sur l'allocation de la place)
                            ni.save()

                            allocation.date_ecriture = dateTimeNow
                            allocation.user_ecriture = user
                            allocation.save()
                        except:
                            pass

def create_note_trimetriel(obj):
    dateTimeNow = datetime.datetime.now(tz=timezone.utc)
    currentYear = datetime.datetime.now(tz=timezone.utc).year
    currentMonth = datetime.datetime.now(tz=timezone.utc).month
    next_periode = obj.periode_id + 1
    exist_not = NoteImposition.objects.filter(entity=obj.entity, entity_id=obj.entity_id, periode_id=next_periode, annee=obj.annee)
    user = User.objects.first()
    if not exist_not:
        if obj.entity == 11:
            activite = VehiculeActivite.objects.get(id=obj.entity_id)
            if not activite.vehicule.compte_propre:
                if activite.vehicule.sous_categorie.taxe_activite.tarif > 0:
                    # ---------------------------------------------------------------------
                    # 3 - Créer et Valider la note d'imposition (taxe sur l'activité de transport municipal)
                    # Générer le nouveau numéro chrono
                    if activite.vehicule.actif:
                        try:
                            if obj.periode.id < 17:
                                new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                obj_chrono.last_chrono = new_chrono
                                obj_chrono.save();

                                # Créer l'objet Note d'imposition pour l'activité de transport
                                ni = NoteImposition()

                                # Référence de la note d'imposition (chronologique)
                                ni.reference = new_chrono

                                # Contribuable
                                ni.contribuable = obj.contribuable

                                # Entity Modèle : 'VehiculeProprietaire'
                                ni.entity = ENTITY_VEHICULE_ACTIVITE

                                # Identifiant de l'entity : 'VehiculeActivite'
                                ni.entity_id = obj.entity_id
                                trim = 0
                                if currentMonth < 4:
                                    trim = 13
                                if 3 < currentMonth < 7:
                                    trim = 14
                                if 6 < currentMonth < 10:
                                    trim = 15
                                if 9 < currentMonth < 13:
                                    trim = 16

                                if obj.annee < currentYear and obj.periode_id == 16:
                                    annee = obj.annee + 1
                                    if annee == currentYear:
                                        annee = currentYear
                                    periode = 13
                                elif obj.annee == currentYear and next_periode == trim:
                                    periode = PeriodeHelpers.getCurrentPeriode(activite.vehicule.sous_categorie.taxe_activite.periode_type)
                                    annee = currentYear
                                else:
                                    annee = obj.annee
                                    periode = next_periode

                                # Période de paiement
                                # Si période multiple (soit : mensuel, trimestriel, ou annuel), alors localiser la période en cours
                                ni.periode_id = periode

                                # Année de paiement (Très important pour la gestion des périodes)
                                ni.annee = annee

                                # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                                ni.taxe = activite.vehicule.sous_categorie.taxe_activite

                                # Montant dû
                                MONTANT_DU = activite.vehicule.sous_categorie.taxe_activite.tarif

                                # Solde de depart
                                if activite.solde_depart > 0:
                                    MONTANT_DU += activite.solde_depart

                                # Montant total de la taxe à payer (parametre taxe)
                                ni.taxe_montant = MONTANT_DU

                                # Traçabilité (date_create est créée depuis le model)
                                ni.date_update = dateTimeNow
                                ni.date_validate = dateTimeNow

                                ni.user_create = user
                                ni.user_update = user
                                ni.user_validate = user

                                # Sauvegarder la note d'imposition (taxe sur activité)
                                ni.save()

                                vehicule.date_ecriture = dateTimeNow
                                vehicule.user_ecriture = user
                                vehicule.save()
                            if obj.periode.id == 19 and obj.annee <= currentYear:
                                new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                obj_chrono.last_chrono = new_chrono
                                obj_chrono.save();

                                # Créer l'objet Note d'imposition pour l'activité de transport
                                ni = NoteImposition()

                                # Référence de la note d'imposition (chronologique)
                                ni.reference = new_chrono

                                # Contribuable
                                ni.contribuable = obj.contribuable

                                # Entity Modèle : 'VehiculeProprietaire'
                                ni.entity = ENTITY_VEHICULE_ACTIVITE

                                # Identifiant de l'entity : 'VehiculeActivite'
                                ni.entity_id = obj.entity_id

                                # Période de paiement
                                # Si période multiple (soit : mensuel, trimestriel, ou annuel), alors localiser la période en cours
                                ni.periode_id = obj.periode_id
                                if obj.annee < currentYear:
                                    annee = obj.annee + 1
                                else:
                                    annee = currentYear
                                # Année de paiement (Très important pour la gestion des périodes)
                                ni.annee = annee

                                # Taxe sur activité, Objet taxe (Type : Note d'imposition)
                                ni.taxe = activite.vehicule.sous_categorie.taxe_activite

                                # Montant dû
                                MONTANT_DU = activite.vehicule.sous_categorie.taxe_activite.tarif

                                # Solde de depart
                                if activite.solde_depart > 0:
                                    MONTANT_DU += activite.solde_depart

                                # Montant total de la taxe à payer (parametre taxe)
                                ni.taxe_montant = MONTANT_DU

                                # Traçabilité (date_create est créée depuis le model)
                                ni.date_update = dateTimeNow
                                ni.date_validate = dateTimeNow

                                ni.user_create = user
                                ni.user_update = user
                                ni.user_validate = user

                                # Sauvegarder la note d'imposition (taxe sur activité)
                                ni.save()

                                vehicule.date_ecriture = dateTimeNow
                                vehicule.user_ecriture = user
                                vehicule.save()
                        except:
                            pass

def genere_note_impot_foncier(expertiseid=0):
    user = User.objects.first()
    currentYear = datetime.datetime.now().year
    dateTimeNow = datetime.datetime.now(tz=timezone.utc)
    if expertiseid != 0:
        # Récuperer l'identifiant de la parcelle
        obj = get_object_or_404(FoncierExpertise, pk=expertiseid)
        if obj.annee < currentYear:
            if obj:
                montant_non_bati = round(obj.superficie_non_batie * obj.impot_non_batie.impot)
                # Traitement des contructions (terrain bâti)
                montant_construction = 0
                lst_car = FoncierCaracteristique.objects.filter(expertise_id=obj.id)
                for car in lst_car:
                    montant_construction += round(car.superficie_batie * car.impot_batie.impot)

                somme_taxe = montant_non_bati + montant_construction
                check_note = NoteImposition.objects.filter(entity=10, entity_id=expertiseid, annee=obj.annee)
                if not check_note:
                    obj.date_validate = dateTimeNow
                    obj.user_validate_id = user.id
                    obj.save()
                    # with transaction.atomic():
                    # OperationsHelpers.execute_action_ecriture(self, obj)
                    # ---------------------------------------------------------------------
                    # 2 - Générer le nouveau numéro chrono
                    new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                    obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                    obj_chrono.last_chrono = new_chrono
                    # Calculer le montant de l'impot (terrain non bati et construction)
                    # somme_taxe, tnb, tb = get_montant_note(obj)

                    # Si accroissement existe
                    taux_accroisement = obj.has_accroissement
                    MONTANT_DU = accroissement = 0
                    if somme_taxe > 0 and taux_accroisement > 0:
                        accroissement = (somme_taxe * taux_accroisement) / 100

                    MONTANT_DU = somme_taxe + accroissement
                    print(somme_taxe,'somme_taxe *****************************************************************')
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
                        print('creation de ', new_chrono,'avec success ***********************************************************************')

                        # dateTimeNow = datetime.datetime.now(tz=timezone.utc)
                        # obj.update(date_ecriture=dateTimeNow,user_ecriture=user)
                        obj.date_ecriture = dateTimeNow
                        obj.user_ecriture = user
                        obj.save()

def autogenere_note_impot_foncier():
    expertise = FoncierExpertise.objects.all()
    for exper in expertise:
        genere_note_impot_foncier(exper.id)
    return

def genere_expertise():
    expertise = FoncierExpertise.objects.all()
    for exper in expertise:
        auto_genere_expertise(exper.id)
    return

def autogenere_note_impot():
    datetimeNow = datetime.datetime.now()
    currentYear = datetime.datetime.now().year
    currentMonth = datetime.datetime.now().month
    currentDay = datetime.datetime.now().day
    currentMinute = datetime.datetime.now().minute
    currentSecond = datetime.datetime.now().second
    #temp de  creation des notes pour AS, AM, AEP, APP, PMC et CPV
    time_to_start_auto_generer_note_annuelle = datetime.datetime(currentYear, 2, 12, 11, 20,0)

    # temp de  creation des notes pour AT et APM
    time_to_start_auto_generer_note_mensuelle = datetime.datetime(currentYear, currentMonth, 1, 0, 0, 0)

    # temp de  creation des expertise
    time_to_start_auto_generer_expertise = datetime.datetime(currentYear, 1, 1, 0, 0, 0)

    # temp de  creation des notes d'impôt foncier pour exercice d'annee en cour
    time_to_start_auto_generer_note_foncier = datetime.datetime(currentYear, 5, 1, 0, 0, 0)

    # temp pour applique les penalite
    time_to_start_apply_penalite = datetime.datetime(currentYear, currentMonth, 1, 0, 0, 0)

    #temps de creation des note pour AT
    time_to_start_trim1 = datetime.datetime(currentYear, 2, 12, 11, 20, 0)
    time_to_start_trim2 = datetime.datetime(currentYear, 4, 1, 0, 0, 0)
    time_to_start_trim3 = datetime.datetime(currentYear, 7, 1, 0, 0, 0)
    time_to_start_trim4 = datetime.datetime(currentYear, 10, 1, 0, 0, 0)


    time_end = datetime.datetime(currentYear, currentMonth, currentDay, 5, 59, 0)


    ArrayEntityAnnuelle = [1,2,5,6,7,13]  # entity pour les notes annuelle
    ArrayEntityMensuelle = [8,12]  # entity pour les notes mensuelle

    # Génération des notes d'imposition annuel
    if time_to_start_auto_generer_note_annuelle < datetimeNow < time_end:
        print('time_to_start_auto_generer_note_annuelle is ok *****************************************')
    #     for check_entity in ArrayEntityAnnuelle:
    #         get_note = NoteImposition.objects.filter(entity=check_entity).order_by('entity')
    #         for containte in get_note:
    #             check_next_year = containte.annee + 1
    #             exist_next_note = NoteImposition.objects.filter(entity=containte.entity,entity_id=containte.entity_id,annee=check_next_year)
    #             if not exist_next_note :
    #                 create_note_annuel(containte)
    #
    # # Génération des notes d'imposition mensuel
    if time_to_start_auto_generer_note_mensuelle < datetimeNow < time_end:
        print('time_to_start_auto_generer_note_mensuelle is ok *****************************************')
    #     for check_entity in ArrayEntityMensuelle:
    #         get_note = NoteImposition.objects.filter(entity=check_entity).order_by('entity')
    #         for containte in get_note:
    #             check_next_year = containte.annee + 1
    #             exist_next_note = NoteImposition.objects.filter(entity=containte.entity, entity_id=containte.entity_id,annee=check_next_year)
    #             if not exist_next_note:
    #                 create_note_monsuel(containte)
    #
    # # Génération des notes d'imposition trimestriel
    if time_to_start_trim1 < datetimeNow < time_end or time_to_start_trim2 < datetimeNow < time_end or time_to_start_trim3 < datetimeNow < time_end or time_to_start_trim4 < datetimeNow < time_end:
        print('time_to_start_trim is ok *****************************************')

    #     get_note = NoteImposition.objects.filter(entity=11).order_by('entity')
    #     for containte in get_note:
    #         if containte.annee < currentYear:
    #             diff_year = currentYear - containte.annee
    #             for x in range(diff_year):
    #                 diff_periode = 16 - containte.periode_id
    #                 for y in range(diff_periode):
    #                     create_note_trimetriel(containte)
    #         else:
    #             create_note_trimetriel(containte)

    # Génération des expertises de l'annee suivante
    if time_to_start_auto_generer_expertise < datetimeNow < time_end:
        # genere_expertise()
        pass

    if time_to_start_auto_generer_note_foncier < datetimeNow < time_end:
        # autogenere_note_impot_foncier()
        pass


    # genere_expertise()
    # applique_penalite()
    # autogenere_note_impot_foncier()
    remove_penalite()
    # # Génération des notes d'impôt fincier de l'exercice en cour
    if time_to_start_auto_generer_note_foncier < datetimeNow < time_end:
        print('time_to_start_auto_generer_note_foncier is ok *****************************************')

    #     auto_genere_expertise_and_note()

def applique_penalite():
    dateTimeNow = datetime.datetime.now()
    get_note = NoteImposition.objects.all()
    # get_note = NoteImposition.objects.filter(entity=10,entity_id=15527,annee=2019)
    for note in get_note:
        if note.entity == 10 and note.taxe_montant_paye < note.taxe_montant and note.annee < int(dateTimeNow.year):
            print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
            obj = get_object_or_404(NoteImposition, pk=note.id)
            # objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
            objExper = FoncierExpertise.objects.filter(id=obj.entity_id)
            if objExper:
                objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
                taux_penalite,taux_interer = PenaliteHelpers.has_penalite(obj.annee, dateTimeNow,obj)
                penalite = 0
                if not obj.date_penalite:
                    print(obj.reference,'reference ***************************************************')
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
                    if obj.date_penalite.month < int(date):
                        print('remix **********************************************************************')
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
                            
                            
def remove_penalite():
    dateTimeNow = datetime.datetime.now()
    get_note = NoteImposition.objects.all()
    count= 0
    for note in get_note:
        if note.entity == 10 and note.date_validate:
            date_debut = date(2022, 1, 1)
            date_fin = date(2022, 1, 31)
            datevalidete = str(note.date_validate)
            # donne = datevalidete[:10].split('-')
            date_validete = tuple([int(x) for x in datevalidete[:10].split('-')])
            # print(donne[1])
            # print(donne[0],donne[1],donne[2])
            date_to_test = date(date_validete[0],date_validete[1],date_validete[2])
            if note.taxe_montant_paye < note.taxe_montant and date_debut <= date_to_test <= date_fin and note.user_validate_id != 1 and note.annee < dateTimeNow.year:
                print(note.reference,note.annee ,'job is run now  reference ***********************************************************************')
                obj = get_object_or_404(NoteImposition, pk=note.id)
                objExpr = get_object_or_404(FoncierExpertise, pk=obj.entity_id)
                datecreate = str(objExpr.date_create)
                date_create = tuple([int(x) for x in datecreate[:10].split('-')])
                date_to_test_expert = date(date_create[0],date_create[1],date_create[2])

                if date_debut <= date_to_test_expert <= date_fin:
                    count += 1
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
                    obj.taxe_montant = solde
                    # obj.taxe_montant = montant_non_bati + montant_bati + montant_accroissement
                    obj.date_penalite = dateTimeNow
                    obj.save()

                    objExpr.accroissement_montant = montant_accroissement
                    objExpr.accroissement_taux = 50.0
                    objExpr.penalite_taux = 10.0
                    objExpr.penalite_montant = montant_penalite
                    objExpr.intere_taux = 0.0
                    objExpr.intere_montant = 0
                    objExpr.save()

                    print(obj.reference, solde, obj.annee,objExpr.superficie_non_batie,objExpr.impot_non_batie.impot,sbt,impobt,'reference,taxe_montant,penalite,montant_intere,annee****************************') 
    print(count)                    
    