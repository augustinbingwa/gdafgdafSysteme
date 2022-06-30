from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from mod_activite.models import DroitPlaceMarche
from mod_crm.models import Contribuable
from mod_finance.models import Taxe

from mod_helpers.hlp_paths import PathsHelpers

from decimal import Decimal

#------------------------------------------------------------
def path_fichier_contrat_marche(instance, filename):
    """
    Répértoire contenant le fichier de contrat d'une place dans le marché
    """
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.ALLOCATION_PLACE_MARCHE_CONTRAT_FOLDER)

#------------------------------------------------------------
class AllocationPlaceMarche(models.Model):
    """
    Modèle Allocation d'une place dans le marché
    Ceci est utilisé dans la gestion d'allocation de la place dans le marché
    """
    # Information du marché + place + coût
    droit_place_marche = models.ForeignKey(DroitPlaceMarche, on_delete=models.CASCADE)
    
    # Identifiant du contribuable
    contribuable = models.ForeignKey(Contribuable, on_delete=models.CASCADE)

    # Référence de la taxe (impôt) (tarif paramétré par m²/place voir Parametrage des Taxe)
    taxe = models.ForeignKey(Taxe, on_delete=models.CASCADE)

    # Date début de l'occupation de la place
    date_debut = models.DateField()

    # Date fin de l'occupation de la place (Mis à jour à partir de l'arrêt service de l'allocation/activité)
    date_fin = models.DateField(blank=True, null=True)
    
    # Solde de départ (montant des arrierés de l'allocation)
    solde_depart = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])

    # le fiche de contrat de l'allocation
    fichier_contrat = models.FileField(upload_to=path_fichier_contrat_marche, max_length=255, blank=True, null=True)

    @property
    def is_occuped(self):
        """
        Si l'allocation est en cours d'occupation
        """
        return (self.date_fin is not None)

    #--------------------------------------------------------
    # ---------------------- CAUTION ------------------------
    #--------------------------------------------------------
    # Si la caution est deja payee ou non
    caution_payee = models.BooleanField(default=None)
    
    # Parametre de la caution se trouve dans le parametre globale
    caution_nombre_mois = models.PositiveSmallIntegerField(default=0)

    # Montant total de la caution (formule : cout de la place * nombre de mois)
    caution_montant = models.DecimalField(decimal_places=0, max_digits=10, default = 0, validators=[MinValueValidator(Decimal('0'))])

    
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
        ordering = ('-id',)

    def __str__(self):
        _contribuable = ' par ' + self.contribuable.matricule + ' - ' + self.contribuable.nom
        return self.droit_place_marche.nom_marche.nom.capitalize() + ' - place n°' + self.droit_place_marche.numero_place + _contribuable

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'allocation_place_marche_list'