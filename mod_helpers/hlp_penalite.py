from django.shortcuts import get_object_or_404
from mod_finance.models import NoteImposition,Periode
from mod_parametrage.models import Penalite
from decimal import Decimal
from django.utils import timezone
import datetime
from datetime import date



class penalite():
    def ajoutPenalite(entity,obj,check=0):

        if check == 0:
            if int(obj.taxe_montant_paye) < int(obj.taxe_montant):
                taux = calcul_taux(entity, obj)
                if taux > 0:
                    print(obj.reference,'ajout penalite ******************************************************************************************')
                    if entity == 11:
                        montant_penalite = 5000
                    else:
                        diff_montant = obj.taxe_montant - obj.taxe_montant_paye
                        montant_penalite = round(diff_montant * Decimal(taux / 100))

                    montant_taxe = round(obj.taxe_montant + montant_penalite)
                    NoteImposition.objects.filter(entity=entity, entity_id=obj.entity_id).update(
                        montant_penalite=Decimal(montant_penalite),
                        montant_taxe=Decimal(montant_taxe),
                        taux_penalite=taux,
                        date_penalite=datetime.datetime.now().strftime("%Y-%m-%d"),
                        user_penalite_id=1)
        else:
            current_note = NoteImposition.objects.filter(entity=entity)
            for notImpo in current_note:
                if int(notImpo.taxe_montant_paye) < int(notImpo.taxe_montant):
                    if not notImpo.date_penalite:
                        taux = calcul_taux(entity, notImpo)
                        if taux > 0:
                            print(notImpo.reference,
                                  'ajout penalite ******************************************************************************************')
                            if entity == 11:
                                montant_penalite = 5000
                            else:
                                diff_montant = notImpo.taxe_montant - notImpo.taxe_montant_paye
                                montant_penalite = round(diff_montant * Decimal(taux / 100))

                            montant_taxe = round(notImpo.taxe_montant + montant_penalite)
                            NoteImposition.objects.filter(entity=entity, entity_id=notImpo.entity_id).update(
                                montant_penalite=Decimal(montant_penalite),
                                montant_taxe=Decimal(montant_taxe),
                                taux_penalite=taux,
                                date_penalite=datetime.datetime.now().strftime("%Y-%m-%d"),
                                user_penalite_id=1)


class PenaliteHelpers():
    """
    Simule un penalite
    """
    def has_penalite(annee, date_note_imposition,obj):
        """
        Si la date de penalite de la note a subit un penalite.
        Remarque : Seules les pertiodes de "type annuel" peut être traitées ici
        annee : année de déclaration de l'activité, ...
        date_note_imposition : date de validation de la note d'imposition
        """
        TAUX_PENALITE = 0
        TAUX_INTERER = 0
        current_year = datetime.datetime.now().year
        if date_note_imposition:
            if annee < date_note_imposition.year:
                if not obj.date_penalite:
                    datecreate = str(obj.date_create)
                    date_create = tuple([int(x) for x in datecreate[:10].split('-')])
                    if date_create[0] == current_year and obj.user_penalite:
                        date_debut = date(date_note_imposition.year, plt.date_debut.month, plt.date_debut.day)
                        date_fin = date(date_note_imposition.year, plt.date_fin.month, plt.date_fin.day)
                        date_to_test = date(date_create[0], date_create[1],date_create[2])
                        if plt.is_taux_annee_ecoulee == 1:
                            TAUX_PENALITE = int(plt.taux)
                            TAUX_INTERER = 0
                        

                            return TAUX_PENALITE, TAUX_INTERER
                    else:
                        check_taux_penalite = Penalite.objects.filter(is_taux_annee_ecoulee=1)
                        for taux_penalite in check_taux_penalite:
                            TAUX_PENALITE = taux_penalite.taux

                        return int(TAUX_PENALITE),int(TAUX_INTERER)
                else:
                    check_taux_interer = Penalite.objects.filter(is_taux_annee_ecoulee=2)
                    interer = 0
                    for taux_interer in check_taux_interer:
                        interer = taux_interer.taux
                    TAUX_INTERER = interer

                    return TAUX_PENALITE,TAUX_INTERER
            else:
                for plt in Penalite.objects.all():
                    date_debut = date(date_note_imposition.year, plt.date_debut.month, plt.date_debut.day)
                    date_fin = date(date_note_imposition.year, plt.date_fin.month, plt.date_fin.day)
                    date_to_test = date(date_note_imposition.year, date_note_imposition.month, date_note_imposition.day)

                    # Test si date de declaration subit un accroissement
                    if date_debut <= date_to_test <= date_fin:
                        if not obj.date_penalite:
                            if plt.is_taux_annee_ecoulee == 1:
                                TAUX_PENALITE = int(plt.taux)
                                TAUX_INTERER = 0

                            if plt.is_taux_annee_ecoulee == 0:
                                TAUX_PENALITE = 0
                                TAUX_INTERER = 0
                        else:
                            if plt.is_taux_annee_ecoulee == 2:
                                TAUX_PENALITE = 0
                                TAUX_INTERER = int(plt.taux)

                        return TAUX_PENALITE,TAUX_INTERER

        return 0