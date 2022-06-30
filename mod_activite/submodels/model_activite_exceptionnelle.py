from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

#from mod_parametrage.models import *
from mod_finance.models import *

class ActiviteExceptionnelle(models.Model):
    """
    Modèle Activité Exceptionnelle (Foire, Spectacle, Bazar de Noel, etc.)
    """
    # Numéro chronologique de l'activité
    numero_activite = models.CharField(max_length=30)
    
    # Le nom du bénéficiaire ou organisateur (personne morale ou physique)
    beneficiaire = models.CharField(max_length=50)
    
    # Motif de la visite (Prendre photo, viste du lieu, Photos mariages)
    motif_activite = models.CharField(max_length=255)
    
    # Date de déivrance de la quittance de paiement ( = quittance d'autorisation)
    date_delivrance = models.DateTimeField()

    # Date d'expiration de la quittance de paiement ( = quittance d'autorisation)
    date_expiration = models.DateTimeField()

    # Référence de la taxe qui est un avis d’imposition (impôt) (tarif paramétré voir Parametrage des Taxe en %)
    taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

    # Le nombre de pièces déclarées (tickets/billets) (5 type de pièce max, ex : adulte, enfant, famille, couple, ...)
    # Les pièces sont en ordre
    piece_nombre_1 = models.PositiveSmallIntegerField(default=0)
    piece_nombre_2 = models.PositiveSmallIntegerField(default=0)
    piece_nombre_3 = models.PositiveSmallIntegerField(default=0)
    piece_nombre_4 = models.PositiveSmallIntegerField(default=0)
    piece_nombre_5 = models.PositiveSmallIntegerField(default=0)

    # le tarif de la pièce (5 type de tarif max, ex : adulte, enfant, famille, couple, ...)
    piece_tarif_1 = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])
    piece_tarif_2 = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])
    piece_tarif_3 = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])
    piece_tarif_4 = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])
    piece_tarif_5 = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])

    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)
    date_validate = models.DateTimeField(null=True)
    date_print = models.DateTimeField(null=True)

    @property
    def montant(self):
        return (self.piece_nombre_1 * self.piece_tarif_1) + (self.piece_nombre_2 * self.piece_tarif_2) + (self.piece_nombre_3 * self.piece_tarif_3) 
        + (self.piece_nombre_4 * self.piece_tarif_5) + (self.piece_nombre_5 * self.piece_tarif_5)

    @property
    def net(self):
        return (self.montant * self.taxe.tarif) / 100
    
    #--------------------------------------------------------
    #------------------ TRAÇABILITÉ -------------------------
    #--------------------------------------------------------
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
    # Ecriture des AI
    date_ecriture = models.DateTimeField(null=True)

    user_ecriture = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_ecriture', null=True)

    class Meta:
        ordering = ('-id', )
        
    def __str__(self):
        return self.numero_activite

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'activite_exceptionnelle_list'