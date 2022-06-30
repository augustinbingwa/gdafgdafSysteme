import datetime

from django.db.models import Q

from mod_finance.models import Periode, PeriodeType
from mod_parametrage import enums


def get_year_from_next_periode(current_periode, current_year):
    """
    Lire l'année de la période suivante
    """
    year = current_year
    nxt_periode = get_next_period(current_periode)
    if nxt_periode:
        if nxt_periode.element == enums.ANNEE:
            year += 1
        elif nxt_periode.element < current_periode.element:
            year += 1

    return year

def get_first_month(periode):
    """
    Renvoie le 1er mois du trimestre
    """
    res = 0
    if isinstance(periode, Periode):
        # TRIMESTRE
        if periode.element == enums.PREMIER_TRIMESTRE:
            res = 1  # 15 Janvier
        elif periode.element == enums.DEUXIEME_TRIMESTRE:
            res = 4  # 15 Avril
        elif periode.element == enums.TROISIEME_TRIMESTRE:
            res = 7  # 15 Juillet
        elif periode.element == enums.QUATRIEME_TRIMESTRE:
            res = 10  # 15 Octobre
        # SEMESTRE
        # elif periode.element == PREMIER_SEMESTRE:
        #     res = 1  # Janvier
        # elif periode.element == DEUXIEME_SEMESTRE:
        #     res = 7  #  Juillet
        # ANNUEL
        elif periode.element == enums.ANNEE:
            res = 3  # 31 Mars

    return res

def get_extreme_element(periode, first=False):
    """
    Renvoie le 1er mois du trimestre
    """
    res = 0
    if isinstance(periode, Periode):
        # MENSUEL
        if periode.element in range(enums.JANVIER, enums.DECEMBRE + 1):
            if first:
                res = enums.JANVIER
            else:
                res = enums.DECEMBRE
        # TRIMESTRE
        elif periode.element in [
            enums.PREMIER_TRIMESTRE,
            enums.DEUXIEME_TRIMESTRE,
            enums.TROISIEME_TRIMESTRE,
            enums.QUATRIEME_TRIMESTRE,
        ]:
            if first:
                res = enums.PREMIER_TRIMESTRE
            else:
                res = enums.QUATRIEME_TRIMESTRE
        # SEMESTRE
        # elif periode.element  in [PREMIER_SEMESTRE, enums.DEUXIEME_SEMESTRE]:
        #     res = enums.DEUXIEME_SEMESTRE
        # ANNUEL
        elif periode.element == enums.ANNEE:
            res = enums.ANNEE

    return res


def get_current_period(obj_periode_type, date=None):
    """
    Lire automatiquement la période en cours selon 'obj_periode_type'
    """
    obj = obj_periode_type
    query = Q()
    if obj and isinstance(obj, PeriodeType):
        if isinstance(date, datetime.date):
            mois = date.month
        else:
            mois = datetime.datetime.now().month

        query = Q(periode_type=obj.id)

        if obj.categorie == enums.MENSUELLE:
            query &= Q(element=mois)

        elif obj.categorie == enums.TRIMSTRIELLE:
            if mois <= 3:
                query &= Q(element=enums.PREMIER_TRIMESTRE)

            elif mois <= 6:
                query &= Q(element=enums.DEUXIEME_TRIMESTRE)

            elif mois <= 9:
                query &= Q(element=enums.TROISIEME_TRIMESTRE)

            elif mois <= 12:
                query &= Q(element=enums.QUATRIEME_TRIMESTRE)

        elif obj.categorie == enums.SEMESTRIELLE:
            if mois <= 6:
                query &= Q(element=enums.PREMIER_SEMESTRE)

            elif mois <= 12:
                query &= Q(element=enums.DEUXIEME_SEMESTRE)

        elif obj.categorie == enums.ANNUELLE:
            query &= Q(element=enums.ANNEE)

    return Periode.objects.filter(query).first()


def get_next_period(current_periode, check_year=False):
    """
    Lire la période suivante
    current_periode : la période courante
    """
    is_next_year = False
    periode = None
    obj = Periode.objects.get(id=current_periode.id)
    lst = Periode.objects.filter(periode_type=obj.periode_type).order_by("element")

    if current_periode.element == get_extreme_element(
        current_periode, first=False
    ):  # IF last
        nxt_p = get_extreme_element(current_periode, first=True)
        is_next_year = True
    else:
        nxt_p = current_periode.element + 1
    for p in lst:
        if p.element == nxt_p:
            periode = p
            break

    if periode is None:
        periode = Periode.objects.get(element=current_periode.element)

    if check_year:
        return periode, is_next_year
    else:
        return periode


def get_month_gte_trimestre_qs(monthly_period):
    if (
        monthly_period
        and isinstance(monthly_period, Periode)
        and monthly_period.periode_type.categorie == enums.MENSUELLE
    ):
        if monthly_period.element in [enums.JANVIER, enums.FEVRIER, enums.MARS]:
            return Q(periode__element=enums.PREMIER_TRIMESTRE)
        elif monthly_period.element in [enums.AVRIL, enums.MAI, enums.JUIN]:
            return Q(periode__element=enums.DEUXIEME_TRIMESTRE)
        elif monthly_period.element in [enums.JUILLET, enums.AOUT, enums.SEPTEMBRE]:
            return Q(periode__element=enums.TROISIEME_TRIMESTRE)
        elif monthly_period.element in [enums.OCTOBRE, enums.NOVEMBRE, enums.DECEMBRE]:
            return Q(periode__element=enums.QUATRIEME_TRIMESTRE)
