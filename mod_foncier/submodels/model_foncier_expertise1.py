from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from mod_helpers.hlp_paths import PathsHelpers
from mod_foncier.models import FoncierParcelle, FoncierTnbImpot
from mod_parametrage.models import Accroissement

from datetime import date
from decimal import Decimal

def path_dossier_expertise(instance, filename):
    return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.LETTRE_DEMANDE_ESPACE_EXP_FOLDER)

class FoncierExpertise(models.Model):
    """
    Modèle Expertise technique (descente sur terraint pour vérifier les info des terrains non batîs et batis)
    """   
    # Identifiant de la parcelle privée
    parcelle = models.ForeignKey(FoncierParcelle, on_delete=models.CASCADE)

    # Date de déclaration de l'impôt foncier
    date_declaration = models.DateField()

    # Année de déclaration de l'impôt foncier
    # annee = models.PositiveSmallIntegerField()
    annee = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(2014),
            MaxValueValidator(9999)
        ]
    ) 

    # La superficie non batîes (succeptible d'être changée)
    superficie_non_batie = models.PositiveIntegerField(default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999999)
        ]
    )

    # Référence de l'impôt à payer à chaque
    impot_non_batie = models.ForeignKey(FoncierTnbImpot, on_delete=models.CASCADE)

    # Pièce jointe (PDF) de lexpertise contenant toute les informations approuvées
    dossier_expertise = models.FileField(upload_to=path_dossier_expertise, max_length=255, null=True, blank=True)   

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

    # Traçabilité de l'annulation de la validation
    date_cancel = models.DateTimeField(null=True)
    user_cancel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='%(class)s_requests_cancel', null=True)

    #-------------------------------------------------------
    #--- TRACABILITE DE LA SUPPRESSION DE LA DECLARATION ---
    #-------------------------------------------------------
    date_delete = models.DateTimeField(null=True)
    user_delete = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='%(class)s_requests_delete', null=True)
    motif_delete = models.TextField(max_length=1024, blank=True, null=True)
    etat = models.BooleanField(default=True)

    @property
    def is_deleted(self):
        """
        Si la déclaration est supprimée
        """
        return self.date_delete and self.user_delete

    #-------------------------------------------------------
    #------------------------ MONTANT ----------------------
    #-------------------------------------------------------
    # Montant total des terrains non bâti
    montant_tnb = models.DecimalField(decimal_places=0, max_digits=10, validators=[MinValueValidator(Decimal('0'))], default=0)
    
    # Montant total des terrains bâti ou contruction
    montant_tb = models.DecimalField(decimal_places=0, max_digits=10, validators=[MinValueValidator(Decimal('0'))], default=0)
    
    #-------------------------------------------------------
    #--------------------- ACCROISSEMENT -------------------
    #-------------------------------------------------------
    accroissement_taux = models.DecimalField(decimal_places=1, max_digits=10, validators=[MinValueValidator(Decimal('0.0'))], default=0.0)
    accroissement_montant =models.DecimalField(decimal_places=0, max_digits=10, validators=[MinValueValidator(Decimal('0'))], default=0)

    # -------------------------------------------------------
    # --------------------- PENALITE -------------------
    # -------------------------------------------------------
    penalite_taux = models.DecimalField(decimal_places=1, max_digits=10,validators=[MinValueValidator(Decimal('0.0'))], default=0.0)
    penalite_montant = models.DecimalField(decimal_places=0, max_digits=10,validators=[MinValueValidator(Decimal('0'))], default=0)
    # -------------------------------------------------------
    # --------------------- INTERE -------------------
    # -------------------------------------------------------
    intere_taux = models.DecimalField(decimal_places=1, max_digits=10,validators=[MinValueValidator(Decimal('0.0'))], default=0.0)
    intere_montant = models.DecimalField(decimal_places=0, max_digits=10,validators=[MinValueValidator(Decimal('0'))], default=0)

    @property
    def has_accroissement(self):
        """
        Si la declaration a subit un acroissement
        """
        if self.date_declaration:
            if self.annee<self.date_declaration.year:
                acc = Accroissement.objects.get(is_taux_annee_ecoulee=True)
                return int(acc.taux)
            else:
                for acc in Accroissement.objects.all():
                    date_debut = date(self.date_declaration.year, acc.date_debut.month, acc.date_debut.day)
                    date_fin = date(self.date_declaration.year, acc.date_fin.month, acc.date_fin.day)    

                    # Test si date de declaration subit un accroissement
                    if date_debut <= self.date_declaration <= date_fin:
                        return int(acc.taux)

        return 0
    
    #-------------------------------------------------------
    #---------------- Ecriture des AI et NI ----------------
    #-------------------------------------------------------
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
        index_together = unique_together = [['parcelle', 'annee']]

    def __str__(self):
        return self.parcelle.numero_parcelle + " - " + self.annee.__str__()

    def class_name(self):
        """utilisé pour la note : renvoie le path complet de la classe module_._..._.ClasseName """
        return self.__module__ + '.'+  self.__class__.__name__

    def view_list_name(self):
        """utilisé pour la note"""
        return 'foncier_expertise_list'