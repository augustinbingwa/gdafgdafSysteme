from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django.db.models import Count
from django.utils import timezone
import datetime

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_periode import PeriodeHelpers
from mod_helpers.hlp_entity import EntityHelpers
from mod_helpers.models import Chrono
from mod_finance.models import NoteImposition,Periode
from mod_foncier.models import FoncierExpertise
from mod_transport.models import Vehicule,VehiculeActivite
from mod_activite.models import  BaseActivite,Standard,Marche,AllocationEspacePublique,AllocationPanneauPublicitaire,PubliciteMurCloture,AllocationPlaceMarche
from mod_finance.templatetags import impot_filter
from mod_parametrage.enums import *

class AutogenerNoteHelpers():

    def create_note_periode_suivante_annuel(entity, obj, annee=0):
        dateTimeNow = datetime.datetime.now(tz=timezone.utc)
        date = dateTimeNow.date()
        currentYear = int(date.strftime("%Y"))
        # filitre selon l'entity
        if annee != 0:
            currentNote = obj.objects.filter(entity=entity,annee__range=[annee, currentYear]).order_by('annee')
        else:
            currentNote = obj.objects.filter(entity=entity).order_by('annee')

        # filtre le resultat recupere dans currentNote pour enleve le redondance dans entity_id
        currentNoteF = currentNote.values('id','entity_id','annee').annotate(entity_check=Count('entity_id')).order_by('entity_id')
        for crtn in currentNoteF:
            # filtre le resultat recupere dans currentNote selon le resultat trouve dans currentNoteF pour determiner le dernier NI créé
            currentNotef1 = currentNote.filter(entity_id=crtn['entity_id']).order_by('annee').last()
            year = currentNotef1.annee
            activite = None
            validate = 0
            if currentNotef1.annee != currentYear:
                while year < currentYear:
                    next_periode = PeriodeHelpers.getNextPeriode(currentNotef1.periode)
                    nextyear = year + 1
                    year = nextyear

                    if entity == 1 and currentNotef1.entity == 1:
                        try:
                            activite = BaseActivite.objects.get(id=currentNotef1.entity_id)
                            libelle = currentNotef1.libelle
                            somme_taxe = currentNotef1.taxe.tarif
                            if activite.actif == True:
                                validate =1
                            else:
                                validate = 0
                        except:
                            validate = 0

                    elif entity == 2 and currentNotef1.entity == 2:
                        activite = BaseActivite.objects.get(id=currentNotef1.entity_id)
                        libelle = currentNotef1.libelle
                        somme_taxe = currentNotef1.taxe.tarif
                        if activite.actif == True:
                            validate =1
                        else:
                            validate = 0
                    elif entity == 5 and currentNotef1.entity == 5:
                        activite = AllocationEspacePublique.objects.get(id=currentNotef1.entity_id)
                        libelle = currentNotef1.libelle
                        somme_taxe = currentNotef1.taxe.tarif
                        if activite.date_fin == None:
                            validate =1
                        else:
                            validate = 0
                    elif entity == 6 and currentNotef1.entity == 6:
                        activite = AllocationPanneauPublicitaire.objects.get(id=currentNotef1.entity_id)
                        libelle = currentNotef1.libelle
                        somme_taxe = currentNotef1.taxe.tarif
                        if activite.date_fin == None:
                            validate =1
                        else:
                            validate = 0
                    elif entity == 7 and currentNotef1.entity == 7:
                        activite = PubliciteMurCloture.objects.get(id=currentNotef1.entity_id)
                        libelle = currentNotef1.libelle
                        somme_taxe = currentNotef1.taxe.tarif
                        if activite.date_fin == None:
                            validate =1
                        else:
                            validate = 0
                    else:
                        validate = 0

                    if validate == 1:
                        new_note = NoteImposition(
                            reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                            entity=currentNotef1.entity,
                            entity_id=currentNotef1.entity_id,
                            annee=nextyear,
                            libelle= libelle,
                            taxe_montant=somme_taxe,
                            taxe_montant_paye=0.00,
                            numero_carte_physique=currentNotef1.numero_carte_physique,
                            nombre_impression=0,
                            date_create=dateTimeNow,
                            date_update=dateTimeNow,
                            date_validate=dateTimeNow,
                            date_print=None,
                            contribuable_id=currentNotef1.contribuable_id,
                            periode_id=next_periode.id,
                            taxe_id=currentNotef1.taxe_id,
                            user_create_id=1,
                            user_print_id=None,
                            user_update_id=1,
                            user_validate_id=1,
                            date_delete=None,
                            motif_delete=None,
                            user_delete_id=None,
                            paiement_externe_file='',
                            etat=True,
                            date_penalite=None,
                            montant_penalite=0,
                            montant_taxe=0,
                            taux_penalite=0,
                            user_penalite_id=None)

                        if nextyear != currentYear+1:
                            try:
                                new_note.save()
                                obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                obj_chrono.save()
                            except:
                                pass

    def create_note_periode_suivante_monsuel(entity, obj, annee=0):
        dateTimeNow = datetime.datetime.now(tz=timezone.utc)
        currentYear = datetime.datetime.now().year
        currentMonth = datetime.datetime.now().month
        currentNoteF = obj.objects.filter(entity=entity).values('entity_id','entity').order_by().annotate(nb_entity_id=Count('entity_id'))

        for crtn in currentNoteF:
            currentNotef1 = obj.objects.filter(entity=entity,entity_id=crtn['entity_id']).order_by('annee','id').last()
            year = currentNotef1.annee
            if currentNotef1.entity == 12 and entity == 12 and crtn['entity_id'] == currentNotef1.entity_id:
                if currentNotef1.annee < currentYear:
                    for anne in range(year, currentYear + 1):
                        if anne < currentYear:
                            if anne == year:
                                periode = currentNotef1.periode_id
                            else:
                                periode = 0

                            for period in range(periode + 1, 13):
                               nextyear = anne
                               next_periode = period
                               rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id,periode_id=period,annee=anne)
                               if rv.count() == 0:
                                   activite = VehiculeActivite.objects.get(id=currentNotef1.entity_id)
                                   if activite.vehicule.actif == True:
                                       new_note = NoteImposition(
                                           reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                           entity=currentNotef1.entity,
                                           entity_id=currentNotef1.entity_id,
                                           annee=nextyear,
                                           libelle=currentNotef1.libelle,
                                           taxe_montant=currentNotef1.taxe.tarif,
                                           taxe_montant_paye=0.00,
                                           numero_carte_physique=currentNotef1.numero_carte_physique,
                                           nombre_impression=0,
                                           date_create=dateTimeNow,
                                           date_update=dateTimeNow,
                                           date_validate=dateTimeNow,
                                           date_print=None,
                                           contribuable_id=currentNotef1.contribuable_id,
                                           periode_id=next_periode,
                                           taxe_id=currentNotef1.taxe_id,
                                           user_create_id=1,
                                           user_print_id=None,
                                           user_update_id=1,
                                           user_validate_id=1,
                                           date_delete=None,
                                           motif_delete=None,
                                           user_delete_id=None,
                                           paiement_externe_file='',
                                           etat=True,
                                           date_penalite=None,
                                           montant_penalite=0,
                                           montant_taxe=0,
                                           taux_penalite=0,
                                           user_penalite_id=None)
                                       new_note.save()
                                       obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                       obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                       obj_chrono.save()

                        if anne == currentYear:
                            for period in range(1,currentMonth + 1):
                                nextyear = anne
                                next_periode = period
                                rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id, periode_id=period, annee=anne)
                                if rv.count() == 0:
                                    activite = VehiculeActivite.objects.get(id=currentNotef1.entity_id)
                                    if activite.vehicule.actif == True:
                                        new_note = NoteImposition(
                                            reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                            entity=currentNotef1.entity,
                                            entity_id=currentNotef1.entity_id,
                                            annee=nextyear,
                                            libelle=currentNotef1.libelle,
                                            taxe_montant=currentNotef1.taxe.tarif,
                                            taxe_montant_paye=0.00,
                                            numero_carte_physique=currentNotef1.numero_carte_physique,
                                            nombre_impression=0,
                                            date_create=dateTimeNow,
                                            date_update=dateTimeNow,
                                            date_validate=dateTimeNow,
                                            date_print=None,
                                            contribuable_id=currentNotef1.contribuable_id,
                                            periode_id=next_periode,
                                            taxe_id=currentNotef1.taxe_id,
                                            user_create_id=1,
                                            user_print_id=None,
                                            user_update_id=1,
                                            user_validate_id=1,
                                            date_delete=None,
                                            motif_delete=None,
                                            user_delete_id=None,
                                            paiement_externe_file='',
                                            etat=True,
                                            date_penalite=None,
                                            montant_penalite=0,
                                            montant_taxe=0,
                                            taux_penalite=0,
                                            user_penalite_id=None)
                                        new_note.save()
                                        obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                        obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                        obj_chrono.save()

                elif currentNotef1.annee == currentYear:
                    for period in range(currentNotef1.periode_id + 1, currentMonth + 1):
                        nextyear = currentNotef1.annee
                        next_periode = period
                        rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id, periode_id=period, annee=year)
                        if rv.count() == 0:
                            activite = VehiculeActivite.objects.get(id=currentNotef1.entity_id)
                            if activite.vehicule.actif == True:
                                new_note = NoteImposition(
                                    reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                    entity=currentNotef1.entity,
                                    entity_id=currentNotef1.entity_id,
                                    annee=nextyear,
                                    libelle=currentNotef1.libelle,
                                    taxe_montant=currentNotef1.taxe.tarif,
                                    taxe_montant_paye=0.00,
                                    numero_carte_physique=currentNotef1.numero_carte_physique,
                                    nombre_impression=0,
                                    date_create=dateTimeNow,
                                    date_update=dateTimeNow,
                                    date_validate=dateTimeNow,
                                    date_print=None,
                                    contribuable_id=currentNotef1.contribuable_id,
                                    periode_id=next_periode,
                                    taxe_id=currentNotef1.taxe_id,
                                    user_create_id=1,
                                    user_print_id=None,
                                    user_update_id=1,
                                    user_validate_id=1,
                                    date_delete=None,
                                    motif_delete=None,
                                    user_delete_id=None,
                                    paiement_externe_file='',
                                    etat=True,
                                    date_penalite=None,
                                    montant_penalite=0,
                                    montant_taxe=0,
                                    taux_penalite=0,
                                    user_penalite_id=None)
                                new_note.save()
                                obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                obj_chrono.save()

            if currentNotef1.entity == 8 and entity == 8 and crtn['entity_id'] == currentNotef1.entity_id:
                if currentNotef1.annee < currentYear:
                    for anne in range(year,currentYear + 1):
                        if anne < currentYear:
                            if anne == year:
                                periode = currentNotef1.periode_id
                            else:
                                periode = 0

                            for period in range(periode +1,13):
                                nextyear = anne
                                next_periode = period
                                rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id,periode_id=period, annee=year)
                                if rv.count() == 0:
                                    allocation = AllocationPlaceMarche.objects.get(id=currentNotef1.entity_id)
                                    if allocation.date_fin == None:
                                        new_note = NoteImposition(
                                            reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                            entity=currentNotef1.entity,
                                            entity_id=currentNotef1.entity_id,
                                            annee=nextyear,
                                            libelle=currentNotef1.libelle,
                                            taxe_montant=currentNotef1.taxe.tarif,
                                            taxe_montant_paye=0.00,
                                            numero_carte_physique=currentNotef1.numero_carte_physique,
                                            nombre_impression=0,
                                            date_create=dateTimeNow,
                                            date_update=dateTimeNow,
                                            date_validate=dateTimeNow,
                                            date_print=None,
                                            contribuable_id=currentNotef1.contribuable_id,
                                            periode_id=next_periode,
                                            taxe_id=currentNotef1.taxe_id,
                                            user_create_id=1,
                                            user_print_id=None,
                                            user_update_id=1,
                                            user_validate_id=1,
                                            date_delete=None,
                                            motif_delete=None,
                                            user_delete_id=None,
                                            paiement_externe_file='',
                                            etat=True,
                                            date_penalite=None,
                                            montant_penalite=0,
                                            montant_taxe=0,
                                            taux_penalite=0,
                                            user_penalite_id=None)
                                        new_note.save()
                                        obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                        obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                        obj_chrono.save()

                        if anne == currentYear:
                            for period in range(1,currentMonth + 1):
                                nextyear = anne
                                next_periode = period
                                rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id, periode_id=period, annee=year)
                                if rv.count() == 0:
                                    allocation = AllocationPlaceMarche.objects.get(id=currentNotef1.entity_id)
                                    if allocation.date_fin == None:
                                        new_note = NoteImposition(
                                            reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                            entity=currentNotef1.entity,
                                            entity_id=currentNotef1.entity_id,
                                            annee=nextyear,
                                            libelle=currentNotef1.libelle,
                                            taxe_montant=currentNotef1.taxe.tarif,
                                            taxe_montant_paye=0.00,
                                            numero_carte_physique=currentNotef1.numero_carte_physique,
                                            nombre_impression=0,
                                            date_create=dateTimeNow,
                                            date_update=dateTimeNow,
                                            date_validate=dateTimeNow,
                                            date_print=None,
                                            contribuable_id=currentNotef1.contribuable_id,
                                            periode_id=next_periode,
                                            taxe_id=currentNotef1.taxe_id,
                                            user_create_id=1,
                                            user_print_id=None,
                                            user_update_id=1,
                                            user_validate_id=1,
                                            date_delete=None,
                                            motif_delete=None,
                                            user_delete_id=None,
                                            paiement_externe_file='',
                                            etat=True,
                                            date_penalite=None,
                                            montant_penalite=0,
                                            montant_taxe=0,
                                            taux_penalite=0,
                                            user_penalite_id=None)
                                        new_note.save()
                                        obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                        obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                        obj_chrono.save()

                elif currentNotef1.annee == currentYear:
                    for period in range(currentNotef1.periode_id +1, currentMonth + 1):
                        nextyear = currentNotef1.annee
                        next_periode = period
                        rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id, periode_id=period, annee=year)
                        if rv.count() == 0:
                            allocation = AllocationPlaceMarche.objects.get(id=currentNotef1.entity_id)
                            if allocation.date_fin == None:
                                print(currentNotef1.annee, period)
                                new_note = NoteImposition(
                                    reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                    entity=currentNotef1.entity,
                                    entity_id=currentNotef1.entity_id,
                                    annee=nextyear,
                                    libelle=currentNotef1.libelle,
                                    taxe_montant=currentNotef1.taxe.tarif,
                                    taxe_montant_paye=0.00,
                                    numero_carte_physique=currentNotef1.numero_carte_physique,
                                    nombre_impression=0,
                                    date_create=dateTimeNow,
                                    date_update=dateTimeNow,
                                    date_validate=dateTimeNow,
                                    date_print=None,
                                    contribuable_id=currentNotef1.contribuable_id,
                                    periode_id=next_periode,
                                    taxe_id=currentNotef1.taxe_id,
                                    user_create_id=1,
                                    user_print_id=None,
                                    user_update_id=1,
                                    user_validate_id=1,
                                    date_delete=None,
                                    motif_delete=None,
                                    user_delete_id=None,
                                    paiement_externe_file='',
                                    etat=True,
                                    date_penalite=None,
                                    montant_penalite=0,
                                    montant_taxe=0,
                                    taux_penalite=0,
                                    user_penalite_id=None)
                                new_note.save()
                                obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                obj_chrono.save()

    def create_note_periode_suivante_trimestriel(entity, obj, annee=0):
        dateTimeNow = datetime.datetime.now(tz=timezone.utc)
        currentYear = datetime.datetime.now().year
        currentMonth = datetime.datetime.now().month
        currentNoteF = obj.objects.filter(entity=entity).values('entity_id', 'entity').order_by().annotate(nb_entity_id=Count('entity_id'))

        for crtn in currentNoteF:
            currentNotef1 = obj.objects.filter(entity=entity, entity_id=crtn['entity_id']).order_by('annee','id').last()
            year = currentNotef1.annee
            if currentNotef1.entity == 11 and entity == 11 and crtn['entity_id'] == currentNotef1.entity_id:
                if currentNotef1.annee < currentYear:
                    if currentNotef1.periode_id != 19:
                        for anne in range(year, currentYear + 1):
                            if anne < currentYear:
                                if anne == year:
                                    periode = currentNotef1.periode_id
                                else:
                                    periode = 12

                                for period in range(periode + 1, 17):
                                   nextyear = anne
                                   next_periode = period
                                   rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id, periode_id=period, annee=anne)
                                   if rv.count() == 0:
                                       activite = VehiculeActivite.objects.get(id=currentNotef1.entity_id)
                                       if activite.vehicule.actif == True:
                                           new_note = NoteImposition(
                                               reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                               entity=currentNotef1.entity,
                                               entity_id=currentNotef1.entity_id,
                                               annee=nextyear,
                                               libelle=currentNotef1.libelle,
                                               taxe_montant=currentNotef1.taxe.tarif,
                                               taxe_montant_paye=0.00,
                                               numero_carte_physique=currentNotef1.numero_carte_physique,
                                               nombre_impression=0,
                                               date_create=dateTimeNow,
                                               date_update=dateTimeNow,
                                               date_validate=dateTimeNow,
                                               date_print=None,
                                               contribuable_id=currentNotef1.contribuable_id,
                                               periode_id=next_periode,
                                               taxe_id=currentNotef1.taxe_id,
                                               user_create_id=1,
                                               user_print_id=None,
                                               user_update_id=1,
                                               user_validate_id=1,
                                               date_delete=None,
                                               motif_delete=None,
                                               user_delete_id=None,
                                               paiement_externe_file='',
                                               etat=True,
                                               date_penalite=None,
                                               montant_penalite=0,
                                               montant_taxe=0,
                                               taux_penalite=0,
                                               user_penalite_id=None)
                                           new_note.save()
                                           obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                           obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                           obj_chrono.save()

                            if anne == currentYear:
                                if int(currentMonth) < 4:
                                    periodelimit = 13
                                elif int(currentMonth) < 3 and int(currentMonth) < 7:
                                    periodelimit = 14
                                elif int(currentMonth) > 6 and int(currentMonth) < 10:
                                    periodelimit = 15
                                elif int(currentMonth) > 9 and int(currentMonth) < 13:
                                    periodelimit = 16

                                for period in range(13,periodelimit +1):
                                    nextyear = anne
                                    next_periode = period
                                    rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id, periode_id=period, annee=anne)
                                    if rv.count() == 0:
                                        activite = VehiculeActivite.objects.get(id=currentNotef1.entity_id)
                                        if activite.vehicule.actif == True:
                                            new_note = NoteImposition(
                                                reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                                entity=currentNotef1.entity,
                                                entity_id=currentNotef1.entity_id,
                                                annee=nextyear,
                                                libelle=currentNotef1.libelle,
                                                taxe_montant=currentNotef1.taxe.tarif,
                                                taxe_montant_paye=0.00,
                                                numero_carte_physique=currentNotef1.numero_carte_physique,
                                                nombre_impression=0,
                                                date_create=dateTimeNow,
                                                date_update=dateTimeNow,
                                                date_validate=dateTimeNow,
                                                date_print=None,
                                                contribuable_id=currentNotef1.contribuable_id,
                                                periode_id=next_periode,
                                                taxe_id=currentNotef1.taxe_id,
                                                user_create_id=1,
                                                user_print_id=None,
                                                user_update_id=1,
                                                user_validate_id=1,
                                                date_delete=None,
                                                motif_delete=None,
                                                user_delete_id=None,
                                                paiement_externe_file='',
                                                etat=True,
                                                date_penalite=None,
                                                montant_penalite=0,
                                                montant_taxe=0,
                                                taux_penalite=0,
                                                user_penalite_id=None)
                                            new_note.save()
                                            obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                            obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                            obj_chrono.save()
                    else:
                        if currentMonth == 1:
                            for anne in range(year, currentYear + 1):
                                if anne < currentYear:
                                    nextyear = anne
                                    rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id, periode_id=period, annee=anne)
                                    if rv.count() == 0:
                                        activite = VehiculeActivite.objects.get(id=currentNotef1.entity_id)
                                        if activite.vehicule.actif == True:
                                            new_note = NoteImposition(
                                                reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                                entity=currentNotef1.entity,
                                                entity_id=currentNotef1.entity_id,
                                                annee=nextyear,
                                                libelle=currentNotef1.libelle,
                                                taxe_montant=currentNotef1.taxe.tarif,
                                                taxe_montant_paye=0.00,
                                                numero_carte_physique=currentNotef1.numero_carte_physique,
                                                nombre_impression=0,
                                                date_create=dateTimeNow,
                                                date_update=dateTimeNow,
                                                date_validate=dateTimeNow,
                                                date_print=None,
                                                contribuable_id=currentNotef1.contribuable_id,
                                                periode_id=19,
                                                taxe_id=currentNotef1.taxe_id,
                                                user_create_id=1,
                                                user_print_id=None,
                                                user_update_id=1,
                                                user_validate_id=1,
                                                date_delete=None,
                                                motif_delete=None,
                                                user_delete_id=None,
                                                paiement_externe_file='',
                                                etat=True,
                                                date_penalite=None,
                                                montant_penalite=0,
                                                montant_taxe=0,
                                                taux_penalite=0,
                                                user_penalite_id=None)
                                            new_note.save()
                                            obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                            obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                            obj_chrono.save()

                elif currentNotef1.annee == currentYear:
                    if int(currentMonth) < 4:
                        periodelimit = 13
                    elif int(currentMonth) > 3 and int(currentMonth) < 7:
                        periodelimit = 14
                    elif int(currentMonth) > 6 and int(currentMonth) < 10:
                        periodelimit = 15
                    elif int(currentMonth) > 9 and int(currentMonth) < 13:
                        periodelimit = 16

                    for period in range(currentNotef1.periode_id + 1, periodelimit + 1):
                        nextyear = currentNotef1.annee
                        next_periode = period
                        rv = obj.objects.filter(entity=entity, entity_id=currentNotef1.entity_id, periode_id=period, annee=year)
                        if rv.count() == 0:
                            activite = VehiculeActivite.objects.get(id=currentNotef1.entity_id)
                            if activite.vehicule.actif == True:
                                new_note = NoteImposition(
                                    reference=ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION),
                                    entity=currentNotef1.entity,
                                    entity_id=currentNotef1.entity_id,
                                    annee=nextyear,
                                    libelle=currentNotef1.libelle,
                                    taxe_montant=currentNotef1.taxe.tarif,
                                    taxe_montant_paye=0.00,
                                    numero_carte_physique=currentNotef1.numero_carte_physique,
                                    nombre_impression=0,
                                    date_create=dateTimeNow,
                                    date_update=dateTimeNow,
                                    date_validate=dateTimeNow,
                                    date_print=None,
                                    contribuable_id=currentNotef1.contribuable_id,
                                    periode_id=next_periode,
                                    taxe_id=currentNotef1.taxe_id,
                                    user_create_id=1,
                                    user_print_id=None,
                                    user_update_id=1,
                                    user_validate_id=1,
                                    date_delete=None,
                                    motif_delete=None,
                                    user_delete_id=None,
                                    paiement_externe_file='',
                                    etat=True,
                                    date_penalite=None,
                                    montant_penalite=0,
                                    montant_taxe=0,
                                    taux_penalite=0,
                                    user_penalite_id=None)
                                new_note.save()
                                obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
                                obj_chrono.last_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
                                obj_chrono.save()

    def create_note_periode_suivante_impot_foncier(expertise):
        dateTimeNow = datetime.datetime.now(tz=timezone.utc)
        new_chrono = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)
        obj_chrono = Chrono.objects.get(prefixe=CHRONO_NOTE_IMPOSITION)
        obj_chrono.last_chrono = new_chrono
        obj_chrono.save()

        objexp = get_object_or_404(FoncierExpertise, pk=expertise)
        libelle = 'Impôt foncier de la parcelle n°' + objexp.parcelle.numero_parcelle

        new_note = NoteImposition(
            reference=new_chrono,
            entity=ENTITY_IMPOT_FONCIER,
            entity_id=objexp.id,
            annee=objexp.annee,
            libelle=libelle,
            taxe_montant=objexp.parcelle.taxe,
            taxe_montant_paye=0.00,
            numero_carte_physique=None,
            nombre_impression=0,
            date_create=dateTimeNow,
            date_update=dateTimeNow,
            date_validate=dateTimeNow,
            date_print=None,
            contribuable_id=objexp.parcelle.contribuable,
            periode_id=PeriodeHelpers.getCurrentPeriode(objexp.parcelle.taxe.periode_type),
            taxe_id=objexp.parcelle.taxe,
            user_create_id=1,
            user_print_id=None,
            user_update_id=1,
            user_validate_id=1,
            date_delete=None,
            motif_delete=None,
            user_delete_id=None,
            paiement_externe_file='',
            etat=True,
            date_penalite=None,
            montant_penalite=0,
            montant_taxe=0,
            taux_penalite=0,
            user_penalite_id=None)

        new_note.save()

