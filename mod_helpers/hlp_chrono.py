from .models import *
from datetime import datetime

class ChronoHelpers():
	"""
	Classe de gestion de numero chronologique
	Modèle : models_chrono.py (Chrono)
	"""
	def last_chrono_to_tab(prefixe, nbr_num, last_chrono):
		nbr_num = nbr_num
		annee_mois = last_crhono[len(prefixe):-nbr_num]
		anne = annee_mois[0:4]
		mois = annee_mois[-2:]

		return

	#Renvoie les prefixes du numéro sans numéro chrono
	def get_num_without_chrono(prefixe):
		res = ''
		obj = Chrono.objects.get(prefixe=prefixe)
		if obj :
			res = obj.prefixe
			if obj.annee :
				res += datetime.now().strftime('%Y')
			if obj.mois :
				res += datetime.now().strftime('%m')

		return res

	#Renvoie le dernier numero
	def get_last_num(prefixe):
		return Chrono.objects.get(prefixe=prefixe)

	#Renvoie le nouveau numéro
	def get_new_num(prefixe):
		obj = ChronoHelpers.get_last_num(prefixe)
		if obj:
			# 1 - Si nouveau mois (comparer le mois en cours avec le dernier mois du last chrono)
			if obj.annee and obj.mois:
				# Get info last chrono
				nombre = obj.nombre
				annee_mois = obj.last_chrono[len(prefixe):-nombre]
				annee = annee_mois[0:4]
				mois = annee_mois[-2:]

				# Get info periode
				annee_new = datetime.now().strftime('%Y')
				mois_new = datetime.now().strftime('%m')
				
				# Comparer le mois 
				if mois != mois_new:
					chrono = ChronoHelpers.get_num_without_chrono(prefixe) #chrono : AI201801
					chrono = chrono + str(1).zfill(obj.nombre) #AI201801000000001
					
					return chrono

			# 2 - Generer new chrono à base de last chrono
			chrono = obj.last_chrono.rstrip()
			if (chrono) != '' :
				chrono = chrono[-obj.nombre:] # chrono : 0000000001
				chrono = int(chrono) + 1 # chrono : 2
				chrono = str(chrono).zfill(obj.nombre) #remplir zero devant, chrono : 000000002
				
				return obj.last_chrono[:-obj.nombre] + chrono #nouveau chrono : AI2018010000000002
			else:
				chrono = ChronoHelpers.get_num_without_chrono(prefixe) #chrono : AI201801
				chrono = chrono + str(1).zfill(obj.nombre) #AI201801000000001
				
				return chrono

		return None