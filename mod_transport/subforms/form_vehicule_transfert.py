from django.utils.translation import gettext as _
from django import forms
from django.db.models import Q

from mod_transport.models import *
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_error import ErrorsHelpers
from mod_helpers.hlp_global_variables import GlobalVariablesHelpers

import re

class VehiculeTransfertForm(forms.ModelForm):
    class Meta:
        model = VehiculeTransfert
        
        fields = ('sous_categorie', 'locale', 'plaque', 'modele', 'chassis',
                  'contribuable_encien','contribuable_nouveau', 'remunere',
                  'compte_propre','actif')
        
        widgets = {
            'sous_categorie':forms.TextInput(attrs={'placeholder':'sous categoire du vehicule ...'}),
            'plaque':forms.TextInput(attrs={'placeholder':'Numero de plaque du vehicule ...'}),
            'chassis': forms.TextInput(attrs={'placeholder':'Le numéro de chassis...'}),
        }

        labels = {
            'sous_categorie': 'Catégorie',
            'locale': "Origine",
            'plaque': "N° plaque",
            'modele': 'Marque et Modèle',
            'chassis': "N° chassis/cadre",
            'contribuable_encien': 'Propriétaire encien',
            'contribuable_nouveau': 'Propriétaire nouveau',
            'remunere': 'Rémunéré',
            'actif': 'En service',
            'compte_propre': " Compte propre",
        }

        help_texts = {
            'sous_categorie': 'Catégorie et Sous-catégorie du véhicule',
            'locale': "Locale/Etrangère",
            'plaque': "Numéro de plaque d'immatriculation",
            'modele': 'Modèle du véhicule',
            'chassis': "Numéro de chassis ou cadre",
            'contribuable_encien': "Information de l'encien contribuale",
            'contribuable_nouveau': 'Information du nouveau contribuale',
            'remunere': 'Activité municipale',
            'compte_propre': "OUI : Ce véhicule paie uniquement le droit de stationnement",
            'actif': "Status de l'activité",
        }
class NonRedevabiliteFileUploadForm(forms.Form):
    """
    Model Form : Upload  CARTE ROSE du véhicule
    """
    fichier_non_redevabilite = forms.FileField(required=False)