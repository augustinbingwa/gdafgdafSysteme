from django.utils.translation import gettext as _
from django import forms
from django.db.models import Q

from mod_helpers.hlp_validators import * 

from mod_transport.models import *

#----------------------------------------------------------------
class VehiculeProprietaireDuplicataForm(forms.ModelForm):
    """
    Formulaire Dulicata de la carte de propriétaire
    """
    class Meta:
        model = VehiculeProprietaireDuplicata 

        fields = ('vehicule_proprietaire',)

        exclude = ('user_create', 'user_update', 'user_validate', 'user_print', 'date_update', 'date_validate', 'date_print')

        labels = {           
            "vehicule_proprietaire": "Information du véhicule",
        }

        help_texts = {
            "vehicule_proprietaire": "Recherche par: numéro de carte, Plaque, chassis",
        }

    def __init__(self, *args, **kwargs):
        super(VehiculeProprietaireDuplicataForm, self).__init__(*args, **kwargs)
        
        #Identifiant de l'objet en cours
        self._id = int(self.instance.id or 0) 

    def clean_vehicule_proprietaire(self):
        """
        Contrôler l'information du véhicule propriété
        """
        vehicule_proprietaire = self.cleaned_data['vehicule_proprietaire']
        
        query = Q(vehicule_proprietaire=vehicule_proprietaire)
        obj = VehiculeProprietaireDuplicata.objects.filter(query)

        # Mode création uniquement
        if self._id == 0:
            if obj:
                # 1 - Empecher la création d'un nouveau duplicata tant que un autre n'est ni validé ni payé ni imprimé    
                if not obj[0].is_printed:
                    raise forms.ValidationError(_("Création impossible! Un autre duplicata de cette carte est en attente de validation/payement/impression"))
            else:
                # 2 - Si carte originale n'est pas reglé (paiement, impression)
                if not vehicule_proprietaire.is_printed:
                    raise forms.ValidationError(_("Création impossible! Ce véhicule n'a pas encore de carte de propriété originale"))
        
        return vehicule_proprietaire

#----------------------------------------------------------------
class VehiculeProprietaireDuplicataPrintForm(forms.ModelForm):
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
        super(VehiculeProprietaireDuplicataPrintForm, self).__init__(*args, **kwargs)

        #Identifiant de l'objet en cours
        self._id = int(self.instance.id or 0) 
    
    def clean_numero_carte_physique(self):
        """
        Numero de la carte phyique obligatoire et en chiffre uniquement
        """
        numero_carte_physique = self.cleaned_data['numero_carte_physique']
        
        if self._id > 0:
            # 1 - Obligatoire
            if numero_carte_physique is None:
                raise forms.ValidationError(_("Le numéro de la carte est obligatoire"))

            # 2 - Nombre entre 0 et 9 uniquement
            if not is_number_only(numero_carte_physique):
                raise forms.ValidationError(_("Le numéro de la carte doit être uniquement en chiffre."))

        return numero_carte_physique