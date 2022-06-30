from django.utils.translation import gettext as _
from django import forms

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import *

from mod_finance.models import Taxe
from mod_activite.models import PubliciteMurCloture
from mod_parametrage.models import RueOuAvenue
from mod_parametrage.enums import *

class PubliciteMurClotureForm(forms.ModelForm):
    """
    Form Allocation Publicité sur les Murs/Clôtures
    """
    class Meta:
        model = PubliciteMurCloture

        fields = ('numero_allocation', 'type_publicite', 'reference_juridique', 'adresse', 'numero_rueavenue', 'adresse_precise', 'contribuable', 'superficie', 'taxe', 'date_debut', 'solde_depart')

        exclude = ('user_create','user_update', 'user_validate', 'user_print', 'date_update', 'date_validate', 'date_print')

        widgets = {
            'numero_allocation': forms.TextInput(attrs={'readonly':'readonly'}),
            'reference_juridique': forms.TextInput(attrs={'placeholder':'La référence juridique du contrat...'}),
            'adresse_precise': forms.TextInput(attrs={'placeholder':"Préciser l'adresse exacte de la parcelle..."}),
        }

        labels = {
            "numero_allocation": "N° allocation",
            "type_publicite": "Type",
            "reference_juridique": "Référence juridique",
            "adresse": "Adresse de la parcelle",
            "numero_rueavenue": "Rue/Avenue",
            "adresse_precise": "Adresse précise",
            "contribuable": "Contribuable",
            "superficie": "Superficie (m²)",
            "taxe": "Taxe",
            "date_debut": "Date début",
            "solde_depart" : "Solde de départ",
        }

        help_texts = {
            "numero_allocation": "Numéro chronologique",
            "type_publicite": "Publicité Mur ou Clôture",
            "reference_juridique": "Référence juridique du contrat - ordonnance",
            "adresse": "Adresse complète de la parcelle (Commune-Zone-Quartier)",
            "numero_rueavenue": "Numéro de rue ou de l’avenue",
            "adresse_precise": "Adresse avec précision (en face de .../ A côté de ...) qui est facultative",
            "contribuable": "Information du contribuable",
            "superficie": "Surface du mur ou de la clôture",
            "taxe": "Matière imposable",
            "date_debut": "Début de l'occupation",
            "solde_depart" : "Montant des arriérés",
        } 

    def __init__(self, *args, **kwargs):
        super(PubliciteMurClotureForm, self).__init__(*args, **kwargs)
        
        # Reference de l'allocation : Initialiser le champs numéro de reference avec le nouveau nom chrono
        self.fields['numero_allocation'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('PMC') #PMC = Allocation Publicité sur les Murs/Clôtures

        # Taxe sur Mur et ou cloture. type_impot = 1 'Note d'imposition, taxe_filter = choix_taxe_filter.TAXE_PUBLICITE_MUR_CLOTURE
        self.fields['taxe'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 1, periode_type__temps = True, taxe_filter = TAXE_PUBLICITE_MUR_CLOTURE)

        #Identifiant de l'activité encours
        self._id = int(self.instance.id or 0) 

        #Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        if self._id>0:
            if self.instance.date_validate:
                self.fields['reference_juridique'].widget.attrs['disabled'] = True
                self.fields['type_publicite'].widget.attrs['disabled'] = True
                self.fields['adresse_precise'].widget.attrs['disabled'] = True
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
            numero_allocation = ChronoHelpers.get_new_num(CHRONO_PUBLICITE_MUR_CLOTURE)

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

    def clean(self):
        # Validation des adresses
        adresse = self.cleaned_data.get('adresse')
        numero_rueavenue = self.cleaned_data.get('numero_rueavenue')
        
        # Adressse obligatoire
        if adresse is None:
            raise forms.ValidationError(_("Veuillez indiquer l'adresse de la publicité."))

        # RueAvenue Obligatoire
        if numero_rueavenue is None:
            raise forms.ValidationError(_("Veuillez indiquer le numéro de rue/avenue/boulevard"))

        # Vérifier la liaison
        if adresse and numero_rueavenue:
            if not is_rue_avenue_exists(adresse, numero_rueavenue):
                raise forms.ValidationError(_("Cette rue-avenue n'existe pas pour l'adresse seléctionnée"))

        return self.cleaned_data

class ImageUploadPubliciteMurClotureForm(forms.Form):
    """
    Fichier upload form.
    """
    fichier_lettre_exp_tmp = forms.FileField(required=False)
    fichier_rap_vis_ter = forms.FileField(required=False)