from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Q

from mod_finance.models import AvisImposition, Taxe, Agence
from mod_parametrage.enums import *
from mod_helpers.hlp_chrono import ChronoHelpers

from datetime import datetime, date, timedelta

class AvisImpositionForm(forms.ModelForm):
    """
    Model Form : Avis d'imposition
    """
    # Champs caché contenant la taxe_filter (0 Adminsitratif pur ou 1 autres avec contribuable)
    taxe_filter = forms.CharField(required=False)

    class Meta:
        #Model correspondant
        model = AvisImposition    

        #Champs de saisie affichés
        fields = ('reference', 'nom', 'contribuable', 'libelle', 'taxe', 'taxe_montant', 'nombre_copie', 'montant_total', 'validite')
        
        #Champs exclus lors du sauvegarde (leur sauvegarde sont geré au niveau du view)
        exclude = ('taxe_filter', 'agence', 'ref_paiement', 'date_paiement', 'user_create', 'user_update', 'user_validate', 'user_print', 'date_create', 'date_update', 'date_validate', 'date_print')

        #Fomatage des champs (contrôles) de saisie
        widgets = {
            'reference': forms.TextInput(attrs={'readonly':'readonly'}),
            'taxe': forms.Select(attrs={'onChange':'ai_OnTaxeChanged()'}), #Utilisé pour chercher le montant de la taxe
            'nombre_copie': forms.TextInput(attrs={'type':'number', 'min': 1, 'onChange':'ai_OnCoastChanged()'}), #Pour calculer le total de la taxe
            'taxe_montant': forms.TextInput(attrs={'readonly':'readonly'}),
            'montant_total': forms.TextInput(attrs={'readonly':'readonly'}),
            'validite': forms.TextInput(attrs={'type':'number', 'min': 1, 'max':5}),
            'libelle': forms.Textarea(attrs={'rows':2, 'style':'resize:none;', 'readonly':'readonly'}),
        }

        #Les libellés des champs
        labels = {
            "reference": "Référence",
            "nom": "Nom et Prénoms",
            "contribuable":"Contribuable",
            "taxe": "Objet",
            "taxe_montant" : "Tarif",
            "nombre_copie" : "Quantité(s)",
            "montant_total" : "Montant total",
            "validite": "Validité",
            "libelle": "Libellé",
        }

        #Les textes d'aide (qui s'affichent en bas de chaque champs de saisie)
        help_texts = {
            "reference" : "Référence de l'avis d'imposition",
            "nom" : "Nom complet du bénéficiaire",
            "contribuable":"Information du contribuable",
            "taxe" : "Matière imposable",
            "taxe_montant" : "Tarif de l'avis",
            "nombre_copie" : "nombre de copies/quantités (min :1)",
            "montant_total" : "Montant total de l'avis",
            "validite": "En jour (max : 5)",
            "libelle": "Libelle de l'avis d'imposition",
        } 

        #Les messages d'érreur
        error_messages = {
            "reference": {
                "required" : ("Référence de l'avis d'imposition obligatoire"),
            },
            'libelle': {
                'required': ("Le libellé de la note doit être menstionné"),
            }
        }
 
    #Traitement des champs spécifiques  
    def __init__(self, *args, **kwargs):

        # taxe_filter depuis le view (mais comme on ne peut pas lire les sessions dans le form, alors
        # on passe dans le constructeur du form la session (voir la view create/update))
        self._taxe_filter = kwargs.pop('taxe_filter', None)
        
        super(AvisImpositionForm, self).__init__(*args, **kwargs)

        # Taxe : Afficher les Avis d'imposition filtré (combo)
        # Avis d'imposition (voir mod_parametrage.enum = choix_imposition (type_impot)) 
        # Pour les affaires adminitratives : taxe_filter est utilisé pour n'acceder qu'aux AI administratif ou autre      
        self.fields['taxe'].queryset = Taxe.objects.filter(categorie_taxe__type_impot = 0, taxe_filter = self._taxe_filter) 

        # Reference : Initialiser le champs référence avec le nouveau nom chrono
        self.fields['reference'].initial = 'Auto - Chorno' #ChronoHelpers.get_new_num('AI')

        # Initialiser la taxe_filter (hidden field pour faciliter la getion de nom et contribuable)
        self.fields['taxe_filter'].initial = self._taxe_filter

        # Recuperer l'ientifiant de l'avis
        self._id = int(self.instance.id or 0)

        # Désactiver tous les contrôles si l'info est valide
        if self.instance.date_validate or self._taxe_filter == str(TAXE_AI_DOCUMENT_FINANCIER) or self.instance.entity:
            self.fields['nom'].widget.attrs['readonly'] = True
            self.fields['taxe'].widget.attrs['readonly'] = True
            self.fields['nombre_copie'].widget.attrs['readonly'] = True
            self.fields['validite'].widget.attrs['readonly'] = True
            self.fields['libelle'].widget.attrs['readonly'] = True  

    def clean_reference(self):
        """
        Generer le numero matricule avant save
        """
        reference = self.cleaned_data['reference']
        
        # Mode création uniquement
        if self._id == 0:
            reference = ChronoHelpers.get_new_num(CHRONO_AVIS_IMPOSITION)

        return reference

    def clean(self):
        """
        Gestion du Nom et COntribuable
        si taxe_filter = 1, Nom est oblogatoire et contribuable null
        si taxe_filter = 0, Contrubuable est oblogatoire et nom est null
        """
        nom = self.cleaned_data['nom']
        contribuable = self.cleaned_data['contribuable']

        if self._taxe_filter == str(TAXE_AI_DOCUMENT_FINANCIER): 
            # Documents financiers
            if contribuable is None:
                raise forms.ValidationError(_("Le contribuable est recquis"))
        else:
            # Avis administratifs et autres
            if not nom:
                raise forms.ValidationError(_("Le nom du bénéficiaire est recquis"))

        return self.cleaned_data

