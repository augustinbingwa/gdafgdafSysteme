from django.utils.translation import gettext as _
from django import forms

from mod_foncier.models import FoncierParcelle
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import *
from mod_finance.models import Taxe
from mod_parametrage.models import RueOuAvenue
from mod_parametrage.enums import *

class FoncierParcelleForm(forms.ModelForm):
    """
    Form Identification de la parcelle privée
    """
    class Meta:
        model = FoncierParcelle

        fields = ('numero_parcelle','contribuable','adresse','numero_rueavenue','numero_police', 'accessibilite', 'taxe')

        exclude = ('user_create','user_update', 'user_validate','user_print','date_update','date_validate','date_print',)

        widgets = {
            'numero_parcelle': forms.TextInput(attrs={'readonly':'readonly'}),
        }

        labels = {
            "numero_parcelle":"N° parcelle",
            "contribuable": "Contribuable",
            "adresse": "Adresse de parcelle",
            "numero_rueavenue": "N° de Rue/Avenue",
            "numero_police": "N° police",
            "accessibilite": "Accessibilité",
            "taxe": "Matière imposable",
        }

        help_texts = {
            "numero_parcelle":"Numéro de la parcelle",
            "contribuable": "Information du contribuable",
            "adresse": "Adresse complète du lieu de la parcelle Commune-Zone-Quartier",            
            "numero_rueavenue": "N°/Nom de rue ou de l’avenue",
            "numero_police": "Numéro de porte si existe",
            "accessibilite": "Accès principal de la parcelle",
            "taxe": "Taxe relative à l'impôt foncier",         
        } 

    def __init__(self, *args, **kwargs):
        super(FoncierParcelleForm, self).__init__(*args, **kwargs)

        # Reference de la parcelle : Initialiser le champs numéro de reference avec le nouveau nom chrono
        self.fields['numero_parcelle'].initial = 'Auto - Chorno'
        
        # Taxe sur Impot foncier. type_impot = 1 'Note d'imposition, taxe_filter = choix_taxe_filter.TAXE_IMPOT_FONCIER
        self.fields['taxe'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 1, periode_type__temps = True, taxe_filter = TAXE_IMPOT_FONCIER)

        # Identifiant de l'activité encours
        self._id = int(self.instance.id or 0) 

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        if self._id>0:
            if self.instance.date_validate:
                self.fields['adresse'].widget.attrs['class'] = 'disabled-element'
                self.fields['numero_police'].widget.attrs['class'] = 'disabled-element'
                self.fields['numero_rueavenue'].widget.attrs['class'] = 'disabled-element'
                self.fields['accessibilite'].widget.attrs['class'] = 'disabled-element'
                self.fields['taxe'].widget.attrs['class'] = 'disabled-element'

    def clean_numero_parcelle(self):
        """
        Generer le numero matricule avant save
        """
        numero_parcelle = self.cleaned_data['numero_parcelle']

        # Mode création uniquement
        if self._id == 0:
            numero_parcelle = ChronoHelpers.get_new_num(CHRONO_PARCELLE_PRIVE)

        return numero_parcelle

    def clean(self):
        # Validation des adresses
        adresse = self.cleaned_data.get('adresse')
        numero_rueavenue = self.cleaned_data.get('numero_rueavenue')

        # Adressse obligatoire
        if adresse is None:
            raise forms.ValidationError(_("Veuillez indiquer l'adresse de la parcelle privée."))

        # RueAvenue Obligatoire
        if numero_rueavenue is None:
            raise forms.ValidationError(_("Veuillez indiquer le numéro de rue/avenue/boulevard"))

        # Vérifier la liaison
        if adresse and numero_rueavenue:
            if not is_rue_avenue_exists(adresse, numero_rueavenue):
                raise forms.ValidationError(_("Cette rue-avenue n'existe pas pour l'adresse seléctionnée"))

        return self.cleaned_data

#--------------------------------------------------------
class ImageUploadFoncierParcelleForm(forms.Form):
    """
    Image upload form.
    """
    fichier_declaration = forms.FileField(required=False)