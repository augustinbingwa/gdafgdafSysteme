from django.utils.translation import gettext as _
from django import forms
from django.db.models import Q

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import * 

from mod_transport.models import *

from mod_parametrage.enums import *

import re

class VehiculeActiviteForm(forms.ModelForm):
    """
    Formulaire : Fiche d'actvité d'un véhicule de transport rémunéré'
    """
    class Meta:
        model = VehiculeActivite 

        fields = ('numero_activite', 'vehicule', 'contribuable', 'chassis', 'date_debut', 'solde_depart')

        exclude = ('user_create', 'user_update', 'user_validate', 'user_print', 'date_update', 'date_validate', 'date_print')

        widgets = {
            'numero_activite': forms.TextInput(attrs={'readonly':'readonly'}),
            'chassis': forms.TextInput(attrs={'placeholder':'Le numéro de chassis...'}),
        }

        labels = {
            "numero_activite": "Référence'",
            "vehicule": "Véhicule",
            'contribuable': 'Propriétaire',
            'chassis': "Chassis",
            'date_debut' : "Ouverture",
            "solde_depart" : "Solde de départ",
        }

        help_texts = {
            "numero_activite": "Numéro de référence de l'activité",
            "vehicule": "Informations du véhicule",
            'contribuable': 'Information du propriétaire ou contribuale',
            'chassis': "Numéro de chassis",
            'date_debut' : "Date d'ouverture de l'activité",
            "solde_depart" : "Montant des arriérés",
        }

    def __init__(self, *args, **kwargs):
        super(VehiculeActiviteForm, self).__init__(*args, **kwargs)
        
        # Reference : Initialiser le champs référence avec le nouveau nom chrono
        self.fields['numero_activite'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('AT')

        # Identifiant de l'objet en cours
        self._id = int(self.instance.id or 0) 

        # Gestion de contrôles : Désactiver tous le champs de saisie si les infos de l'activité du véhicule sont validées
        if self._id>0:
                if self.instance.date_validate:
                    self.fields['chassis'].widget.attrs['disabled'] = True
                    self.fields['date_debut'].widget.attrs['disabled'] = True
                    self.fields['solde_depart'].widget.attrs['disabled'] = True

                    # Les champs suivants sont des champs autocompletion ie des champs qui ne sont pas dans meta fields
                    # Alors leur desactivation se fera au niveau du template (_vehicule_activite_form.html) voir button
                    # 'vehicule', 'contribuable'

    def clean_numero_activite(self):
        """
        Generer le numero matricule avant save
        """
        numero_activite = self.cleaned_data['numero_activite']
        
        # Mode création uniquement
        if self._id == 0:
            numero_activite = ChronoHelpers.get_new_num(CHRONO_ACTIVITE_TRANSPORT)

        return numero_activite

    def clean_chassis(self):
        """
        Validation du numéro de chassis
        - taille : 17 caractères
        - format : alphanumérique seulement
        - unicité : le numéro est UNIQUE pour tout véhicule (Modele Vehicule)
        - Si le véhicule change de numéro de chassi alors il doit changer de carte rose
        - Si le véhicule change de propriétaire alors il doit changer de carte rose
        """
        chassis = str(self.cleaned_data.get('chassis'))
        vehicule = self.cleaned_data.get('vehicule')

        error_messages = []

        if vehicule is not None:
            # Filtrer uniquement les voitures qui ont de plaque ie de carte rose
            q = Q(id = vehicule.sous_categorie.id) & Q(has_plaque = True) 
            obj = VehiculeSousCategorie.objects.filter(q)
            if obj:
                # Taille entre 1 et 17
                if len(chassis) == 4 and chassis == 'None': # A RESOUDRE
                    raise forms.ValidationError(_("La longueur du numéro de chassis est comprise entre 1 à 17."))

                # Alphanumerique
                if not is_alphanumeric_only(chassis):
                    raise forms.ValidationError(_("Le numéro de chassis doit être uniquement en lettre/chiffre."))

                # Unicité
                if chassis != vehicule.chassis.upper():
                    #Chercher dans le Modele Vehicule si chassis existe
                    obj = Vehicule.objects.filter(chassis = chassis)
                    if obj:
                        raise forms.ValidationError(_("Le numéro du chassis appartient déjà à un autre véhicule."))
        
        return chassis #Le mettre toujours en majiscule

    def clean(self):
        """
        # En mode CREATION (date_validate = null, actif = True), On réfuse de lui créer une autre activité
        """
        vehicule = self.cleaned_data.get('vehicule')
        
        # Véhicule sans taxe d'activité (TOUJOURS IMPORTANT meme si c'est obsolete)
        if  vehicule:
            if vehicule.sous_categorie.taxe_activite is None:
                raise forms.ValidationError(_("Cette catégorie de véhicule ne peut pas exercer d'activité"))    

        # Vehicule en cours d'ativité
        if self.instance.id is None:
            if vehicule:
                obj = VehiculeActivite.objects.filter(vehicule=vehicule.id)
                if obj:
                    raise forms.ValidationError(_("Ce véhicule est en cours d'activité"))

        """
        # Si le numéro de chassi change alors exiger la carte_rose
        if obj is not None and obj_vehicule is not None:
            if obj.chassis != obj_vehicule.chassis:
                if not obj.fichier_carte_rose:
                    pass
                    #return ErrorsHelpers.show_message(request, 'Fichier carte rose obligatoire')
        
        
        # Si le contribuable change alors exiger la carte rose
        """

        return self.cleaned_data

#----------------------------------------------------------------
class VehiculeActiviteFileUploadForm(forms.Form):
    """
    Model Form : Upload  CARTE ROSE et AUTORISATION DE TRANSPORT du véhicule
    """
    # Carte rose
    fichier_carterose = forms.FileField(required=False)

    # Atutorisation de transport
    fichier_autorisation = forms.FileField(required=False)

#----------------------------------------------------------------
class VehiculeActivitePrintForm(forms.ModelForm):
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
        super(VehiculeActivitePrintForm, self).__init__(*args, **kwargs)
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
                raise forms.ValidationError("Le numéro de la carte est obligatoire")

            # Nombre entre 0 et 9 uniquement
            if not is_number_only(numero_carte_physique):
                raise forms.ValidationError("Le numéro de la carte doit être uniquement en chiffre.")

        return numero_carte_physique