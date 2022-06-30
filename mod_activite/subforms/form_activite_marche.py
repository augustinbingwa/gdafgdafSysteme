from django.utils.translation import gettext as _
from django import forms

from mod_activite.models import Marche, NomMarche, AllocationPlaceMarche
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import *
from mod_finance.models import Taxe

from mod_parametrage.enums import *

class MarcheForm(forms.ModelForm):
    """
    Form Activité dans le Marché
    """
    class Meta:
        model = Marche

        fields = ('numero_activite', 'allocation_place_marche', 'taxe', 'date_debut', 'solde_depart', 'ai_cout_carte')

        exclude = ('user_create','user_update', 'user_validate','user_print','date_create','date_update','date_validate','date_print')

        widgets = {
            'numero_activite': forms.TextInput(attrs={'readonly':'readonly'}),
        }

        labels = {
            "numero_activite": "N° Activité (Marché)",
            "allocation_place_marche": "Information de l'allocation de place dans le marché",
            "taxe": "Matière imposable",
            "date_debut": "Date début",
            "solde_depart" : "Solde de départ",
            "ai_cout_carte" : "Coût de la carte professionnelle",
        }

        help_texts = {
            "numero_activite": "Numéro d'activité",
            "allocation_place_marche": "Marché - Place - Contribuable)",
            "taxe": "Taxe sur l'activité dans le marché",
            "date_debut": "Début de l’activité",
            "solde_depart" : "Montant des arriérés",
            "ai_cout_carte" : "Avis d'impostionpour le coût de la carte professionnelle",
        } 

        error_messages = {
            'allocation_place_marche': {
                'required': ("La place est recquise"),
            },
            'taxe': {
                'required': ("L'activité est recquise"),
            },
            'date_debut': {
                'required': ("La date est recquise"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(MarcheForm, self).__init__(*args, **kwargs)

        # Numero activité : Initialiser le champs numéro d'activité avec le nouveau nom chrono
        self.fields['numero_activite'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('AM')

        # Taxe sur le papier sécurisé. type_impot = 0 'Avis d'imposition, taxe_filter.TAXE_AI_DOCUMENT_FINANCIER
        self.fields['ai_cout_carte'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 0, taxe_filter = TAXE_AI_DOCUMENT_FINANCIER)

        # Identifiant de l'activité encours
        self._id = int(self.instance.id or 0)

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé 
        if self._id>0:
           if self.instance.date_validate:
                self.fields['date_debut'].widget.attrs['disabled'] = True
                self.fields['solde_depart'].widget.attrs['disabled'] = True

    def clean_numero_activite(self):
        """
        Generer le numero activite avant save
        """
        numero_activite = self.cleaned_data['numero_activite']
        
        # Mode création uniquement
        if self._id == 0:
            numero_activite = ChronoHelpers.get_new_num(CHRONO_ACTIVITE_MARCHE)

        return numero_activite

    def clean_allocation_place_marche(self):
        """
        Controler le doublon, interdire la créaton d'une nouvelle activité sur la même place en mode création
        """
        allocation_place_marche = self.cleaned_data['allocation_place_marche']

        if self.instance.id is None:
            # En mode création
            if allocation_place_marche:
                obj = Marche.objects.filter(allocation_place_marche__id=allocation_place_marche.id)
                if obj:
                    if not obj[0].date_fin:
                        raise forms.ValidationError(_("Une activité a été déjà attribuée à cet emplacement."))

        return allocation_place_marche

    def clean_date_debut(self):
        """
        Validation de la date début de l'activité
        """
        date_debut = self.cleaned_data.get('date_debut')

        if not is_date_valid(date_debut):
            raise forms.ValidationError(_("Date début invalide."))

        return date_debut

#----------------------------------------------------------------
class MarchePrintForm(forms.ModelForm):
    """
    Form Impression : Mettre à jour du numero de la carte physique avant l'impression de la carte
    """
    class Meta:
        model = Marche 

        fields = ('numero_carte_physique', )

        labels = {
            "numero_carte_physique": "N° de la carte physique",
        }

        help_texts = {
            "numero_carte_physique": "Numéro de la carte se trouvant sur le papier sécurisé",
        }

    def __init__(self, *args, **kwargs):
        super(MarchePrintForm, self).__init__(*args, **kwargs)
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