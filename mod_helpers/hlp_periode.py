from django.db.models import Q
from mod_parametrage.enums import * 
from mod_finance.models import PeriodeType, Periode
import datetime
from datetime import date

class PeriodeHelpers():
	"""
	Gestion des périodes
	"""
	def getPeriodeByElement(element):
		"""
		Chercher la période selon l'élément de la periode 
		JANVIER, FEVRIER, PREMIER_TRIMESTRE, ...
		"""
		return Periode.objects.get(element = element)

	def getCurrentPeriode(obj_periode_type, date=None):
		"""
		Lire automatiquement la période en cours selon 'obj_periode_type'
		"""
		obj = obj_periode_type
		if obj and isinstance(obj, PeriodeType):
			if isinstance(date, datetime.date):
				mois = date.month
			else:
				mois = datetime.datetime.now().month
			
			query = Q(periode_type = obj.id)

			if obj.categorie == MENSUELLE:
				query &= Q(element = mois)

			elif obj.categorie == TRIMSTRIELLE:
				if mois<=3:
					query &= Q(element = PREMIER_TRIMESTRE)
				
				elif mois<=6:
					query &= Q(element = DEUXIEME_TRIMESTRE)
					
				elif mois<=9:
					query &= Q(element = TROISIEME_TRIMESTRE)
					
				elif mois<=12:
					query &= Q(element = QUATRIEME_TRIMESTRE)

			elif obj.categorie == SEMESTRIELLE:
				if mois<=6:
					query &= Q(element = PREMIER_SEMESTRE)					

				elif mois<=12:
					query &= Q(element = DEUXIEME_SEMESTRE)					
				
			elif obj.categorie == ANNUELLE:
				query &= Q(element = ANNEE)

		return Periode.objects.filter(query)[0]

	def getNextPeriode(current_periode):
		"""
		Lire la période suivante
		current_periode : la période courante
		"""
		periode = None
		obj = Periode.objects.get(id=current_periode.id)
		lst = Periode.objects.filter(periode_type=obj.periode_type).order_by('element')
		nxt_p = current_periode.element + 1
		for p in lst:
			if p.element==nxt_p:
				periode = p
				break

		if periode is None:
			if current_periode.element == 12:
				periode = Periode.objects.get(element=1)
			elif current_periode.element == 16:
				periode = Periode.objects.get(element=13)
			elif current_periode.element == 18:
				periode = Periode.objects.get(element=17)
			else:
				periode = Periode.objects.get(element=current_periode.element)

		return periode


	def getYearFromNextPeriode(current_periode, cyrrent_year):
		"""
		Lire l'année de la période suivante
		"""
		year = cyrrent_year
		nxt_periode = PeriodeHelpers.getNextPeriode(current_periode)
		if nxt_periode:
			if nxt_periode.element == ANNEE:
				year += 1
			elif nxt_periode.element < current_periode.element:
				year += 1

		return year

	def getFirstMonthTrimestre(periode):
		"""
		Renvoie le 1er mois du trimestre
		"""
		res = 0
		if isinstance(periode, Periode):
			if periode.element==PREMIER_TRIMESTRE:
				res = 1 # Janvier
			elif periode.element==DEUXIEME_TRIMESTRE:
				res = 4 # Avril
			elif periode.element==TROISIEME_TRIMESTRE:
				res = 7 # Juillet
			elif periode.element==QUATRIEME_TRIMESTRE:
				res = 10 # Octobre

		return res

	def getFirstMonthSemestriel(periode):
		"""
		Renvoie le 1er mois du semestre
		"""
		res = 0
		if isinstance(periode, Periode):
			if periode.element==PREMIER_SEMESTRE:
				res = 1 # Janvier
			elif periode.element==DEUXIEME_SEMESTRE:
				res = 7 # Juillet
		return res