from django.utils.translation import gettext as _
from django import forms
from django.db.models import Q

from mod_helpers.hlp_validators import * 

from mod_transport.models import *

class VehiculeActiviteDuplicataForm(forms.ModelForm):
    """
    Formulaire Dulicata de la carte professionnelle
    """
    class Meta:
        model = VehiculeActiviteDuplicata 

        fields = ('vehicule_activite', )

        exclude = ('user_create', 'user_update', 'user_validate', 'user_print', 'date_update', 'date_validate', 'date_print')

        labels = {           
            "vehicule_activite": "Information de l'activité du véhicule",
        }

        help_texts = {
            "vehicule_activite": "Réchercher par : numero d'activité, plaque, chassi",
        }

    def __init__(self, *args, **kwargs):
        super(VehiculeActiviteDuplicataForm, self).__init__(*args, **kwargs)
        
        #Identifiant de l'objet en cours
        self._id = int(self.instance.id or 0) 

    def clean_vehicule_activite(self):
        """
        Contrôler l'information de l'activité du véhicule 
        """
        vehicule_activite = self.cleaned_data['vehicule_activite']
        
        query = Q(vehicule_activite=vehicule_activite)
        obj = VehiculeActiviteDuplicata.objects.filter(query)

        # Mode création uniquement
        if self._id == 0:
            if obj:
                # 1 - Empecher la création d'un nouveau duplicata tant que un autre n'est ni validé ni payé ni imprimé    
                if not obj[0].is_printed:
                    raise forms.ValidationError(_("Création impossible. Un autre duplicata de cette carte est en attente de validation/payement/impression"))
            else:
                # 2 - Si carte originale n'est pas reglé (paiement, impression)
                if not vehicule_activite.is_printed:
                    raise forms.ValidationError(_("Création impossible. Ce véhicule n'a pas encore de carte professionnelle originale"))
        
        return vehicule_activite

#----------------------------------------------------------------
class VehiculeActiviteDuplicataPrintForm(forms.ModelForm):
    """
    Form Impression : Mattre à jour du numero de la carte physique avant l'impression de la carte
    """
    class Meta:
        model = VehiculeActivite 

        fields = ('numero_carte_physique', )

        labels = {
            "numero_carte_physique": "N° de la carte physique",
        }

        help_texts = {
            "numero_carte_physique": "Numéro de la carte se trouvant sur le papier sécurisé",
        }

    def __init__(self, *args, **kwargs):
        super(VehiculeActiviteDuplicataPrintForm, self).__init__(*args, **kwargs)

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