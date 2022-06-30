from django import forms
from django.utils.translation import gettext as _
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, date, timedelta

from mod_activite.models import *
from mod_finance.models import *
from mod_transport.models import *
from mod_parametrage.enums import *

from mod_helpers.hlp_validators import * 
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_periode import PeriodeHelpers

class NoteImpositionForm(forms.ModelForm):
    """
    Form : Note d'imposition pour toutes les entités
    """
    class Meta:
        # Model correspondant
        model = NoteImposition

        # Champs de saisie affichés
        fields = ('reference', 'taxe', 'periode', 'annee', 'taxe_montant', 'contribuable', 'entity_id')
        
        # Champs exclus lors du sauvegarde (leur sauvegarde sont geré au niveau du view)
        exclude = ('user_create', 'user_update', 'user_validate', 'user_print', 'date_create', 'date_update', 'date_validate', 'date_print')

        #Fomatage des champs (contrôles) de saisie
        widgets = {
            'reference': forms.TextInput(attrs={'readonly':'readonly'}),
            'taxe_montant': forms.TextInput(attrs={'readonly':'readonly'}),
        }

        #Les libellés des champs
        labels = {
            "reference": "N° Référence",
            "taxe": "Taxe à payer",
            "periode": "Période suivante",
            "annee": "Année",
            "taxe_montant" : 'Montant',
            "contribuable" : 'Contribuable',
        }

        #Les textes d'aide (qui s'affichent en bas de chaque champs de saisie)
        help_texts = {
            "reference": "Note d'imposition",
            "taxe" : "Matière imposable",
            "periode": "Période de paiement : Mensuel/Trimestriel/Annuel",
            "annee": "Année de paiement",
            "taxe_montant" : "Total de la taxe",
            "contribuable" : 'Information du contribuable',
        }

        #Les messages d'érreur
        error_messages = {
            'periode': {
                'required': ("La période de paiement doit être précisée"),
            },
            'annee': {
                'required': ("L'année de paiement doit être précisée"),
            },
        }
    
    def __init__(self, *args, **kwargs):
        # L'objet entity lors de la création 
        self._obj_entity = kwargs.pop('obj_entity', None)
        self._user = kwargs.pop('user', None)

        super(NoteImpositionForm, self).__init__(*args, **kwargs)

        # Reference : Initialiser le champs référence avec le nouveau nom chrono
        self.fields['reference'].initial = 'Auto - Chorno' # ChronoHelpers.get_new_num('NI')

        # Recuperer l'ientifiant de l'objet note d'imposition
        self._id = int(self.instance.id or 0)
        
        # Gestion de contrôles : Désactiver tous le champs de saisie si la note est validée
        if isinstance(self.instance, NoteImposition) and self._id:
            obj = NoteImposition.objects.get(id=self._id)
            if obj and obj.date_validate:
                self.fields['periode'].widget.attrs['disabled'] = True
                self.fields['annee'].widget.attrs['disabled'] = True
        
    def clean_reference(self):
        """
        Generer le numero matricule avant save
        """
        reference = self.cleaned_data['reference']
        
        # Mode création uniquement
        if self._id == 0:
            reference = ChronoHelpers.get_new_num(CHRONO_NOTE_IMPOSITION)

        return reference
    
    def clean(self):
        """
        Gestion des Validators 
        """        
        #Champs uniques : entity_id+periode+annee (entity_id = id de l'activité)
        periode = self.cleaned_data['periode'] #OU periode = self.cleaned_data.get('periode')
        annee = self.cleaned_data['annee']

        error_messages = []

        # Si Année anticipative alors refuser
        if annee > timezone.now().year:
            error_messages.append("Le payement anticipatif de la note pour " + str(annee) + " n'est pas permis.")

        # Si Année < anée écriture de l'objet alors refuser
        # if self._obj_entity:
        #     if annee < self._obj_entity.date_ecriture.year:
        #         error_messages.append("L'année " + str(annee) + " n'est plus valide")

        # Tester si l'objet a été déjà générée pour cette période
        q = Q(periode__exact=periode) & Q(annee__exact=annee) & Q(entity__exact=ENTITY_ACTIVITE_STANDARD) &  Q(entity_id__exact=self._obj_entity.id)  # UNICITE
        obj = NoteImposition.objects.filter(q)
        if obj:
            error_messages.append("La taxe de cette activité a été déjà payée pour la période (" + periode.get_element_display() + " " +  str(annee) + ")")

        if len(error_messages):
            raise forms.ValidationError(_(' & '.join(error_messages)))

        return self.cleaned_data

    # Metre à jour la traçailité (la note est automatiquement validée) avec entity id
    def save(self, commit=True):
        dateTimeNow = datetime.datetime.now()

        # Traçabilité
        self.instance.date_update = dateTimeNow
        self.instance.user_update = self._user
        self.instance.date_validate = dateTimeNow
        self.instance.user_validate = self._user

        # Entty id
        self.instance.entity_id = self._obj_entity.id

        return super(NoteImpositionForm, self).save(commit)

    # Détécter la période suivante
    def GetNextPeriodeByNote(self, entity, entity_id):
        """
        Lire la période suivante d'une note d'imposition
        """
        next_periode = None

        obj_note = NoteImposition.objects.filter(entity=entity, entity_id=entity_id).order_by('-id').first()
        if obj_note:
            next_periode = PeriodeHelpers.getNextPeriode(obj_note.periode)

        return next_periode

