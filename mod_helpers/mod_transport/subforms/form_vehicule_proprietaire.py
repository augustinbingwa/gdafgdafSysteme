from django.utils.translation import gettext as _
from django import forms

from mod_transport.models import *

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import * 
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers

from mod_parametrage.enums import *

import re

#----------------------------------------------------------------
class VehiculeProprietaireForm(forms.ModelForm):
    """
    Formulaire : Carte de propriétaire
    """
    class Meta:
        model = VehiculeProprietaire 

        fields = ('numero_carte', 'vehicule', 'contribuable', )

        exclude = ('user_create', 'user_update', 'user_validate', 'user_print', 'date_update', 'date_validate', 'date_print')

        widgets = {
            'numero_carte': forms.TextInput(attrs={'readonly':'readonly'}),
        }

        labels = {
            "numero_carte": "N° de la carte",
            "vehicule": "Véhicule",
            'contribuable': 'Contribuable',
        }

        help_texts = {
            "numero_carte": "Numéro de la carte de propriétaire",
            "vehicule": "Informations du véhicule et de l'ancien propriétaire",
            'contribuable': 'Information du propriétaire',
        }

    def __init__(self, *args, **kwargs):
        super(VehiculeProprietaireForm, self).__init__(*args, **kwargs)
        
        #Reference : Initialiser le champs référence avec le nouveau nom chrono
        self.fields['numero_carte'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('CP')

        #Identifiant de l'objet en cours
        self._id = int(self.instance.id or 0) 

    def clean_numero_carte(self):
        """
        Generer le numero matricule avant save
        """
        numero_carte = self.cleaned_data['numero_carte']
        
        # Mode création uniquement
        if self._id == 0:
            numero_carte = ChronoHelpers.get_new_num(CHRONO_CARTE_PROPRIETE_VEHICULE)

        return numero_carte

#----------------------------------------------------------------
class VehiculeProprietairePrintForm(forms.ModelForm):
    """
    Form Impression : Mattre à jour du numero de la carte physique avant l'impression de la carte
    """
    class Meta:
        model = VehiculeProprietaire 

        fields = ('numero_carte_physique', )

        labels = {
            "numero_carte_physique": "N° de la carte physique",
        }

        help_texts = {
            "numero_carte_physique": "Numéro de la carte se trouvant sur le papier sécurisé",
        }

    def __init__(self, *args, **kwargs):
        super(VehiculeProprietairePrintForm, self).__init__(*args, **kwargs)

        #Identifiant de l'objet en cours
        self._id = int(self.instance.id or 0) 
    
    def clean_numero_carte_physique(self):
        """
        Numero de la carte phyique obligatoire et en chiffre uniquement
        """
        numero_carte_physique = self.cleaned_data['numero_carte_physique']
        
        if self._id > 0:
            # Obligatoire
            if numero_carte_physique is None:
                raise forms.ValidationError(_("Le numéro de la carte est obligatoire"))

            # Nombre entre 0 et 9 uniquement
            if not is_number_only(numero_carte_physique):
                raise forms.ValidationError(_("Le numéro de la carte doit être uniquement en chiffre."))

        return numero_carte_physique