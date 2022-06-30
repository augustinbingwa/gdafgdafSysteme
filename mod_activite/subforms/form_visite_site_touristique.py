from django.utils.translation import gettext as _
from django import forms

from mod_activite.models import VisiteSiteTouristique
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_finance.models import Taxe
from mod_parametrage.enums import *

class VisiteSiteTouristiqueForm(forms.ModelForm):
    """
    Form Activité Exceptionnelle
    """
    class Meta:
        model = VisiteSiteTouristique

        fields = ('numero_visite', 'site_touristique', 'beneficiaire', 'motif_visite', 'date_delivrance', 'date_expiration', 'taxe',)

        exclude = ('user_create', 'user_update', 'user_validate', 'user_print','date_update','date_validate','date_print')

        widgets = {
            'numero_visite': forms.TextInput(attrs={'readonly':'readonly'}),
            'beneficiaire': forms.TextInput(attrs={'placeholder':'Le nom du bébéficiaire ...'}),
            'motif_visite': forms.TextInput(attrs={'placeholder':"Le motif de la visite ..."}),
        }

        labels = {
            "numero_visite": "N° visite",
            'site_touristique' : 'Site touristique',
            "beneficiaire": "Nom du béneficiaire",
            "motif_visite": "Motif de la visite",
            "date_delivrance": "Délivrée le",
            "date_expiration": "Expirée le",           
            "taxe": "Matière imposable",
        }

        help_texts = {
            "numero_visite": "Numéro de l'visite",
            'site_touristique' : 'Lieu du site touristique',
            "beneficiaire": "Nom du bénéficiaire",
            "motif_visite": "Prise de photos de mariage, visite ...",
            "date_delivrance": "Date de délivrance",
            "date_expiration": "Date d'expiration",
            "taxe": "Taxe relative à la visite du site touristique",
        } 

        error_messages = {
            'beneficiaire': {
                'required': ('Nom du bénéficiaire recquis'),
            },
        }

    def __init__(self, *args, **kwargs):
        super(VisiteSiteTouristiqueForm, self).__init__(*args, **kwargs)
        
        # Reference visite : Initialiser le champs numéro de reference avec le nouveau nom chrono
        self.fields['numero_visite'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('VST') #VST = Visite Site Touristique
        
        # Taxe sur Activite Exceptionnelle. type_impot = 0 'Avis d'imposition, taxe_filter.TAXE_VISITE_SITE_TOURISTIQUE
        self.fields['taxe'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 0, taxe_filter = TAXE_VISITE_SITE_TOURISTIQUE)

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        self._id = int(self.instance.id or 0) #Identifiant de l'visite encours

        if self._id>0:
            if self.instance.date_validate:
                self.fields['beneficiaire'].widget.attrs['disabled'] = True
                self.fields['motif_visite'].widget.attrs['disabled'] = True
                self.fields['date_delivrance'].widget.attrs['disabled'] = True
                self.fields['date_expiration'].widget.attrs['disabled'] = True  
                self.fields['taxe'].widget.attrs['disabled'] = True
    
    def clean_numero_visite(self):
        """
        Generer le numero matricule avant save
        """
        numero_visite = self.cleaned_data['numero_visite']
        
        # Mode création uniquement
        if self._id == 0:
            numero_visite = ChronoHelpers.get_new_num(CHRONO_VISITE_SITE_TOURISTIQUE)

        return numero_visite

    def clean(self):
        """
        Gestion des Validators     
        """
        beneficiaire = self.cleaned_data.get('beneficiaire')
        motif_visite = self.cleaned_data.get('motif_visite')
        date_delivrance = self.cleaned_data.get('date_delivrance')
        date_expiration = self.cleaned_data.get('date_expiration')

        if len(beneficiaire)<10:
            raise forms.ValidationError(_("Nom du bénéficiaire trop court. Au moins 10 caractères."))

        if len(motif_visite)<10:
            raise forms.ValidationError(_("Motif de l'visite trop court. Au moins 10 caractères."))
        
        if date_delivrance > date_expiration:
            raise forms.ValidationError(_("La date d'expiration doit être égale ou supérieur à la date de délivrance."))

        return self.cleaned_data