class AvisImpositionPaiementForm(forms.ModelForm):
    """
    Model Form : Paiement Avis d'imposition
    """
    class Meta:
        #Model correspondant
        model = AvisImposition

        #Champs de saisie affichés
        fields = ('reference', 'agence', 'ref_paiement', 'date_paiement')
        
        #Champs exclu lors du sauvegarde (leur sauvegarde sont geré au niveau du view et model)
        exclude = ('user_create', 'user_update', 'user_validate', 'user_print', 'date_create', 'date_update', 'date_validate', 'date_print')

        #Les libellés des champs
        labels = {
            "reference": "Référence",
            "agence": "Agence de paiement",
            "ref_paiement": "Référence de paiement",
            "date_paiement": "Date de paiement",
        }

        #Les textes d'aide (qui s'affichent en bas de chaque champs de saisie)
        help_texts = {
            "reference": "Référence de l'avis d'imposition",
            'agence': "Banque/Mobile money/Autres",
            'ref_paiement' : 'Numéro du bordereau',
            "date_paiement": "Date du bordereau",
        } 

    #Traitement des champs spécifique 
    def __init__(self, *args, **kwargs):
        super(AvisImpositionPaiementForm, self).__init__(*args, **kwargs)

        #Agenc, afficher en combo les agences de paiement
        self.fields['agence'].queryset = Agence.objects.all()

        # Recuperer l'ientifiant de l'avis
        self._id = int(self.instance.id or 0) #Identifiant de l'activité encours

        # Désactiver tous les contrôles si l'info est valide
        if self.instance.date_validate:
            self.fields['reference'].widget.attrs['disabled'] = True
            self.fields['agence'].widget.attrs['disabled'] = True
            self.fields['ref_paiement'].widget.attrs['disabled'] = True
            self.fields['date_paiement'].widget.attrs['disabled'] = True  

    def clean_date_paiement(self):
        """
        Validation de la date de paiement 
        """
        date_paiement = self.cleaned_data.get('date_paiement')

        if date_paiement > timezone.now() :
           raise forms.ValidationError(_("La date de paiement ne doit pas dépasser la date d'aujourdh'ui"))
        
        return date_paiement

    def __si_ref_paiement_existe(self, ref_paiement, agence):
        """
        Tester si la référence de payement existe pour une agence
        (Garder l'unicité de la référence de paiement pour chaque agence)
        """
        res = False
        
        # Filtrer uniquement les reference de paiement de l'agence en parametre agence
        q = Q(agence=agence) & Q(ref_paiement=ref_paiement) 
        obj = AvisImposition.objects.filter(q)
        if obj:
            if self.instance.id is None:
                # Nouveau Avis (en mode création)
                res = True
            else:
                # Avis existant (en mode update)
                obj = obj.filter(id = self.instance.id) #Lui même
                if not obj :
                    res = True
        
        return res

    def clean_ref_paiement(self):
        """
        Validation de la référence de paiement (numéro du bordereau) 
        """
        ref_paiement = self.cleaned_data.get('ref_paiement')
        agence = self.cleaned_data.get('agence')

        if ref_paiement and agence:
            if self.__si_ref_paiement_existe(ref_paiement, agence):
                raise forms.ValidationError(_("Le numéro de référence existe déjà pour cette l'agence"))

        return ref_paiement

class AvisImpositionFileUploadForm(forms.Form):
    """
    Model Form : Upload Fichier bordereau de l'avis d'imposition
    """
    fichier_paiement = forms.FileField()