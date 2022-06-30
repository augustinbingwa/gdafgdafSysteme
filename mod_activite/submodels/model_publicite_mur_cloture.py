from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from mod_crm.models import *
from mod_helpers.hlp_paths import PathsHelpers
from mod_finance.models import Taxe
from mod_parametrage.enums import *

from decimal import Decimal

from django.utils import timezone

def path_fichier_lettre_exp_tmp(instance, filename):
    """
    Repertoire des fichiers des lettres d'eploitation temporaire des panneaux publicitaires
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.MUR_CLOTURE_LETTRE_EXP_TMP)

def path_fichier_rap_vis_ter(instance, filename):
    """
    Repertoire des fichiers des rapport de visite technique des publicité sur les murs et clôtures
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.MUR_CLOTURE_RAP_VIS_TER)

class PubliciteMurCloture(models.Model):
    """
    Modèle des publicités sur les murs et clôtures
    """
    # Numéro de contrat de l'allocation
    numero_allocation = models.CharField(max_length=30)

    # Type de la publicité (Mur ou Cloture)
    type_publicite = models.IntegerField(choices=choix_publicite)

    # Référence juridique
    reference_juridique = models.CharField(max_length=30, unique=True)

    #Adresse du mur/clôture (Commune - Zone - Quartier)
    adresse = models.ForeignKey(Quartier, on_delete=models.CASCADE)
    
    #Rue ou Avenue
    numero_rueavenue = models.ForeignKey(RueOuAvenue, on_delete=models.CASCADE)

    #Adresse précise (en face du, à côté de, ...)
    adresse_precise = models.CharField(max_length=255, blank=True, null=True)

    # Le contribuable (locataire)
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE)
    
    # La superficie du mûr/cloture
    superficie = models.PositiveSmallIntegerField(default=0)

    # Référence de la taxe (impôt) (tarif paramétré par par m² voir Parametrage des Taxe)
    taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

    # Date début de la publicité
    date_debut = models.DateField()

    # Date fin de la publicité (Mis à jour à partir de l'arrêt service de Publicité)
    date_fin = models.DateField(blank=True, null=True)

    #Solde de départ (montant des arrierés)
    solde_depart = models.DecimalField(decimal_places=2, max_digits=10, default = 0.00, validators=[MinValueValidator(Decimal('0.00'))])
    
    # Lettre de demande de l’exploitation temporaire    
    fichier_lettre_exp_tmp = models.FileField(upload_to=path_fichier_lettre_exp_tmp, max_length=255, null=True, blank=True) 
    
    # Rapport de visite du terrain    
    fichier_rap_vis_ter = models.FileField(upload_to=path_fichier_rap_vis_ter, max_length=255, null=True, blank=True)

    #--------------------------------------------------------
    # ----------------- TRAÇABILITÉ -------------------------
    #--------------------------------------------------------
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True)
    date_validate = models.DateTimeField(null=True)
    date_print = models.DateTimeField(null=True)
    
    user_create = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created',null=True)
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

    # -------------------------------------------------------
    # Ecriture des NI
    date_ecriture = models.DateTimeField(null=True)

    user_ecriture = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(class)s_requests_ecriture', null=True)

    @property
    def is_ecriture_valid(self):
        """
        Si l'écriture a été générée (validée)
        """
        return self.date_ecriture and self.user_ecriture

    class Meta:
        ordering = ('-id', )
        
    def __str__(self):
        return self.numero_allocation

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'publicite_mur_cloture_list'