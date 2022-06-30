from django.conf import settings
from django.db import models

from mod_transport.submodels.model_vehicule import Vehicule
from mod_crm.models import Contribuable
from mod_helpers.hlp_paths import PathsHelpers

class VehiculeProprietaire(models.Model):
    """
    Modele Titre de propriété de véhicule
    Catégorie cible : Vélo et Vélo moteur
    Remarque : Seul les véihicule SANS PLAQUE d'IMMATRICULATION ou CARTE ROSE paie l'impôt sur le properiétaire et 
    possède obligatoirement une carte de propriétaire.
    L'impôt se paie ANNUELLEMENT
    """

    # Numéro de référence généré chronologiquement (voir parametre chrono)
    # Et qui sera le numéro de la carte de propriétaire
    numero_carte = models.CharField(max_length=50, unique=True)

    # Identifiant du véhicule sans carte rose (sans plaque d'immatriculation)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)

    # Propriétaire du véhicule (Le véhicule peut appartenir à un autre contribuable)
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE, verbose_name="Contribuable")

    #--------------------------------------------------------
    # --------------- CONTROLE D'IMPRESSION -----------------
    #--------------------------------------------------------
    # Numero de la carte physique à resaisir au moment de l'impression pour controler l'authenticité de la carte
    numero_carte_physique = models.CharField(max_length=10, blank=True, null=True)
    
    # Nombre d'impressions (Voir global_variables (PRINT, MAX_NUMBER))
    nombre_impression = models.PositiveSmallIntegerField(default=0)

    #--------------------------------------------------------
    # ----------------- TRAÇABILITÉ -------------------------
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
        ordering = ('-id',)

    def __str__(self):
        return self.numero_carte

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'vehicule_proprietaire_list'