from django.utils.translation import gettext as _
from django import forms
from django.db.models import Q

from mod_transport.models import *
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers

import re

class VehiculeForm(forms.ModelForm):
    """
    Formulaire : Véhicule
    """
    # Afficher si le véhicule est en activité
    actif = forms.CharField(required=False, label="En service", help_text="Status de l'activité")

    class Meta:
        model = Vehicule
        
        fields = ('sous_categorie', 'locale', 'plaque', 'modele', 'chassis', 'contribuable', 'remunere', 'compte_propre')

        exclude = ('actif', 'user_create', 'user_update', 'user_validate', 'user_print', 'date_update', 'date_validate', 'date_print')
        
        widgets = {
            'sous_categorie':forms.Select(attrs={"onChange":'OnCategorieChanged()'}),
            'locale':forms.Select(choices=[(True,"Locale"),(False,"Etrangère")]),
            'remunere':forms.Select(choices=[(True,"Oui"),(False,"Non")]),
            'chassis': forms.TextInput(attrs={'placeholder':'Le numéro de chassis...'}),
            'compte_propre':forms.Select(choices=[(True,"Oui, paiement du droit de stationnement uniquement"),(False,"Non")]),
        }

        labels = {
            'sous_categorie': 'Catégorie',
            'locale': "Origine",
            'plaque': "N° plaque",
            'modele': 'Marque et Modèle',
            'chassis': "N° chassis/cadre",
            'contribuable': 'Propriétaire',
            'remunere': 'Rémunéré',
            'compte_propre': 'Compte propre',
        }

        help_texts = {
            'sous_categorie': 'Catégorie et Sous-catégorie du véhicule',
            'locale': "Locale/Etrangère",
            'plaque': "Numéro de plaque d'immatriculation",
            'modele': 'Modèle du véhicule',
            'chassis': "Numéro de chassis ou cadre",
            'contribuable': 'Information du contribuale',
            'remunere': 'Activité municipale',
            'compte_propre': "OUI : Ce véhicule paie uniquement le droit de stationnement",
        }   

    def __init__(self, *args, **kwargs):
        super(VehiculeForm, self).__init__(*args, **kwargs)
        
        #Identifiant de l'objet en cours
        self._id = int(self.instance.id or 0) 

        # Gestion de contrôles : Désactiver tous le champs de saisie si les infos du véhicule sont validées
        if self._id>0:
            if self.instance.date_validate:
                self.fields['sous_categorie'].widget.attrs['disabled'] = True
                self.fields['locale'].widget.attrs['disabled'] = True
                self.fields['plaque'].widget.attrs['disabled'] = True
                self.fields['chassis'].widget.attrs['disabled'] = True
                self.fields['remunere'].widget.attrs['disabled'] = True
                self.fields['compte_propre'].widget.attrs['disabled'] = True

                # Les champs suivants sont des champs autocompletion ie des champs qui ne sont pas dans meta filds
                # Alors leur desactivation se fera au niveau du template (_vehicule_form.html) voir button
                # 'modele', 'contribuable'

    def __si_plaque_existe(self, plaque, type_roue):
        """
        Tester si la plaque existe pour une catégorie de véhicule seléctionnée
        """
        res = False
        
        # Filtrer uniquement le véhicule à 4 roues                        
        q = Q(sous_categorie__categorie__type_roue = type_roue) & Q(plaque = plaque) 
        obj = Vehicule.objects.filter(q)
        if obj:
            if self.instance.id is None:
                #Nouveau véhicule (en mode création)
                res = True
            else:
                #Vehicule existant (en mode update)
                obj = obj.filter(id = self.instance.id) #Lui même
                if not obj :
                    res = True
        
        return res

    def clean_plaque(self):
        """
        Validator de plaque d'immatriculation
        - filtre : Seul le véhicule avec carte rose sera à contrôler
        - unicité : les véhicules à 4 roues ont de plaque UNIQUE chacun
        - regle : on teste seulement l'unicité entre les véhicules du même type de roue
        """
        plaque = self.cleaned_data.get('plaque')
        sous_categorie = self.cleaned_data.get('sous_categorie')
        locale = self.cleaned_data.get('locale')

        # Plaue alphanumerique
        if not re.match(r'[A-Z0-9_]', plaque):
            raise forms.ValidationError("Le numéro de plaque doit être uniquement en lettre majuscule/chiffre.")

        if sous_categorie :
            # Voiture locale avec carte rose
            if locale:
                if sous_categorie.has_plaque and len(plaque) != 6 :
                    raise forms.ValidationError("Le nombre de caractères de la plaque burundaise doit être égal à 6.")
                    
            # Pour le typede vehicule sans carte rose : velo/velomoteur), la plaque doit commencer par 'BJM' (Voir variable global)
            if not sous_categorie.has_plaque:
                valeur = GlobalVariablesHelpers.get_global_variables("TRANSPORT", "PLAQUE_DEFAULT").valeur
                if len(valeur)>0:
                    if plaque[0:len(valeur)] != valeur:
                        raise forms.ValidationError(_("La plaque du vélo/velo-moteur doit commencer par '" + valeur + "'"))

            #Le type de roue seléctionné
            type_roue = sous_categorie.categorie.type_roue

            if type_roue == 2: # Filtrer uniquement le véhicule à 4 roues
                if self.__si_plaque_existe(plaque, type_roue):
                    raise forms.ValidationError(_("Le numéro de plaque existe déjà pour les véhicules à 4 roues"))
            elif type_roue == 1: # Filtrer uniquement le véhicule à 2/3 roues
                if self.__si_plaque_existe(plaque, type_roue):
                    raise forms.ValidationError(_("Le numéro de plaque existe déjà pour les véhicules à 2/3 roues"))
            elif type_roue == 0: # Filtrer uniquement le véhicule sans roues (bateau)
                if self.__si_plaque_existe(plaque, type_roue):
                    raise forms.ValidationError(_("Le numéro de plaque existe déjà pour les bateaux"))

        return plaque

    def clean_chassis(self):
        """
        Validation du numéro de chassis
        - filtre : Seul le véhicule avec carte rose sera à contrôler
        - unicité : le numéro est UNIQUE pour tout véhicule
        - exception : les véhicules sans carte rore n'a pas de numéro de chassi
        - format : alphanumérique seulement
        - taille : 17 caractères
        """
        chassis = str(self.cleaned_data.get('chassis'))
        sous_categorie = self.cleaned_data.get('sous_categorie')

        q =  Q(id = sous_categorie.id) & Q(has_plaque = True) # Filtrer uniquement les voitures qui ont de plaque ie de carte rose
        obj = VehiculeSousCategorie.objects.filter(q)
        if obj:
            # Taille entre 1 et 17
            if len(chassis) == 4 and chassis == 'None': # A RESOUDRE
                raise forms.ValidationError(_("La longueur du numéro de chassis est comprise entre 1 à 17."))

            # Alphanumerique
            if not re.match(r'[a-zA-Z0-9_]', chassis):
                raise forms.ValidationError(_("Le numéro de chassis est composé de lettre et de chiffre seulement."))

            # Unicité
            obj = Vehicule.objects.filter(chassis = chassis)            
            if obj:
                obj = obj.filter(id = self.instance.id) #Lui même
                if obj is None:
                    raise forms.ValidationError(_("Le numéro de chassis existe déjà."))

        return chassis #Le mettre toujours en majiscule

    def clean_remunere(self):
        """
        Validation du numéro de chassis
        - contrainte : les voiures à 4 roues doivent exercer obligatoirement des activités de transport rémunéré
        - option : les véhicules à 0/2/3 roues n'exercement pas obligatoirement des activité de transport rémunéré
        - format : alphanumérique seulement
        - taille : 17 caractères
        """
        remunere = self.cleaned_data.get('remunere')
        sous_categorie = self.cleaned_data.get('sous_categorie')
        
        if remunere:
            # Vélo privé et vélo moteur
            if sous_categorie.taxe_activite is None:
                raise forms.ValidationError(_("Le velo/velomouter ayant cette catégorie ne peut pas exercer une activité rémunérée."))
        else:
            # Taxi velo et taxi moto
            if sous_categorie.taxe_activite:
                raise forms.ValidationError(_("Le véhicule ayant cette catégorie doit toujours exercer une activité rémunérée. SEULEMENT, il ne paiera pas la carte municipale s'il est sous son compte propre."))

        obj = VehiculeSousCategorie.objects.get(id = sous_categorie.id)
        if obj:
            if (not remunere) & (obj.categorie.type_roue == 2): #Camion - Voiture - Bus - ... // Ils sont obligatoirement rémunéré
                raise forms.ValidationError(_("Le véhicule ayant cette catégorie doit exercer des activités municipales."))

        return remunere

    def clean_compte_propre(self):
        """
        Controle des véhicule qui n'exercent pas d'activité locale, par contre le droit de stationnement est obligatoire
        """
        compte_propre = self.cleaned_data.get('compte_propre')
        sous_categorie = self.cleaned_data.get('sous_categorie')
        locale = self.cleaned_data.get('locale')

        if not locale and not compte_propre:
            raise forms.ValidationError(_("La voiture étrangère doit être sur le compte propre"))

        if sous_categorie and compte_propre == True:
            if not sous_categorie.has_compte_propre:
                raise forms.ValidationError(_("Cette catégorie n'exerce pas d'activité sous son propre compte"))

        return compte_propre

class CarteRoseFileUploadForm(forms.Form):
    """
    Model Form : Upload  CARTE ROSE du véhicule
    """
    fichier_carterose = forms.FileField(required=False)