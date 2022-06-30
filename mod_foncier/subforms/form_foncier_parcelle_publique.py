from django.utils.translation import gettext as _
from django import forms

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import *

from mod_foncier.models import FoncierParcellePublique

from mod_parametrage.models import RueOuAvenue
from mod_parametrage.enums import *

class FoncierParcellePubliqueForm(forms.ModelForm):
    """
    Form Modèle foncier publique
    """
    # Afficher si la parcelle est occupée ou non
    occupee = forms.CharField(required=False, label="Occupée", help_text="Parcelle en cours d'occupation")

    class Meta:
        model = FoncierParcellePublique

        fields = ('numero_parcelle', 'adresse', 'numero_rueavenue', 'adresse_precise',)

        exclude = ('user_create','user_update', 'user_validate', 'user_print', 'date_update', 'date_validate', 'date_print')

        widgets = {
            'numero_parcelle': forms.TextInput(attrs={'readonly':'readonly'}),
            'adresse_precise': forms.TextInput(attrs={'placeholder':"Préciser l'adresse exacte..."}),
        }

        labels = {
            "numero_parcelle": "Numéro de l'espace",
            "adresse": "Adresse de l'espace",
            "numero_rueavenue": "Rue/Avenue",
            "adresse_precise": "Adresse précise",
        }

        help_texts = {
            "numero_parcelle": "Numéro chronologique",
            "adresse": "Adresse complète de l'espace (Commune-Zone-Quartier)",
            "numero_rueavenue": "Numéro de rue ou de l’avenue",
            "adresse_precise": "Adresse avec précision (en face de .../ A côté de ...)",
        } 

    def __init__(self, *args, **kwargs):
        super(FoncierParcellePubliqueForm, self).__init__(*args, **kwargs)
        
        # Reference de la parcelle : Initialiser le champs numéro de reference avec le nouveau nom chrono
        self.fields['numero_parcelle'].initial = 'Auto - Chorno'

        # Identifiant de l'activité encours
        self._id = int(self.instance.id or 0) 

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        if self._id>0:
            if self.instance.date_validate:
                self.fields['adresse_precise'].widget.attrs['class'] = 'disabled-element'
                self.fields['numero_rueavenue'].widget.attrs['class'] = 'disabled-element'
    
    def clean_numero_parcelle(self):
        """
        Generer le numero matricule avant save
        """
        numero_parcelle = self.cleaned_data['numero_parcelle']
        
        # Mode création uniquement
        if self._id == 0:
            numero_parcelle = ChronoHelpers.get_new_num(CHRONO_PARCELLE_PUBLIQUE)

        return numero_parcelle

    
    def clean(self):
        # Validation des adresses
        adresse = self.cleaned_data.get('adresse')
        numero_rueavenue = self.cleaned_data.get('numero_rueavenue')
        
        # Adressse obligatoire
        if adresse is None:
            raise forms.ValidationError(_("Veuillez indiquer l'adresse de l'espace public."))

        # RueAvenue Obligatoire
        if numero_rueavenue is None:
            raise forms.ValidationError(_("Veuillez indiquer le numéro de rue/avenue/boulevard"))

        # Vérifier la liaison
        if adresse and numero_rueavenue:
            if not is_rue_avenue_exists(adresse, numero_rueavenue):
                raise forms.ValidationError(_("Cette rue-avenue n'existe pas pour l'adresse seléctionnée"))

        return self.cleaned_data