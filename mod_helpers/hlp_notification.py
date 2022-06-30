from django.contrib.auth.models import User
from mod_parametrage.models import Notification
from django.db.models import Q

from mod_crm.models import *
from mod_activite.models import *
from mod_foncier.models import *
from mod_finance.models import *
from mod_transport.models import *

class Note:
	def __init__(self, class_name, id, note, title, view_list_name, user_create, date_create, reponse_note=None, demande_annulation_validation=False):
		self.class_name = class_name
		self.id = id
		self.note = note
		self.title = title
		self.view_list_name = view_list_name
		self.user_create = user_create
		self.date_create = date_create
		self.reponse_note = reponse_note
		self.demande_annulation_validation = demande_annulation_validation

class NotificationHelpers():
	"""
	Classe herlpers de lecture des notifications(message/autorisation) de l'utilisateur connecté
	"""
	def load_list(entity, query, title, note_lst):
		lst = entity.objects.filter(query).order_by('-date_create').exclude(note__exact='')
		for obj in lst:
			if obj.user_note:
				user = obj.user_note
			else:
				user = obj.user_create

			if obj.date_note:
				date = obj.date_note
			else:
				date = obj.date_create

			reponse = obj.reponse_note
			dem_valid_annul = obj.demande_annulation_validation

			note = Note(obj.class_name, obj.id, obj.note, title, obj.view_list_name, user, date, reponse, dem_valid_annul)
			note_lst.append(note)

		return note_lst

	def get_list(request):
		"""
		lire la liste de toutes les notes de l'utilisateur connecté
		"""
		note_lst = []
		query = Q(note__isnull=False) & Q(user_create=request.user.id)
		# mod_crm
		note_lst = NotificationHelpers.load_list(PersonnePhysique, query, 'Pesonne physique', note_lst)
		note_lst = NotificationHelpers.load_list(PersonneMorale, query, 'Personne morale', note_lst)
		
		# mod_transport
		note_lst = NotificationHelpers.load_list(Vehicule, query, 'Véhicule', note_lst)
		note_lst = NotificationHelpers.load_list(VehiculeActivite, query, 'Activité de transport', note_lst)
		note_lst = NotificationHelpers.load_list(VehiculeActiviteDuplicata, query, 'Duplicata carte transport', note_lst)
		note_lst = NotificationHelpers.load_list(VehiculeProprietaire, query, 'Véhicule de propriéte', note_lst)
		note_lst = NotificationHelpers.load_list(VehiculeProprietaireDuplicata, query, 'Duplicata carte propriéte', note_lst)
		
		# mod_activite
		note_lst = NotificationHelpers.load_list(Standard, query, 'Activité standard', note_lst)
		note_lst = NotificationHelpers.load_list(Marche, query, 'Activité marché', note_lst)
		note_lst = NotificationHelpers.load_list(ActiviteExceptionnelle, query, 'Activité exceptionnelle', note_lst)
		note_lst = NotificationHelpers.load_list(VisiteSiteTouristique, query, 'Visite touristique', note_lst)
		note_lst = NotificationHelpers.load_list(AllocationPanneauPublicitaire, query, 'Panneau publicitaire', note_lst)
		note_lst = NotificationHelpers.load_list(PubliciteMurCloture, query, 'Publicite mur/clôture', note_lst)
		note_lst = NotificationHelpers.load_list(AllocationEspacePublique, query, 'Allocation parcelle publique', note_lst)
		note_lst = NotificationHelpers.load_list(AllocationPlaceMarche, query, 'Allocation place marché', note_lst)
		
		# mod_foncier
		note_lst = NotificationHelpers.load_list(FoncierParcelle, query, 'Identification parcelle privée', note_lst)
		note_lst = NotificationHelpers.load_list(FoncierParcellePublique, query, 'Identification parcelle publique', note_lst)
		note_lst = NotificationHelpers.load_list(FoncierExpertise, query, 'Déclaration foncière', note_lst)
		
		# mod_finance
		note_lst = NotificationHelpers.load_list(AvisImposition, query, "Avis d'imposition", note_lst)

		return note_lst
