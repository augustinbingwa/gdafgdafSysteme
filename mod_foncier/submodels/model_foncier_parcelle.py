from django.conf import settings
from django.db import models

from mod_crm.models import Contribuable
from mod_finance.models import Taxe
from mod_parametrage.models import *

from mod_helpers.hlp_paths import PathsHelpers

def path_fichier_declaration(instance, filename):
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.DECLARATION_FONCIER_FOLDER)

class FoncierParcelle(models.Model):
    """
    Modèle d'identification de parcelle privée
    Ceci est utilisé dans la gestion privée des impôts fonciers
    """
    # Identifiant de la parcelle (numéro chronologique)
    numero_parcelle = models.CharField(max_length=15, unique=True)

    # Le propriétaire de la parcelle
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE)

    # Le matière imposable (taxe)
    taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

    adresse = models.ForeignKey(Quartier, on_delete=models.CASCADE)

    numero_rueavenue = models.ForeignKey(RueOuAvenue, on_delete=models.CASCADE)

    numero_police = models.CharField(max_length=15, blank=True, null=True)

    # Définir préalablement l'acces pricipal (ceci afin de faciliter le fitrage des caractéristiques des contructions)
    accessibilite = models.ForeignKey(Accessibilite, on_delete=models.CASCADE)

    #Le fichier numérisé des déclarations
    fichier_declaration = models.FileField(upload_to=path_fichier_declaration, max_length=255, null=True, blank=True)
    
    #--------------------------------------------------------
    # -------------- CONTROLE D'IMPRESSIONS -----------------
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
        return self.numero_parcelle

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'foncier_parcelle_list'

# ------------------------------------------------------------------------------
class FoncierParcelleTransfert(models.Model):
    """
    Modèle d'identification de parcelle privée
    Ceci est utilisé dans la gestion privée des impôts fonciers
    """
    # Identifiant de la parcelle (numéro chronologique)
    numero_parcelle = models.CharField(max_length=15, unique=True)
    
    # Le propriétaire de la parcelle
    contribuable_exi = models.ForeignKey(Contribuable, on_delete=models.CASCADE)
    contribuable_nv = models.IntegerField(default=0)

    # Le matière imposable (taxe)
    taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

    adresse = models.ForeignKey(Quartier, on_delete=models.CASCADE)

    numero_rueavenue = models.ForeignKey(RueOuAvenue, on_delete=models.CASCADE)

    numero_police = models.CharField(max_length=15, blank=True, null=True)

    # Définir préalablement l'acces pricipal (ceci afin de faciliter le fitrage des caractéristiques des contructions)
    accessibilite = models.ForeignKey(Accessibilite, on_delete=models.CASCADE)

    #Le fichier numérisé des déclarations
    fichier_declaration = models.FileField(upload_to=path_fichier_declaration, max_length=255, null=True, blank=True)
    
    #--------------------------------------------------------
    # -------------- CONTROLE D'IMPRESSIONS -----------------
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
        return self.numero_parcelle

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'foncier_parcelle_list'