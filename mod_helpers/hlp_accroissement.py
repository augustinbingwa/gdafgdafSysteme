from mod_parametrage.models import Accroissement
from datetime import date

class AccroissementHelpers():
    """
    Simule un accroissement
    """
    def has_accroissement(annee, date_note_imposition):
        """
        Si la date de déclaration de l'activité a subit un acroissement.
        Remarque : Seules les pertiodes de "type annuel" peut être traitées ici
        annee : année de déclaration de l'activité, ...
        date_note_imposition : date de validation de la note d'imposition
        """
        if date_note_imposition:
            if annee < date_note_imposition.year:
                acc = Accroissement.objects.get(is_taux_annee_ecoulee=True)
                return int(acc.taux)
            else:
                for acc in Accroissement.objects.all():
                    date_debut = date(date_note_imposition.year, acc.date_debut.month, acc.date_debut.day)
                    date_fin = date(date_note_imposition.year, acc.date_fin.month, acc.date_fin.day)
                    date_to_test = date(date_note_imposition.year, date_note_imposition.month, date_note_imposition.day)
                    
                    # Test si date de declaration subit un accroissement
                    if date_debut <= date_to_test <= date_fin:
                        return int(acc.taux)

        return 0