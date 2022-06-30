from django.utils.translation import gettext as _
from django import forms

from mod_activite.models import ActiviteExceptionnelle
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import *
from mod_finance.models import Taxe
from mod_parametrage.enums import *

class ActiviteExceptionnelleForm(forms.ModelForm):
    """
    Form Activité Exceptionnelle
    """
    class Meta:
        model = ActiviteExceptionnelle

        fields = ('numero_activite', 'beneficiaire', 'motif_activite', 'date_delivrance', 'date_expiration', 'taxe',
            'piece_nombre_1', 'piece_tarif_1', 'piece_nombre_2', 'piece_tarif_2', 'piece_nombre_3', 'piece_tarif_3',
            'piece_nombre_4', 'piece_tarif_4', 'piece_nombre_5', 'piece_tarif_5')

        exclude = ('user_create', 'user_update', 'user_validate', 'user_print','date_update','date_validate','date_print')

        widgets = {
            'numero_activite': forms.TextInput(attrs={'readonly':'readonly'}),
            'beneficiaire': forms.TextInput(attrs={'placeholder':'Le nom du bénéficiaire ...'}),
            'motif_activite': forms.TextInput(attrs={'placeholder':"Le motif de l'actvité ..."}),
        }

        labels = {
            "numero_activite": "N° activité",
            "beneficiaire": "Nom du béneficiaire",
            "motif_activite": "Motif de l'activité",
            "date_delivrance": "Délivrée le",
            "date_expiration": "Expirée le",           
            "taxe": "Matière imposable",
            "piece_nombre_1": "Nombre pièces TYPE 1",
            "piece_tarif_1": "Tarif de la pièce TYPE 1",
            "piece_nombre_2": "Nombre pièces TYPE 2",
            "piece_tarif_2": "Tarif de la pièce TYPE 2",
            "piece_nombre_3": "Nombre pièces TYPE 3",
            "piece_tarif_3": "Tarif de la pièce TYPE 3",
            "piece_nombre_4": "Nombre pièces TYPE 4",
            "piece_tarif_4": "Tarif de la pièce TYPE 4",
            "piece_nombre_5": "Nombre pièces TYPE 5",
            "piece_tarif_5": "Tarif de la pièce TYPE 5",
        }

        help_texts = {
            "numero_activite": "Numéro de l'activité",
            "beneficiaire": "Personne Physique ou Morale (Organisateur)",
            "date_delivrance": "Date de délivrance",
            "date_expiration": "Date d'expiration",
            "motif_activite": "Le motif de l’activité : Foire, Spectacle, Bazar de noel ...",
            "taxe": "Taxe relative à l'activité exércée",
            "piece_nombre_1": "Pièces ou Tickets déclarés TYPE 1",
            "piece_tarif_1": "Montant par pièce/ticket TYPE 1",
            "piece_nombre_2": "Pièces ou Tickets déclarés TYPE 2",
            "piece_tarif_2": "Montant par pièce/ticket TYPE 2",
            "piece_nombre_3": "Pièces ou Tickets déclarés TYPE 3",
            "piece_tarif_3": "Montant par pièce/ticket TYPE 3",
            "piece_nombre_4": "Pièces ou Tickets déclarés TYPE 4",
            "piece_tarif_4": "Montant par pièce/ticket TYPE 4",
            "piece_nombre_5": "Pièces ou Tickets déclarés TYPE 5",
            "piece_tarif_5": "Montant par pièce/ticket TYPE 5",
        } 

        error_messages = {
            'numero_activite': {
                'required': ('Numéro de référence recquise'),
            },
        }

    def __init__(self, *args, **kwargs):
        super(ActiviteExceptionnelleForm, self).__init__(*args, **kwargs)
        
        # Reference activité : Initialiser le champs numéro de reference avec le nouveau nom chrono
        self.fields['numero_activite'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('AE')
        
        # Taxe sur Activite Exceptionnelle. type_impot = 0 'Avis d'imposition, taxe_filter.TAXE_ACTIVITE_EXCEPTIONNELLE
        self.fields['taxe'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 0, taxe_filter = TAXE_ACTIVITE_EXCEPTIONNELLE)
        
        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        self._id = int(self.instance.id or 0) #Identifiant de l'activité encours

        if self._id>0:
            if self.instance.date_validate:
                self.fields['numero_activite'].widget.attrs['disabled'] = True
                self.fields['beneficiaire'].widget.attrs['disabled'] = True
                self.fields['motif_activite'].widget.attrs['disabled'] = True
                self.fields['date_delivrance'].widget.attrs['disabled'] = True
                self.fields['date_expiration'].widget.attrs['disabled'] = True  
                self.fields['taxe'].widget.attrs['disabled'] = True
                self.fields['piece_nombre_1'].widget.attrs['disabled'] = True
                self.fields['piece_tarif_1'].widget.attrs['disabled'] = True
                self.fields['piece_nombre_2'].widget.attrs['disabled'] = True
                self.fields['piece_tarif_2'].widget.attrs['disabled'] = True
                self.fields['piece_nombre_3'].widget.attrs['disabled'] = True
                self.fields['piece_tarif_3'].widget.attrs['disabled'] = True
                self.fields['piece_nombre_4'].widget.attrs['disabled'] = True
                self.fields['piece_tarif_4'].widget.attrs['disabled'] = True
                self.fields['piece_nombre_5'].widget.attrs['disabled'] = True
                self.fields['piece_tarif_5'].widget.attrs['disabled'] = True
    
    def clean_numero_activite(self):
        """
        Generer le numero matricule avant save
        """
        numero_activite = self.cleaned_data['numero_activite']
        
        # Mode création uniquement
        if self._id == 0:
            numero_activite = ChronoHelpers.get_new_num(CHRONO_ACTIVITE_EXCEPTIONNELLE)

        return numero_activite

    def clean_date_delivrance(self):
        """
        Validation de la date début de l'activité
        """
        date_delivrance = self.cleaned_data.get('date_delivrance')

        if not is_date_valid(date_delivrance):
            raise forms.ValidationError(_("Date de délivrance invalide."))

        return date_delivrance

    def clean_date_expiration(self):
        """
        Validation de la date début de l'activité
        """
        date_expiration = self.cleaned_data.get('date_expiration')

        if not is_date_valid(date_expiration):
            raise forms.ValidationError(_("Date d'expiration invalide."))

        return date_expiration

    def clean(self):
        """
        Gestion des Validators     
        """
        beneficiaire = self.cleaned_data.get('beneficiaire')
        motif_activite = self.cleaned_data.get('motif_activite')
        date_delivrance = self.cleaned_data.get('date_delivrance')
        date_expiration = self.cleaned_data.get('date_expiration')
        
        piece_nombre_1 = self.cleaned_data.get('piece_nombre_1')
        piece_tarif_1 = self.cleaned_data.get('piece_tarif_1')
        piece_nombre_2 = self.cleaned_data.get('piece_nombre_2')
        piece_tarif_2 = self.cleaned_data.get('piece_tarif_2')
        piece_nombre_3 = self.cleaned_data.get('piece_nombre_3')
        piece_tarif_3 = self.cleaned_data.get('piece_tarif_3')
        piece_nombre_4 = self.cleaned_data.get('piece_nombre_4')
        piece_tarif_4 = self.cleaned_data.get('piece_tarif_4')
        piece_nombre_5 = self.cleaned_data.get('piece_nombre_5')
        piece_tarif_5 = self.cleaned_data.get('piece_tarif_5')

        if len(beneficiaire)<10:
            raise forms.ValidationError(_("Nom du bénéficiaire trop court. Au moins 10 caractères."))

        if len(motif_activite)<10:
            raise forms.ValidationError(_("Motif de l'activité trop court. Au moins 10 caractères."))
        
        if date_delivrance > date_expiration:
            raise forms.ValidationError(_("La date d'expiration doit être supérieur ou égale à la date de délivrance."))

        # Piece nombre et tarif 1 doivent être obligatoires
        if piece_nombre_1 <= 0:
            raise forms.ValidationError(_("Le nombre de pièces/tickets 'TYPE 1' doit être positif."))

        if piece_tarif_1 <= 0:
            raise forms.ValidationError(_("Le tarif de la pièce/ticket 'TYPE 1' doit être positif."))

        # Piece nombre/tarif de 2 à 5 sont facultatif mais seraient remplis en ordre
        if (piece_nombre_2<=0 and piece_tarif_2>0) or (piece_nombre_2>0 and piece_tarif_2<=0):
            raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 2' doivent être positifs."))

        if (piece_nombre_3<=0 and piece_tarif_3>0) or (piece_nombre_3>0 and piece_tarif_3<=0):
            raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 3' doivent être positifs."))

        if (piece_nombre_4<=0 and piece_tarif_4>0) or (piece_nombre_4>0 and piece_tarif_4<=0):
            raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 4' doivent être positifs."))
        
        if (piece_nombre_5<=0 and piece_tarif_5>0) or (piece_nombre_5>0 and piece_tarif_5<=0):
            raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 5' doivent être positifs."))

        # Controle ar ordre
        if (piece_nombre_2 + piece_tarif_2)<=0:
            if (piece_nombre_3 + piece_tarif_3)>0: 
                raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 2' doivent être mentionnés avant 'TYPE 3'."))

            if (piece_nombre_4 + piece_tarif_4)>0: 
                raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 2' doivent être mentionnés avant 'TYPE 4'."))

            if (piece_nombre_5 + piece_tarif_5)>0: 
                raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 2' doivent être mentionnés avant 'TYPE 5'."))

        if (piece_nombre_3 + piece_tarif_3)<=0:
            if (piece_nombre_4 + piece_tarif_4)>0: 
                raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 3' doivent être mentionnés avant 'TYPE 4'."))

            if (piece_nombre_5 + piece_tarif_5)>0:
                raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 3' doivent être mentionnés avant 'TYPE 5'."))
        
        if (piece_nombre_4 + piece_tarif_4)<=0:
            if (piece_nombre_5 + piece_tarif_5)>0:
                raise forms.ValidationError(_("Le nombre et tarif de pièces/tickets 'TYPE 4' doivent être mentionnés avant 'TYPE 5'."))

        return self.cleaned_data