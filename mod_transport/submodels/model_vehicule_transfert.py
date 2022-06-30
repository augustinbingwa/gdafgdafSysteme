from django.db import models
from django.conf import settings

from mod_crm.models import Contribuable

from mod_helpers.hlp_paths import PathsHelpers

from mod_transport.models import *

def path_fichier_vehicule_carterose(instance, filename):
    """
    Parametrage du path de la carte rose du véhicule
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.VEHICULE_CARTEROSE_FOLDER)

def path_fichier_vehicule_non_redevabilite(instance, filename):
    """
    Parametrage du path de la non redevabilité pour le transfert du véhicule
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.VEHICULE_NON_REDEVABILITE_FOLDER)

class VehiculeTransfert(models.Model):
    """
    Modèle véhicule
    """
    # Chaque voiture est identifié par une sous catégorie
    # ATTENTION : La sous catégorie détermine les informations clés du véhicule et 
    # que les infos des tâxes en dépendent, alors une fois validé (date_valide) elle ne sera jamais modifiée
    sous_categorie = models.ForeignKey(VehiculeSousCategorie, on_delete=models.PROTECT)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE,null=True)

    # Voiture (ou étrangère => le nombre de caractères de la plaque est variable) 
    locale = models.BooleanField(default=True)

    # Numéro de la plaque du véhicule (Pour les véhicule 'SANS PLAQUE' (velo, velo-moteur) alors il faut generer des
    # numéro chronologique)
    # Remarque : plaque est UNIQUE entre même catégorie (6 caractères pour la voiture locales)
    plaque = models.CharField(max_length=10, blank=True, null=True)

    # Modèle du véhicule, ex : Bmw Série 3, Renault 306, ...
    modele = models.ForeignKey(VehiculeModele, on_delete=models.CASCADE)
    
    #Numéro de chassis du véhicule (Seul les véhicules 'AVEC PLAQUE' ont de numéro de châssis, la fichier est nullable)
    chassis = models.CharField(max_length=17, blank=True, null=True)

    # Propriétaire du véhicule (contribuable par défaut)
    # Remarque : Mis à jour automatique à partir de la création de l'activité de transport rémunéré
    # OU Si c'est véhicule (Vélo/velomoteur) privé,
    contribuable_encien = models.ForeignKey(Contribuable, on_delete=models.CASCADE, related_name='contribuable_encien')
    contribuable_nouveau = models.ForeignKey(Contribuable, on_delete=models.CASCADE, related_name='contribuable_nouveau')

    # Si la voiture exerce une activité (transport rémunéré), par défaut tout est rémunéré
    # SAUF la catgorie de vélo peut ne pas être rémunéré
    remunere = models.BooleanField(default=True)

    # Véhicules qui ont de compte propre (VehiculeCategorie.has_compte_propre = True, et qui n'exerce pas d'activité locale)
    # L'Activité est crée car le stationneent depend de l'activité. (PAr conséquent la Valeur de l'activité est de 0)
    compte_propre = models.BooleanField(default=False)

    # Actif =  Si le véhicule est en période d'activité (Par défaut, l'activité est simplement enregistré)
    # C'est l'arrêt de son activité qui le rend inactif
    # S'il est inactif alors il ne pourra exerce aucune activité. Pour reactivé, il faut lui ouvrir une nouvelle activité
    # Pour les cas des sous catégories (velo privé et velo moteur, actif = False), car il n'exercera jamais d'activité
    actif = models.BooleanField(default=False)

    #Fichier carte rose du véhicule (Seul les véhicules AVEC PLAQUE ont de carte rose, le fichier est nullable)
    #Fichier obligatoire, mais enregisré dans le formulaire upload (il faut une carte rose avant la validation des info du véhicule)
    fichier_carterose = models.FileField(upload_to=path_fichier_vehicule_carterose, max_length=255, null=True, blank=True)
    fichier_non_redevabilite = models.FileField(upload_to=path_fichier_vehicule_non_redevabilite, max_length=255, null=True, blank=True)

    # Traçabilité
    date_create = models.DateTimeField(null=True)
    date_update = models.DateTimeField(null=True)
    date_validate = models.DateTimeField(null=True)
    date_print = models.DateTimeField(null=True)
    date_transfert = models.DateTimeField(null=True)

    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    user_transfert = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_transfert')
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_updated', null=True)
    user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_validate', null=True)
    user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_print', null=True)

    #-------------------------------------------------------
    #------------------- NOTE ET REPONSE -------------------
    #-------------------------------------------------------
    # Note envoyée par un autre user ou lui même
    note = models.CharField(max_length=255, blank=True, null=True)
    user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_note', null=True)
    date_note = models.DateTimeField(null=True)

    # Réponse de la note par l'user de création
    reponse_note = models.CharField(max_length=255, blank=True, null=True)

    # Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
    demande_annulation_validation = models.BooleanField(default=False)
    
    # Traçabilité de l'annulation
    date_cancel = models.DateTimeField(null=True)
    user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_cancel', null=True)

    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return self.plaque + ' - (' + self.modele.nom + ')'

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'vehicule_list'