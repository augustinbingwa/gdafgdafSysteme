from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from mod_transport.submodels.model_vehicule import Vehicule
from mod_crm.models import Contribuable
from mod_helpers.hlp_paths import PathsHelpers

from decimal import Decimal

def path_fichier_vehicule_activite_carterose(instance, filename):
    """
    Parametrage du path de la carte rose du véhicule
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.VEHICULE_ACTIVITE_CARTEROSE_FOLDER)

def path_fichier_vehicule_activite_autorisation(instance, filename):
    """
    Parametrage du path de l'autorisation de transport
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.VEHICULE_ACTIVITE_AUTORISATION_FOLDER)

def path_fichier_formulaire_arret(instance, filename):
    """
    Parametrage du path du scan du formulaire d'arrêt de service
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.VEHICULE_ACTIVITE_FORMULAIRE_ARRET_FOLDER)

def path_fichier_formulaire_arret_activite_vehicule(instance, filename):
    """
    Parametrage du path du scan du formulaire d'arrêt de service
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.VEHICULE_ACTIVITE_FORMULAIRE_ARRET_FOLDER)

class VehiculeActivite(models.Model):
    """
    Modèle activité de transport rémununéré du véhicule
    Remarque : Seul le véhicule qui exerce une activité de transport rémunéré est géré ici
    Le paiement se fait selon la catégorie du véhicule (trimestriel, annuel, ...)
    """

    # Numéro de référence de l'activité généré chronologiquement (voir parametre chrono)
    # Et qui sera le numéro de la carte d'activité de transport rémunéré
    numero_activite = models.CharField(max_length=30, unique=True)

    # Date début de l'activité
    date_debut = models.DateField()

    # Identifiant du véhicule UNIQUEMENT avec carte rose (plaque d'immatriculation)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)

    # Propriétaire du véhicule (Le véhicule peut appartenir à un autre contribuable)
    # En mode save (création/update), il modifiera le contribuable du vehicule.contribuable
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE)

    # Numéro de chassis du véhicule (Cela pourrait changer si le véhicule change de moteur)
    chassis = models.CharField(max_length=17, blank=True, null=True)

    # Solde de départ (montant des arrierés)
    solde_depart = models.DecimalField(decimal_places=2, max_digits=10, default = 0.00, validators=[MinValueValidator(Decimal('0.00'))])
    
    # Fichier carte rose du véhicule (La carte rose peut changer d'informations d'un propriétaire à l'autre)
    fichier_carterose = models.FileField(upload_to=path_fichier_vehicule_activite_carterose, max_length=255, null=True, blank=True)

    # Fichier d'autorisation de transport venant du Ministère de Commerce
    fichier_autorisation = models.FileField(upload_to=path_fichier_vehicule_activite_autorisation, max_length=255, null=True, blank=True)

    #--------------------------------------------------------
    #------------- ARRET D'ACTIVITE OU SERVICE --------------       
    #--------------------------------------------------------
    # Motif d'arrête de service
    motif = models.CharField(max_length=100, blank=True, null=True) 

    # Date fin/d'arrêt de l'activité, C'est l'arret de service qui le mettra à jour, et Vehicule.actif = False
    date_fin = models.DateField(blank=True, null=True)
    
    # Un formulaire d'arrêt d'activité à remplir mannuellement et à joindre,
    fichier_formulaire_arret = models.FileField(upload_to=path_fichier_formulaire_arret_activite_vehicule, max_length=255, null=True, blank=True) 
   
    #--------------------------------------------------------
    #--------------- CONTROLE D'IMPRESSIONS -----------------
    #--------------------------------------------------------
    # Numero de la carte physique à resaisir au moment de l'impression pour controler l'authenticité de la carte
    numero_carte_physique = models.CharField(max_length=10, blank=True, null=True)

    # Nombre d'impressions (Voir global_variables (PRINT, MAX_NUMBER))
    nombre_impression = models.PositiveSmallIntegerField(default=0)

    #--------------------------------------------------------
    #------------------ TRAÇABILITÉ -------------------------
    #--------------------------------------------------------
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)
    date_validate = models.DateTimeField(null=True)
    date_print = models.DateTimeField(null=True)
    
    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_created')
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_updated', null=True)
    user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='%(class)s_requests_validate', null=True)
    user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='%(class)s_requests_print', null=True)

    #-------------------------------------------------------
    #------------------- NOTE ET REPONSE -------------------
    #-------------------------------------------------------
    # Note envoyée par un autre user ou lui même
    note = models.CharField(max_length=255, blank=True, null=True)
    user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='%(class)s_requests_note', null=True)
    date_note = models.DateTimeField(null=True)

    # Réponse de la note par l'user de création
    reponse_note = models.CharField(max_length=255, blank=True, null=True)

    # Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
    demande_annulation_validation = models.BooleanField(default=False)

    # Traçabilité de l'annulation
    date_cancel = models.DateTimeField(null=True)
    user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='%(class)s_requests_cancel', null=True)
    user_arret = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_arret', null=True)

    # -------------------------------------------------------
    # Ecriture des AI et NI
    date_ecriture = models.DateTimeField(null=True)

    user_ecriture = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_ecriture', null=True)
    
    @property
    def is_ecriture_valid(self):
        """
        Si l'écriture a été générée (validée)
        """
        return self.date_ecriture and self.user_ecriture

    # Si déjà imprimé
    @property
    def is_printed(self):
        if self.nombre_impression>0 and self.date_print is not None and self.user_print is not None:
            return True

        return False

    class Meta:
        ordering = ('-id', )

    def __str__(self):
        return self.numero_activite

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'vehicule_activite_list'



