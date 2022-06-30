from django.conf import settings
from django.db import models
from mod_parametrage.models import *

class FoncierParcellePublique(models.Model):
    """
    Modèle parcelle pour Foncier Publique
    Ceci est utilisé dans la gestion d'allocation de l'espace publiques et des panneaux publicitaires
    """
    numero_parcelle = models.CharField(max_length=15, unique=True)
    
    # Adresse du panneau (Commune - Zone - Quartier)
    adresse = models.ForeignKey(Quartier, on_delete=models.CASCADE)
    
    # Rue ou Avenue
    numero_rueavenue = models.ForeignKey(RueOuAvenue, on_delete=models.CASCADE)

    # Adresse précise du panneau (en face du, à côté de, ...)
    adresse_precise = models.CharField(max_length=255, blank=True, null=True)

    # Si occupée, ce champs sera mis à jour via la validation l'allocation de l'espace publique seulement
    occupee = models.BooleanField(default=False)

    # Usage de la parcelle publique (USAGE_NEANT=0, USAGE_ACTIVITE=1, USAGE_PANNEAU=2)
    usage = models.IntegerField(choices=choix_usage_parcelle_public, default=USAGE_NEANT)

    #--------------------------------------------------------
    #------------------ TRAÇABILITÉ -------------------------
    #--------------------------------------------------------
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)
    date_validate = models.DateTimeField(null=True)
    date_print = models.DateTimeField(null=True)
    
    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_updated', null=True)
    user_validate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_validate',null=True)
    user_print = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_print', null=True)

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

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.numero_parcelle + ' - ' + str(self.adresse) + ', ' + str(self.numero_rueavenue)

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'foncier_parcelle_publique_list'