#----------------------------------------------------------------
class NI_ActiviteStandardForm(NoteImpositionForm):
    """
    Note d'ImpositionForm : Activité Standard
    """
    def __init__(self, *args, **kwargs):
        super(NI_ActiviteStandardForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = "Réf Acivité"
        self.fields['entity_id'].help_text = "Activité standard"

        if isinstance(self._obj_entity, Standard):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.taxe.periode_type)

            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_ACTIVITE_STANDARD, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id
            else:
                # Changer le libellé de la période
                self.fields['periode'].label = '-------'

            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.taxe.tarif
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    # Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_ACTIVITE_STANDARD #choix_entity_imposition = Standard)
        
        return super(NI_ActiviteStandardForm, self).save(commit)

#----------------------------------------------------------------
class NI_AllocationPlaceMarcheForm(NoteImpositionForm):
    """
    Note d'Imposition Form : Allocation de place dans le marché
    """
    def __init__(self, *args, **kwargs):
        super(NI_AllocationPlaceMarcheForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = "Réf allocation"
        self.fields['entity_id'].help_text = "Place dans le marché"

        if isinstance(self._obj_entity, AllocationPlaceMarche):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.taxe.periode_type)

            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_ALLOCATION_PLACE_MARCHE, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id
            else:
                self.fields['periode'].initial =  PeriodeHelpers.getCurrentPeriode(self._obj_entity.vehicule.sous_categorie.taxe_stationnement.periode_type, self._obj_entity.date_debut)

            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.droit_place_marche.cout_place
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    # Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_ALLOCATION_PLACE_MARCHE #choix_entity_imposition = AllocationPlaceMarche)

        return super(NI_AllocationPlaceMarcheForm, self).save(commit)

#----------------------------------------------------------------
class NI_ActiviteMarcheForm(NoteImpositionForm):
    """
    Note d'ImpositionForm : Activité Marché
    """
    def __init__(self, *args, **kwargs):
        super(NI_ActiviteMarcheForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = "Réf activité"
        self.fields['entity_id'].help_text = "Activité dans le marché"

        if isinstance(self._obj_entity, Marche):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.taxe.periode_type)

            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_ACTIVITE_MARCHE, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id

            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.taxe.tarif
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    #Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_ACTIVITE_MARCHE #choix_entity_imposition = Marche)

        return super(NI_ActiviteMarcheForm, self).save(commit)

