from django import forms
from django.db.models import Q
from django.utils.translation import gettext as _
from datetime import datetime, date, timedelta

from mod_finance.models import *
from mod_parametrage.enums import *

#Form : Paiement de note d'imposition
class NoteImpositionPaiementForm(forms.ModelForm):
    _ni_pk = 0 #Identifiant de la note d'imposition
    _taxe_montant = 0 #Montant de la taxe totale à payer
    _taxe_montant_paye = 0  #Montant total de la taxe payé 
    _montant_restant_du = 0 #Montant reste à payer : utilisé ce champs virtuel pour tester la validité du montant de la tranche à payer

    _id = 0 #Id du paiement de la note d'imposition

    # Montant totale de la note (read only)
    montant_total = forms.CharField(label="Information du paiement", help_text="Montant Total et Payé")

    class Meta:
        #Model correspondant
        model = NoteImpositionPaiement
       
        #Champs de saisie affichés
        fields = ('montant_tranche', 'agence', 'ref_paiement', 'date_paiement', 'montant_excedant', )
        
        #Champs exclus lors du sauvegarde (leur sauvegarde sont geré au niveau du view)
        exclude = ('user_create', 'user_update', 'user_validate', 'user_print', 'date_create', 'date_update', 'date_validate', 'date_print')

        #Les libellés des champs
        labels = {
            'montant_tranche' : 'Montant du bordereau',
            'agence' : 'Agence de paiement',
            'ref_paiement' : 'Référence du bordereau',
            'date_paiement' : 'Date du bordereau',
            'montant_excedant' : 'Montant Excedant',
        }

        #Les textes d'aide (qui s'affichent en bas de chaque champs de saisie)
        help_texts = {
            'montant_tranche' : 'A payer ou Reste à payer',
            'agence': "Banque/Mobile money/Autres",
            'ref_paiement' : 'Numéro de référence du bordereau',
            "date_paiement": "Date de paiement",
            'montant_excedant' : 'A payer prochainement',
        } 

        #Les messages d'érreur
        error_messages = {
            'agence': {
                'required': ("Agence de paiement obligatoire"),
            },
            'ref_paiement': {
                'required': ("Référence de paiement obligatoire"),
            }
        }

     #Traitement des champs spécifiques
    def __init__(self, *args, **kwargs):

        #ni_pk : depuis le view (mais comme on ne peut pas lire les sessions dans le form, alors
        #on passe dans le constructeur du form la session et sera recuperé via ni_pk (voir la view create/update))
        self._ni_pk = kwargs.pop('ni_pk', None)

        super(NoteImpositionPaiementForm, self).__init__(*args, **kwargs)

        obj = NoteImposition.objects.get(id=self._ni_pk)

        self.fields['montant_total'].initial = 'Total : ' + str(intcomma(round(obj.taxe_montant))) +  ' | Payé : ' +  str(intcomma(round(obj.taxe_montant_paye))) + ' | Reste à payer : ' + str(intcomma(round(obj.taxe_montant - obj.taxe_montant_paye)))
        self.fields['montant_total'].widget.attrs['readonly'] = True

        # Initialiser le montant en tranche = montant total
        # self.fields['montant_tranche'].initial = round(obj.taxe_montant - obj.taxe_montant_paye)

        self._taxe_montant = round(obj.taxe_montant)
        self._taxe_montant_paye = round(obj.taxe_montant_paye)
        self._montant_restant_du = round(obj.taxe_montant - obj.taxe_montant_paye)

        self._id = int(self.instance.id or 0) #Identifiant du paiement de la note d'imposition

        #Gestion de contrôles : Désactiver tous le champs de saisie si le paiement dejà éfféctué
        if self._id>0:
            obj_paie = NoteImpositionPaiement.objects.get(id=self._id)
            if obj_paie:
                if obj_paie.date_validate:
                    self.fields['montant_tranche'].widget.attrs['disabled'] = True
                    self.fields['agence'].widget.attrs['disabled'] = True
                    self.fields['ref_paiement'].widget.attrs['disabled'] = True
                    self.fields['date_paiement'].widget.attrs['disabled'] = True
    
    # Metre à jour NoteImposition
    def save(self, commit=True):
        self.instance.note_imposition = NoteImposition.objects.get(id=self._ni_pk)

        return super(NoteImpositionPaiementForm, self).save(commit)

    def __si_ref_paiement_existe(self, ref_paiement, agence):
        """
        Tester si la référence de payement existe pour une agence
        (Garder l'unicité de la référence de paiement pour chaque agence)
        """
        res = False
        
        # Filtrer uniquement les reference de paiement de l'agence en parametre agence
        q = Q(agence=agence) & Q(ref_paiement=ref_paiement) 
        
        obj = NoteImpositionPaiement.objects.filter(q)
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
        
    def clean(self):
        """
        Gestion des Validators 
        """
        montant_tranche = self.cleaned_data['montant_tranche'] #new montant

        error_messages = []
        
        if (self._id > 0):
            # Update ligne payement
            lst = NoteImpositionPaiement.objects.filter(note_imposition=self._ni_pk)
            somme = 0
            for o in lst:
                if o.id == self._id:
                    somme += montant_tranche
                    self._taxe_montant_paye -= o.montant_tranche
                else:
                    somme += o.montant_tranche

            if (somme > self._taxe_montant):
                error_messages.append("Le montant reste à payer doit être inférieur ou égal à " + str(self._taxe_montant - self._taxe_montant_paye)) + " Bif"
        else:
            # Create ligne payement 
            if self._montant_restant_du == 0:
                error_messages.append("Paiement déjà effectué")
            elif ( montant_tranche > self._montant_restant_du ):
                error_messages.append("Le montant reste à payer doit être inférieur ou égal à " + str(self._montant_restant_du)) + " Bif"

        # Excedant
        montant_excedant = self.cleaned_data['montant_excedant']
        if (self._montant_restant_du - montant_tranche > 0) and (montant_excedant>0):
            error_messages.append("Le montant de l'excedant doit être (0 Bif) car le montant restant dû est encore positif (" + str(self._montant_restant_du - montant_tranche) + " Bif)")

        if len(error_messages):
            raise forms.ValidationError(' & '.join(error_messages))

        return self.cleaned_data

#------------------------------------------------------------------------
class NoteImpositionPaiementFileUploadForm(forms.Form):
    """Upload Fichier bordereau de la note d'imposition"""
    fichier_paiement = forms.FileField()