class VehiculeActiviteArret(models.Model):
    """
    Modèle activité de transport rémununéré du véhicule
    Remarque : Seul le véhicule qui exerce une activité de transport rémunéré est géré ici
    Le paiement se fait selon la catégorie du véhicule (trimestriel, annuel, ...)
    """

    # Numéro de référence de l'activité généré chronologiquement (voir parametre chrono)
    # Et qui sera le numéro de la carte d'activité de transport rémunéré
    numero_activite = models.CharField(max_length=30, unique=True)

    # Date début de l'activité
    date_debut = models.DateField()

    # Identifiant du véhicule UNIQUEMENT avec carte rose (plaque d'immatriculation)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)

    # Propriétaire du véhicule (Le véhicule peut appartenir à un autre contribuable)
    # En mode save (création/update), il modifiera le contribuable du vehicule.contribuable
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE)

    # Numéro de chassis du véhicule (Cela pourrait changer si le véhicule change de moteur)
    chassis = models.CharField(max_length=17, blank=True, null=True)

    # Solde de départ (montant des arrierés)
    solde_depart = models.DecimalField(decimal_places=2, max_digits=10, default = 0.00, validators=[MinValueValidator(Decimal('0.00'))])
    
    # Fichier carte rose du véhicule (La carte rose peut changer d'informations d'un propriétaire à l'autre)
    fichier_carterose = models.FileField(upload_to=path_fichier_vehicule_activite_carterose, max_length=255, null=True, blank=True)

    # Fichier d'autorisation de transport venant du Ministère de Commerce
    fichier_autorisation = models.FileField(upload_to=path_fichier_vehicule_activite_autorisation, max_length=255, null=True, blank=True)

    #--------------------------------------------------------
    #------------- ARRET D'ACTIVITE OU SERVICE --------------       
    #--------------------------------------------------------
    # Motif d'arrête de service
    motif = models.CharField(max_length=100, blank=True, null=True) 

    # Date fin/d'arrêt de l'activité, C'est l'arret de service qui le mettra à jour, et Vehicule.actif = False
    date_fin = models.DateField(blank=True, null=True)
    
    # Un formulaire d'arrêt d'activité à remplir mannuellement et à joindre,
    fichier_formulaire_arret = models.FileField(upload_to=path_fichier_formulaire_arret_activite_vehicule, max_length=255, null=True, blank=True)
   
    #--------------------------------------------------------
    #--------------- CONTROLE D'IMPRESSIONS -----------------
    #--------------------------------------------------------
    # Numero de la carte physique à resaisir au moment de l'impression pour controler l'authenticité de la carte
    numero_carte_physique = models.CharField(max_length=10, blank=True, null=True)

    # Nombre d'impressions (Voir global_variables (PRINT, MAX_NUMBER))
    nombre_impression = models.PositiveSmallIntegerField(default=0)

    #--------------------------------------------------------
    #------------------ TRAÇABILITÉ -------------------------
    #--------------------------------------------------------
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)
    date_validate = models.DateTimeField(null=True)
    date_print = models.DateTimeField(null=True)
    
    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_updated', null=True)
    user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='%(class)s_requests_validate', null=True)
    user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_print', null=True)
    user_arret = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_arret', null=True)

    #-------------------------------------------------------
    #------------------- NOTE ET REPONSE -------------------
    #-------------------------------------------------------
    # Note envoyée par un autre user ou lui même
    note = models.CharField(max_length=255, blank=True, null=True)
    user_note = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='%(class)s_requests_note', null=True)
    date_note = models.DateTimeField(null=True)

    # Réponse de la note par l'user de création
    reponse_note = models.CharField(max_length=255, blank=True, null=True)

    # Demande d'annulation de validation par l'user de création (Si c'est déjà vadidé)
    demande_annulation_validation = models.BooleanField(default=False)

    # Traçabilité de l'annulation
    date_cancel = models.DateTimeField(null=True)
    user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='%(class)s_requests_cancel', null=True)

    # -------------------------------------------------------
    # Ecriture des AI et NI
    date_ecriture = models.DateTimeField(null=True)

    user_ecriture = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_ecriture', null=True) 