#----------------------------------------------------------------
class NI_AllocationEspacePubliqueForm(NoteImpositionForm):
    """
    Note d'Imposition Form : Allocation/Occupation/Exploitation espace publique
    """
    def __init__(self, *args, **kwargs):
        super(NI_AllocationEspacePubliqueForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = "Réf allocation"
        self.fields['entity_id'].help_text = "Espace publique"

        if isinstance(self._obj_entity, AllocationEspacePublique):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.taxe.periode_type)

            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_ALLOCATION_ESPACE_PUBLIQUE, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id

            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.superficie * self._obj_entity.taxe.tarif
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    #Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_ALLOCATION_ESPACE_PUBLIQUE #choix_entity_imposition = AllocationEspacePublique)

        return super(NI_AllocationEspacePubliqueForm, self).save(commit)

#----------------------------------------------------------------
class NI_AllocationPanneauPublicitaireForm(NoteImpositionForm):
    """
    Note d'Imposition Form : Allocation des panneaux publicitaires
    """
    def __init__(self, *args, **kwargs):
        super(NI_AllocationPanneauPublicitaireForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = "Réf allocation"
        self.fields['entity_id'].help_text = "Panneau publicitaire"

        if isinstance(self._obj_entity, AllocationPanneauPublicitaire):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.taxe.periode_type)
            
            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id

            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.superficie * self._obj_entity.taxe.tarif
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    #Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_ALLOCATION_PANNEAU_PUBLICITAIRE #choix_entity_imposition = AllocationPanneauPublicitaire)

        return super(NI_AllocationPanneauPublicitaireForm, self).save(commit)

#----------------------------------------------------------------
class NI_PubliciteMurClotureForm(NoteImpositionForm):
    """
    Note d'Imposition Form : Publicités sur les murs et clôtures
    """
    def __init__(self, *args, **kwargs):
        super(NI_PubliciteMurClotureForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = "Réf publicité"
        self.fields['entity_id'].help_text = "Mur et/ou clôture"

        if isinstance(self._obj_entity, PubliciteMurCloture):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.taxe.periode_type)

            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_PUBLICITE_MUR_CLOTURE, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id

            # Mettre le libellé
            # Libellé de la note (Par défaut = libellé de la taxe)
            type_publicite = ''
            if self._obj_entity.type_publicite == MUR:
                type_publicite = ' le mur'
            else:
                type_publicite = ' la clôture'
            
            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.superficie * self._obj_entity.taxe.tarif
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    #Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_PUBLICITE_MUR_CLOTURE #choix_entity_imposition = PubliciteMurCloture)

        return super(NI_PubliciteMurClotureForm, self).save(commit)

#----------------------------------------------------------------
class NI_VehiculeActiviteForm(NoteImpositionForm):
    """ 
    Note d'ImpositionForm : Taxe sur les Transport rémunéré Activité
    """
    def __init__(self, *args, **kwargs):
        super(NI_VehiculeActiviteForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = 'N° Carte'
        self.fields['entity_id'].help_text = "Carte municipale"

        if isinstance(self._obj_entity, VehiculeActivite):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.vehicule.sous_categorie.taxe_activite.periode_type)

            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_VEHICULE_ACTIVITE, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id
            else:
                self.fields['periode'].initial =  PeriodeHelpers.getCurrentPeriode(self._obj_entity.vehicule.sous_categorie.taxe_stationnement.periode_type, self._obj_entity.date_debut)
            
            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.vehicule.sous_categorie.taxe_activite.tarif
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    #Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_VEHICULE_ACTIVITE #choix_entity_imposition = VehiculeActivite)

        return super(NI_VehiculeActiviteForm, self).save(commit)

