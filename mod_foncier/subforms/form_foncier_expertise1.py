from django.utils.translation import gettext as _
from django import forms
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import intcomma

from mod_foncier.models import FoncierExpertise, FoncierTnbImpot
from mod_foncier.subviews.view_foncier_helpers import get_montant_note

from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import *

from mod_helpers.hlp_validators import *

import datetime 

class FoncierExpertiseForm(forms.ModelForm):
    """
    Form Expertise technique des terrains
    """
    # Afficher le contribuable qui correspond à l'entité seléctionnée
    contribuable = forms.CharField(required=False, label="Contribuable", help_text="Nom complet du contribuable")
    
    total_non_bati = forms.CharField(required=False, label="Total Non Bâti")
    total_bati = forms.CharField(required=False, label="Total Bâti")
    total_declaration = forms.CharField(required=False, label="Total déclaration")

    class Meta:
        model = FoncierExpertise

        fields = ('annee', 'parcelle', 'superficie_non_batie', 'impot_non_batie', 'date_declaration')

        exclude = ('user_create','user_update', 'user_validate','user_print','date_update','date_validate','date_print',)

        labels = {
            "annee": "Année",
            "parcelle": "Parcelle privée",
            "superficie_non_batie": "Superficies(non bâties)",
            "impot_non_batie": "Taux - impôt non bâti",
            "date_declaration":"Date déclaration",     
        }

        help_texts = {
            "annee": "Année d'expertise",
            "parcelle": "Numéro d’identification de la parcelle privée",    
            "superficie_non_batie": "Superficie non bâtie (en m²)",       
            "impot_non_batie": "Caractéristique de l’espace non bâtie", 
            "date_declaration": "Déclaration manuelle",
        } 

        error_messages = {
            'parcelle': {'required': ('Le numéro parcelle est obligatoire'),},
            'annee': {'required': ('Le contribuable est obligatoire'),}, 
            'superficie_non_batie': {'required': ('La superficie non bâtie est obligatoire'),},
            'impot_non_batie': {'required': ("L'impôt' non bâtie est obligatoire"),},         
        }

    def __init__(self, *args, **kwargs):

        super(FoncierExpertiseForm, self).__init__(*args, **kwargs)

        # Année : Initialiser le champs année avec l'année en cours (modifiable et unique pour chaque année)
        self.fields['annee'].initial = timezone.now().year
        self.fields['date_declaration'].initial = timezone.now()
        self.fields['annee'].widget.attrs['class'] = 'disabled-element'
        self.fields['date_declaration'].widget.attrs['class'] = 'disabled-element'

        # Identifiant de l'instance en cours
        self._id = int(self.instance.id or 0) 

        self._montant_total = 0
        self._tnb = 0
        self._tb = 0

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé        
        if self._id>0:
            # Afficher les differents montant de l'expertise
            self._montant_total, self._tnb, self._tb = get_montant_note(self.instance)
            self.fields['total_non_bati'].initial = str(intcomma(int(self._tnb))) + ' Bif'
            self.fields['total_bati'].initial = str(intcomma(int(self._tb))) + ' Bif'
            self.fields['total_declaration'].initial = str(intcomma(int(self._montant_total))) + ' Bif'

            # Filter les impôts selon l'accessibilité de la parcelle
            self.fields['impot_non_batie'].queryset = FoncierTnbImpot.objects.filter(accessibilite = self.instance.parcelle.accessibilite)

            # Désactiver les controles si toute info validée
            if self.instance.date_validate:
                self.fields['parcelle'].widget.attrs['class'] = 'disabled-element'
                self.fields['annee'].widget.attrs['class'] = 'disabled-element'
                self.fields['superficie_non_batie'].widget.attrs['class'] = 'disabled-element'
                self.fields['impot_non_batie'].widget.attrs['class'] = 'disabled-element'
                self.fields['date_declaration'].widget.attrs['class'] = 'disabled-element'

    def clean_parcelle(self):
        """
        Validation de l'année de déclaration 
        """
        parcelle = self.cleaned_data.get('parcelle')
        annee = self.cleaned_data.get('annee')

        # Si année existe pour cette déclaration alors refuser l'enregistrerment
        if self._id==0:
            obj = FoncierExpertise.objects.filter(parcelle=parcelle, annee=annee)
            if obj:
                raise forms.ValidationError(_("L'année de déclaration existe déjà pour cette parcelle."))            

        return parcelle

    def clean_annee(self):
        """
        Contrôle de l'anée
        """
        annee = self.cleaned_data.get('annee')

        # Format de l'année
        if not is_year_valid(annee):
            raise forms.ValidationError(_("Le format de l'année est érroné."))

        # Année anticipée
        if annee > timezone.now().year:
            raise forms.ValidationError(_("L'année de déclaration ne peut pas être anticipée."))

        return annee

    def clean_date_declaration(self):
        """
        Validation de la date de paiement 
        """
        date_declaration = self.cleaned_data.get('date_declaration')

        if not is_date_valid(date_declaration):
            raise forms.ValidationError(_("Date de déclaration invalide."))

        if date_declaration > datetime.date.today():
           raise forms.ValidationError(_("La date de déclaration ne doit pas dépasser la date d'aujourd'hui"))

        return date_declaration

    def save(self, commit=True):
        """
        Metre à jour certains champs calculés
        """
        self.instance.montant_tnb = self._tnb
        self.instance.montant_tb = self._tb

        taux_accroissement = self.instance.has_accroissement # property in model
        if taux_accroissement>0:
            self.instance.accroissement_taux = taux_accroissement
            self.instance.accroissement_montant = (self._montant_total * taux_accroissement)/100
        else:
            self.instance.accroissement_taux = 0
            self.instance.accroissement_montant = 0

        return super(FoncierExpertiseForm, self).save(commit)

#---------------------------------------------------------------
class ImageUploadFoncierExpertiseForm(forms.Form):
    """
    Fichier upload form.
    """
    dossier_expertise = forms.FileField(required=False)

#---------------------------------------------------------------
class FoncierExpertiseAnnulationForm(forms.ModelForm):
    """
    Annulation de la déclaration
    """
    class Meta:
        model = FoncierExpertise

        fields = ('motif_delete', )
        
        widgets = {
            'motif_delete': forms.Textarea(attrs={'rows':4, 'style':'resize:none;'}),
        }

        labels = {
            "motif_delete": "Motif d'annulation",
        }

    def clean_motif_delete(self):
        """
        Libellé obligatoire
        """
        motif_delete = self.cleaned_data['motif_delete']

        # Mode création uniquement
        if not motif_delete:
            raise forms.ValidationError(_("Le motif d'annulation doit être mentionné"))

        return motif_delete