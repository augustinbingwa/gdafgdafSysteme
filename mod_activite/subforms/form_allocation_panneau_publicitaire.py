from django.utils.translation import gettext as _
from django import forms

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import *
from mod_activite.models import AllocationPanneauPublicitaire
from mod_finance.models import Taxe
from mod_parametrage.enums import *

class AllocationPanneauPublicitaireForm(forms.ModelForm):
    """
    Form Allocation Panneau Publicitaire
    """
    class Meta:
        model = AllocationPanneauPublicitaire

        fields = ('numero_allocation', 'reference_juridique', 'parcelle_publique', 'contribuable', 'superficie', 'taxe', 'date_debut' ,'solde_depart')

        exclude = ('user_create','user_update', 'user_validate', 'user_print', 'date_update', 'date_validate', 'date_print')

        widgets = {
            'numero_allocation': forms.TextInput(attrs={'readonly':'readonly'}),
            'reference_juridique': forms.TextInput(attrs={'placeholder':'La référence juridique du contrat...'}),
            'adresse_precise': forms.TextInput(attrs={'placeholder':"Préciser l'adresse exacte de la parcelle..."}),
        }

        labels = {
            "numero_allocation": "N° allocation",
            "reference_juridique": "Référence juridique",
            "parcelle_publique": "Référence de la parcelle",
            "contribuable": "Contribuable",
            "superficie": "Superficie (m²)",
            "taxe": "Frais de location",
            "date_debut": "Date début",
            "solde_depart" : "Solde de départ",
        }

        help_texts = {
            "numero_allocation": "Numéro chronologique",
            "reference_juridique": "Référence juridique du contrat - ordonnance",
            "parcelle_publique": "Information complète de la parcelle/espace publique",
            "contribuable": "Information du contribuable",
            "superficie": "Supérficie du panneau",
            "taxe": "Matière imposable",
            "date_debut": "Occupation",
            "solde_depart" : "Montant des arriérés",
        }

    def __init__(self, *args, **kwargs):
        super(AllocationPanneauPublicitaireForm, self).__init__(*args, **kwargs)

        # Reference de l'allocation : Initialiser le champs numéro de reference avec le nouveau nom chrono
        self.fields['numero_allocation'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('APP') #APP = Allocation Panneau Publicitaire

        # Taxe sur Allocation de panneau publicitaire. type_impot = 1 'Note d'imposition, taxe_filter = choix_taxe_filter.TAXE_ALLOCATION_PANNEAU_PUBLICITAIRE
        self.fields['taxe'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 1, periode_type__temps = True, taxe_filter = TAXE_ALLOCATION_PANNEAU_PUBLICITAIRE)
         
        # Identifiant de l'activité encours
        self._id = int(self.instance.id or 0)
        
        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        if self._id>0:
            if self.instance.date_validate:
                self.fields['reference_juridique'].widget.attrs['disabled'] = True
                self.fields['superficie'].widget.attrs['disabled'] = True
                self.fields['taxe'].widget.attrs['disabled'] = True
                self.fields['date_debut'].widget.attrs['disabled'] = True
                self.fields['solde_depart'].widget.attrs['disabled'] = True

    def clean_numero_allocation(self):
        """
        Generer le numero matricule avant save
        """
        numero_allocation = self.cleaned_data['numero_allocation']
        
        # Mode création uniquement
        if self._id == 0:
            numero_allocation = ChronoHelpers.get_new_num(CHRONO_ALLOCATION_PANNEAU_PUBLICITAIRE)

        return numero_allocation

    def clean_superficie(self):
        """
        Validation de la superficie   
        """
        superficie = self.cleaned_data.get('superficie')
        
        if superficie <= 0:
           raise forms.ValidationError(_("La supérficie doit être positive."))

        return superficie

    def clean_date_debut(self):
        """
        Validation de la date début de l'activité
        """
        date_debut = self.cleaned_data.get('date_debut')

        if not is_date_valid(date_debut):
            raise forms.ValidationError(_("Date début invalide."))

        return date_debut

class ImageUploadAllocationPanneauPublicitaireForm(forms.Form):
    """Fichier upload form."""
    fichier_lettre_exp_tmp = forms.FileField(required=False)
    fichier_rap_vis_ter = forms.FileField(required=False)