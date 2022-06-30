from django.conf import settings
from django.db import models

from mod_crm.models import Contribuable
from mod_helpers.hlp_paths import PathsHelpers
from mod_finance.models import AvisImposition, Taxe
from mod_parametrage.models import *
from mod_activite.submodels.model_activite_parametrage import SiteTouristique

class VisiteSiteTouristique(models.Model):
    """
    Modèle Access au site routistique (Accès temporaire pour prendre des visites ou prise de photo)
    """
    # Numéro chronologique 
    numero_visite = models.CharField(max_length=30)

    # Le lieu touristique
    site_touristique = models.ForeignKey(SiteTouristique, on_delete=models.CASCADE)

    # Le nom du bénéficiaire/visiteur ou organisateur (personne morale ou physique)
    beneficiaire = models.CharField(max_length=50)

    # Motif de la visite (Prendre photo, viste du lieu, Photos mariages)
    motif_visite = models.CharField(max_length=255)
    
    # Date de déivrance de la quittance de paiement ( = quittance d'autorisation)
    date_delivrance = models.DateTimeField()

    # Date d'expiration de la quittance de paiement ( = quittance d'autorisation)
    date_expiration = models.DateTimeField()

    # Référence de la taxe qui est un avis d’imposition (impôt) (tarif paramétré voir Parametrage des Taxe)
    taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

    # -------------------------------------------------------
    # Note (information à rajouter ou à signaler)
    note = models.CharField(max_length=255, blank=True, null=True)

    #--------------------------------------------------------
    #------------------ TRAÇABILITÉ -------------------------
    #--------------------------------------------------------
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)
    date_validate = models.DateTimeField(null=True)
    date_print = models.DateTimeField(null=True)
    
    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='%(class)s_requests_created',null=True)
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='%(class)s_requests_updated', null=True)
    user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='%(class)s_requests_validate',null=True)
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
    # Ecriture des AI
    date_ecriture = models.DateTimeField(null=True)

    user_ecriture = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_ecriture', null=True)

    class Meta:
        ordering = ('-id', )
        
    def __str__(self):
        return self.numero_visite

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'visite_site_touristique_list'