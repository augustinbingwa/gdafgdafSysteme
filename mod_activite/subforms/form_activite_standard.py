from django.utils.translation import gettext as _
from django import forms

from mod_activite.models import Standard
from mod_finance.models import Taxe

from mod_parametrage.enums import *
from mod_parametrage.models import RueOuAvenue

from mod_helpers.hlp_validators import *
from mod_helpers.hlp_chrono import ChronoHelpers

class StandardForm(forms.ModelForm):
    """
    Form Activté Standard
    """
    class Meta:
        model = Standard

        fields = ('numero_activite', 'contribuable', 'type_espace', 'adresse', 'numero_rueavenue', 'numero_police', 'taxe', 
                  'date_debut', 'allocation_espace_publique', 'solde_depart', 'ai_cout_carte')

        exclude = ('user_create','user_update', 'user_validate','user_print','date_update','date_validate','date_print',)

        widgets = {
            'numero_activite': forms.TextInput(attrs={'readonly':'readonly'}),
            'type_espace': forms.Select(attrs={"onChange":'OnTypeEspaceChanged()'}),
            'numero_police': forms.TextInput(attrs={'placeholder':'...'}),
        }

        labels = {
            "numero_activite": "N° Activité",
            "contribuable": "Contribuable",
            "type_espace": "Type d'éspace",
            "adresse": "Adresse de l'activité (PRIVÉ)",
            "numero_rueavenue": "Rue/Avenue (PRIVÉ)",
            "numero_police": "N° Police",
            "taxe": "Matière imposable",
            "date_debut": "Date début",
            "allocation_espace_publique": "Allocation de l'espace (PUBLIC)",
            "solde_depart" : "Solde de départ",
            "ai_cout_carte" : "Coût de la carte professionnelle",
        }

        help_texts = {
            "numero_activite": "Numéro de l'activité",
            "contribuable": "Numéro d’identification du contribuable",
            "type_espace": "Public: bâtiment municipal de la mairie, espace de l’Etat",
            "adresse": "Adresse complète du lieu d’activité Commune-Zone-Quartier",
            "taxe": "Taxe relative à l'activité exércée",
            "numero_police":"Le numéro du logement",
            "numero_rueavenue": "Numéro/Nom de rue ou de l’avenue si existe",
            "date_debut": "Début de l’activité",
            "allocation_espace_publique": "Si le type d'espace est PUBLIQUE: Information du contrat de l'allocation de l'éspace publique",
            "solde_depart" : "Montant des arriérés",
            "ai_cout_carte" : "Avis d'impostionpour le coût de la carte professionnelle",
        }

        error_messages = {
            'contribuable': {'required': ('Le contribuable est recquis'),}
        }

    def __init__(self, *args, **kwargs):
        super(StandardForm, self).__init__(*args, **kwargs)
        
        # Numero activité : Initialiser le champs numéro d'activité avec le nouveau nom chrono
        self.fields['numero_activite'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('AS')
        
        # Taxe sur le papier sécurisé. type_impot = 0 'Avis d'imposition, taxe_filter.TAXE_AI_DOCUMENT_FINANCIER
        self.fields['ai_cout_carte'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 0, taxe_filter = TAXE_AI_DOCUMENT_FINANCIER)

        #Identifiant de l'activité encours
        self._id = int(self.instance.id or 0)

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé 
        if self._id>0:
            if self.instance.date_validate:
                self.fields['type_espace'].widget.attrs['disabled'] = True
                self.fields['numero_police'].widget.attrs['disabled'] = True
                self.fields['taxe'].widget.attrs['disabled'] = True
                self.fields['date_debut'].widget.attrs['disabled'] = True
                self.fields['solde_depart'].widget.attrs['disabled'] = True
                self.fields['ai_cout_carte'].widget.attrs['disabled'] = True
                
    def clean_numero_activite(self):
        """
        Generer le numero matricule avant save
        """
        numero_activite = self.cleaned_data['numero_activite']
        
        # Mode création uniquement
        if self._id == 0:
            numero_activite = ChronoHelpers.get_new_num(CHRONO_ACTIVITE_STANDARD)

        return numero_activite

    def clean_date_debut(self):
        """
        Validation de la date début de l'activité
        """
        date_debut = self.cleaned_data.get('date_debut')

        if not is_date_valid(date_debut):
            raise forms.ValidationError(_("Date début invalide."))

        return date_debut

    def clean(self):
        """
        Validation de la allocation_espace_publique
        pour les cas type_espace = PUBLIQUE
        """
        type_espace = self.cleaned_data.get('type_espace')
        allocation_espace_publique = self.cleaned_data.get('allocation_espace_publique')

        if type_espace == PUBLIQUE: #choix_espace (PRIVE ou  PUBLIQUE)
            if allocation_espace_publique is None:
                raise forms.ValidationError(_("Veuillez seléctionner l'espace publique."))
        else:
            # Allocation espace publique est facultative
            self.cleaned_data['allocation_espace_publique'] = None

            # Adresse est obligatoire
            adresse = self.cleaned_data.get('adresse')
            numero_rueavenue = self.cleaned_data.get('numero_rueavenue')
            
            # Adressse obligatoire
            if adresse is None:
                raise forms.ValidationError(_("Veuillez indiquer l'adresse de l'activité."))

            # RueAvenue Obligatoire
            if numero_rueavenue is None:
                raise forms.ValidationError(_("Veuillez indiquer le numéro de rue/avenue/boulevard"))

            # Vérifier la liaison
            if adresse and numero_rueavenue:
                if not is_rue_avenue_exists(adresse, numero_rueavenue):
                    raise forms.ValidationError(_("Cette rue-avenue n'existe pas pour l'adresse seléctionnée"))

        return self.cleaned_data

#----------------------------------------------------------------
class StandardAutorisationFileUploadForm(forms.Form):
    """
    Fichier upload form.
    """
    fichier_autorisation = forms.FileField(required=False)

#----------------------------------------------------------------
class StandardPrintForm(forms.ModelForm):
    """
    Form Impression : Mettre à jour du numero de la carte physique avant l'impression de la carte
    """
    class Meta:
        model = Standard 

        fields = ('numero_carte_physique', )

        labels = {
            "numero_carte_physique": "N° de la carte physique",
        }

        help_texts = {
            "numero_carte_physique": "Numéro de la carte se trouvant sur le papier sécurisé",
        }

    def __init__(self, *args, **kwargs):
        super(StandardPrintForm, self).__init__(*args, **kwargs)
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