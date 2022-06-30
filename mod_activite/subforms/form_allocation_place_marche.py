from django.utils.translation import gettext as _
from django import forms

from mod_helpers.hlp_validators import *

from mod_activite.models import AllocationPlaceMarche, DroitPlaceMarche
from mod_finance.models import Taxe
from mod_parametrage.enums import *

from mod_helpers.hlp_global_variables import GlobalVariablesHelpers

#----------------------------------------------------------------
class AllocationPlaceMarcheForm(forms.ModelForm):
    """
    Form Allocation de Place dans le marché (c'est un contrat, payé mensuellement)
    """
    class Meta:
        model = AllocationPlaceMarche

        fields = ('droit_place_marche','contribuable', 'taxe', 'date_debut', 'solde_depart', 'caution_payee', 'caution_nombre_mois', 'caution_montant', )

        exclude = ('user_create','user_update', 'user_validate','user_print','date_update','date_validate','date_print',)

        widgets = {
            'caution_payee':forms.Select(attrs={'required':'required'}, choices=[(None,"---------"), (True,"La caution a été déjà payeé"),(False,"La caution n'est pas encore payeé")]),
            'caution_nombre_mois': forms.TextInput(attrs={'readonly':'readonly'}),
            'caution_montant': forms.TextInput(attrs={'readonly':'readonly'}),
        }

        labels = {
            "droit_place_marche": "Marché - Place",
            "contribuable": "Contribuable",
            "taxe": "Frais de location",
            "date_debut": "Date début",
            "solde_depart" : "Solde de départ",
            "caution_payee" : "Caution status",
            "caution_nombre_mois" : "Nombre de mois",
            "caution_montant" : "Montant caution",
        }

        help_texts = {
            "droit_place_marche": "Information du marché et de la place",
            "contribuable": "Information du contribuable",
            "taxe": "Matière imposable",
            "date_debut": "Début de l’activité",
            "solde_depart" : "Montant des arriérés",
            "caution_payee" : "Payée ou non",
            "caution_nombre_mois" : "Nombre de mois à payer",
            "caution_montant" : "Le montant total de la caution",
        }

        error_messages = {
            'contribuable': {'required': ('Le contribuable est recquis'),}
        }

    def __init__(self, *args, **kwargs):
        super(AllocationPlaceMarcheForm, self).__init__(*args, **kwargs)

        # Taxe sur Activite Standard/Marché. type_impot = 1 'Note d'imposition, taxe_filter = choix_taxe_filter.TAXE_DROIT_PLACE_MARCHE
        self.fields['taxe'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 1, periode_type__temps = True, taxe_filter = TAXE_ALLOCATION_PLACE_MARCHE)

        # Afficher le nombre de mois de caution (variable gobale)
        self.fields['caution_nombre_mois'].initial = GlobalVariablesHelpers.get_global_variables("ALLOCATION_PLACE_MARCHE", "CAUTION").valeur

        # Identifiant de l'allocation de place encours
        self._id = int(self.instance.id or 0) 

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        if self._id>0:
            if self.instance.date_validate:
                self.fields['taxe'].widget.attrs['class'] = 'disabled-element'
                self.fields['date_debut'].widget.attrs['class'] = 'disabled-element'
                self.fields['solde_depart'].widget.attrs['class'] = 'disabled-element'
                self.fields['caution_payee'].widget.attrs['class'] = 'disabled-element'
                self.fields['caution_nombre_mois'].widget.attrs['class'] = 'disabled-element'
                self.fields['caution_montant'].widget.attrs['class'] = 'disabled-element'

    def clean_droit_place_marche(self):
        """
        Validation de l'a a'llocation de la place dans le marché
        """
        droit_place_marche = self.cleaned_data.get('droit_place_marche')
        
        # Unicité
        if droit_place_marche:
            obj = DroitPlaceMarche.objects.get(id = droit_place_marche.id)
            if obj and obj.occupee :
                raise forms.ValidationError(_("Cette place est déjà occupée."))
        
        return droit_place_marche

    def clean_date_debut(self):
        """
        Validation de la date début de l'activité
        """
        date_debut = self.cleaned_data.get('date_debut')

        if not is_date_valid(date_debut):
            raise forms.ValidationError(_("Date début activité invalide."))

        return date_debut

    def clean_caution_montant(self):
        """
        Calculer la caution
        """
        droit_place_marche = self.cleaned_data.get('droit_place_marche')
        caution_montant = self.cleaned_data.get('caution_montant')
        caution_payee = self.cleaned_data.get('caution_payee')
        caution_nombre_mois = self.cleaned_data.get('caution_nombre_mois')

        if not caution_payee:
            caution_montant = caution_nombre_mois * droit_place_marche.cout_place
        else:
            caution_montant = 0

        return caution_montant

#----------------------------------------------------------------
class FichierUploadAllocationPlaceMarcheForm(forms.Form):
    """
    Fichier upload form.
    """
    fichier_contrat = forms.FileField(required=False)