#----------------------------------------------------------------
class NI_DroitStationnementForm(NoteImpositionForm):
    """
    Note d'ImpositionForm : Taxe sur les droits de stationnement (Transport)
    """
    def __init__(self, *args, **kwargs):
        super(NI_DroitStationnementForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = 'N° Carte'
        self.fields['entity_id'].help_text = "Carte municipale"

        if isinstance(self._obj_entity, VehiculeActivite):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.vehicule.sous_categorie.taxe_stationnement.periode_type)

            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_DROIT_STATIONNEMENT, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id
            else:
                self.fields['periode'].initial = PeriodeHelpers.getCurrentPeriode(self._obj_entity.vehicule.sous_categorie.taxe_stationnement.periode_type, self._obj_entity.date_debut)

            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.vehicule.sous_categorie.taxe_stationnement.tarif
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    # Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_DROIT_STATIONNEMENT #choix_entity_imposition = ENTITY_DROIT_STATIONNEMENT)

        return super(NI_DroitStationnementForm, self).save(commit)

#----------------------------------------------------------------
class NI_VehiculeProprietaireForm(NoteImpositionForm):
    """
    Note d'ImpositionForm : Taxe sur les propritaires (véhicule sans plaque d'immatriculaton et 
    qui n'exerce pas d'activité municipale 
    """
    def __init__(self, *args, **kwargs):
        super(NI_VehiculeProprietaireForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = 'N° Carte'
        self.fields['entity_id'].help_text = "Carte de propriété"

        if isinstance(self._obj_entity, VehiculeProprietaire):
            # Determiner la période
            self.fields['periode'].queryset = Periode.objects.filter(periode_type=self._obj_entity.vehicule.sous_categorie.taxe_proprietaire.periode_type)

            # Détécter la période suivante
            next_periode = self.GetNextPeriodeByNote(ENTITY_VEHICULE_PROPRIETE, self._obj_entity.id)
            if next_periode:
                self.fields['periode'].initial = next_periode.id

            # Mettre le montant de l'activité
            self.fields['taxe_montant'].initial = self._obj_entity.vehicule.sous_categorie.taxe_proprietaire.tarif
        else:
            # Changer le libellé de la période
            self.fields['periode'].label = 'Période'

    #Metre à jour entity
    def save(self, commit=True):
        self.instance.entity = ENTITY_VEHICULE_PROPRIETE #choix_entity_imposition = VehiculeProprietaire)

        return super(NI_VehiculeProprietaireForm, self).save(commit)

#----------------------------------------------------------------
class NI_ImpotFoncierForm(NoteImpositionForm):
    """
    Note d'ImpositionForm : Impôt sur les parcelles (Gestion foncière)
    """
    def __init__(self, *args, **kwargs):
        super(NI_ImpotFoncierForm, self).__init__(*args, **kwargs)

        self.fields['entity_id'].label = 'Réf déclaration'
        self.fields['entity_id'].help_text = "Déclaration foncière"

#----------------------------------------------------------------
#------- PRINT form: Impression de la note la quittance ---------
#----------------------------------------------------------------
class NoteImpositionPrintForm(forms.ModelForm):
    """
    Form Impression : Mattre à jour du numero de la carte physique avant l'impression de la carte
    """
    nombre_impression = forms.CharField(required=False, label="Nombre d'impressions", help_text="Information de l'impression")

    class Meta:
        model = NoteImposition

        fields = ('numero_carte_physique', )

        labels = {
            "numero_carte_physique": "N° de la carte physique",
        }

        help_texts = {
            "numero_carte_physique": "Numéro de la carte se trouvant sur le papier sécurisé",
        }

    def __init__(self, *args, **kwargs):
        super(NoteImpositionPrintForm, self).__init__(*args, **kwargs)
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

#----------------------------------------------------------------
#------- UPLOAD form: Fichier Carte Municipale EXTERNE ----------
#----------------------------------------------------------------
class NoteImpositionFileUploadExterneForm(forms.Form):
    """
    Model Form : Upload Fichier bordereau de l'avis d'imposition
    """
    paiement_externe_file = forms.FileField()


class ChangerNumeroBordereau(forms.Form):
    ref_paiement = forms.CharField(required=False, label="Numero bordereau")
    
    def ref_paiment(self):
        ref_paiement = self.cleaned_data['ref_paiement']

        return ref_paiement