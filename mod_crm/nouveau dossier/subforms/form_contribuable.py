from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.admin import widgets
from django.db.models import Q

from mod_crm.models import *
from mod_parametrage.models import RueOuAvenue
from mod_helpers.hlp_chrono import ChronoHelpers
from mod_helpers.hlp_validators import *

from mod_parametrage.enums import *

from datetime import datetime
import re

#------------------------------------------------------------------------------ 
class PhysiqueForm(forms.ModelForm):
    """
    Formulaire : Contribuable personne physique
    """
    class Meta:
        model = PersonnePhysique

        fields = ('matricule','nom', 'adresse', 'numero_rueavenue', 'numero_police', 'code_postal', 'tel',
            'email', 'date_naiss' , 'sexe', 'lieu_naiss','identite', 
            'identite_numero', 'adresse_exacte', 'nif_numero', 'photo_file',)

        exclude = ('user_create', 'user_update', 'user_validate', 'date_update', 'date_validate')

        widgets = {
            'matricule': forms.TextInput(attrs={"readonly":'readonly', 'placeholder':'Auto - Chorno ...'}),
            'nom': forms.TextInput(attrs={'placeholder':'Le nom et prénom ...'}),
            'identite_numero': forms.TextInput(attrs={'placeholder':"Le numéro d'identité ..."}),
            'lieu_naiss': forms.TextInput(attrs={'placeholder':'Le lieu de naissance ...'}),
            'code_postal': forms.TextInput(attrs={'placeholder':'Le code postal ...'}),
            'tel': forms.TextInput(attrs={'placeholder':'Le téléphone ...'}),
            'email': forms.TextInput(attrs={'placeholder':"L'adresse éléctronique ..."}),
            'numero_police': forms.TextInput(attrs={'placeholder':'Le numéro de police ...'}),
            'adresse_exacte': forms.TextInput(attrs={'placeholder':'Autre adrese ...'}),
            'nif_numero': forms.TextInput(attrs={'placeholder':'numéro du NIF ...'}),
        }

        labels = {
            "matricule": "Martricule",
            "nom": "Nom et Prénom",
            "date_naiss": "Date de naissance",
            "sexe":"Sexe",
            "lieu_naiss":"Lieu de naissance",
            "identite":"Type",
            "identite_numero" : "Numéro d'identité",
            "code_postal":"Code postal",
            "tel": "N° Tél",
            "email": "Email",
            "adresse": "Adresse du domicile",
            "numero_rueavenue": "Rue-Avénue",
            "numero_police": "N° Police",
            "adresse_exacte": "Autre adresse de domiciliation",
            'nif_numero': 'N° NIF',
        }

        help_texts = {
            "matricule": "Identifiant du contribuable",
            "nom": "Nom complet",
            "date_naiss": "Format (JJ/MM/AAAA)",
            "sexe":"Féminin/Masculin",
            "lieu_naiss":"Votre lieu de naissance",
            "identite":"CNI ou Passeport",
            "identite_numero" : "Numéro de CNI ou Passeport",            
            "code_postal":"Format : entier",
            "tel":"Numéro de téléphone valide",
            "email":"Adresse email valide",
            "adresse":"Commune - Zone - Quartier",
            "numero_rueavenue":"Rue-Avenue-Boulevard",
            "numero_police":"Le numéro du logement",
            "adresse_exacte": "Pays, ville, provine, région, ...",
            'nif_numero': "Numéro d'identité fiscale",
        }

        error_messages = {
            'nom': {
                'required': ('Le nom est obligatoire'),
            }
        }

    def __init__(self, *args, **kwargs):
        super(PhysiqueForm, self).__init__(*args, **kwargs)
        
        # New numero contribuable : Initialiser le champs matricule avec le nouveau nom chrono
        # 18 : Province, 0 : Personne Physique
        # self.fields['matricule'].initial = ChronoHelpers.get_new_num('180')
        self.fields['matricule'].initial = 'Auto - Chorno'

        # Identifiant du contribuable encours
        self._id = int(self.instance.id or 0)

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        if self._id>0:
            if self.instance.date_validate:
                self.fields['nom'].widget.attrs['disabled'] = True
                self.fields['numero_rueavenue'].widget.attrs['disabled'] = True
                self.fields['date_naiss'].widget.attrs['disabled'] = True
                self.fields['identite'].widget.attrs['disabled'] = True
                self.fields['numero_police'].widget.attrs['disabled'] = True
                self.fields['code_postal'].widget.attrs['disabled'] = True
                self.fields['tel'].widget.attrs['disabled'] = True
                self.fields['email'].widget.attrs['disabled'] = True
                self.fields['sexe'].widget.attrs['disabled'] = True
                self.fields['lieu_naiss'].widget.attrs['disabled'] = True
                self.fields['identite_numero'].widget.attrs['disabled'] = True
                self.fields['adresse_exacte'].widget.attrs['disabled'] = True
                self.fields['nif_numero'].widget.attrs['disabled'] = True

    def clean_matricule(self):
        """
        Generer le numero matricule avant save
        """
        matricule = self.cleaned_data['matricule']
        
        # Mode création uniquement
        if self._id == 0: 
            matricule = ChronoHelpers.get_new_num(CHRONO_PERSONNE_PHYSIQUE)

        return matricule

    def clean_nif_numero(self):
        """
        Validation du numero du nif, non obligatoire matricule mais UNIQUE
        """
        nif_numero = self.cleaned_data.get('nif_numero')
        if nif_numero:
            if self._id>0:
                # Mode update
                obj = Contribuable.objects.filter(nif_numero = nif_numero).exclude(id = self._id)
            else:
                # Mode creation
                obj = Contribuable.objects.filter(nif_numero = nif_numero)
            if obj:
                raise forms.ValidationError(_("Le numéro du NIF existe déjà"))

        return nif_numero

    def clean(self):
        """
        Validations des champs spécifique
        """
        # Validation du nom
        nom = str(self.cleaned_data.get('nom')).strip()
        if not is_alpha_only(nom):
            raise forms.ValidationError(_("Le nom doit être en lettre uniquement."))            
        if len(nom)<4:
            raise forms.ValidationError(_("Nom trop court. Au moins 4 caractères."))
    
        # Validation de la date de naissance
        date_naiss = self.cleaned_data.get('date_naiss')

        if not is_date_valid(date_naiss):
            raise forms.ValidationError(_("Date de naissance invalide."))

        # Validation de la date de naissance  (minimum 16 ans)
        age = datetime.now().year - date_naiss.year
        if  age < 16 :
            raise forms.ValidationError(_("La date de naissance minimale est de 16 ans."))            

        # Validation deu code postal (en chiffre uniquement), facultatif
        code_postal = self.cleaned_data.get('code_postal')
        if code_postal:
            if not is_number_only(str(code_postal).strip()):
                raise forms.ValidationError(_("Le code postal doit être en chiffre uniquement."))            

        # Validation de d'adresse email, facultatif
        email = self.cleaned_data.get('email')
        if email:
            if not is_email_valid(email):
                raise forms.ValidationError(_("Addresse email invalide."))

        # Validation du numéro de tél, facultatif
        tel = self.cleaned_data.get('tel')
        if tel:
            if not is_phone_valid(tel):
                raise forms.ValidationError(_("Numéro de téléphone invalide."))
    
        # Validation des adresses (Minimun une adresse doit être indiquée)
        adresse_exacte = self.cleaned_data.get('adresse_exacte')
        adresse = self.cleaned_data.get('adresse')
        numero_rueavenue = self.cleaned_data.get('numero_rueavenue')

        if adresse_exacte is None and adresse is None:
            raise forms.ValidationError(_("Veuillez indiquer l'adresse du domicile."))
        
        if adresse and numero_rueavenue:
            if not is_rue_avenue_exists(adresse, numero_rueavenue):
                raise forms.ValidationError(_("Cette rue-avenue n'existe pas pour l'adresse seléctionnée"))

        return self.cleaned_data

#------------------------------------------------------------------------------
class MoraleForm(forms.ModelForm):
    """
    Formulaire : Contribuable personne morale
    """
    class Meta:
        model = PersonneMorale
        
        fields = ('matricule','nom', 'adresse', 'numero_rueavenue', 'numero_police', 'code_postal', 'tel', 
            'email', 'nif_numero', 'rc_numero', 'type_caractere', 'adresse_exacte')
        
        exclude = ('user_create', 'user_update', 'user_validate', 'date_update', 'date_validate')
        
        widgets = {
            'matricule': forms.TextInput(attrs={"readonly":'readonly', 'placeholder':'Auto - Chorno ...'}),
            'nom': forms.TextInput(attrs={'placeholder':'Le nom de la société ou organisme ...'}),
            'code_postal': forms.TextInput(attrs={'placeholder':'Le code postal ...'}),
            'tel': forms.TextInput(attrs={'placeholder':'Le téléphone ...'}),
            'email': forms.TextInput(attrs={'placeholder':"L'adresse éléctronique ..."}),
            'nif_numero': forms.TextInput(attrs={'placeholder':'numéro du NIF ...'}),
            'rc_numero': forms.TextInput(attrs={'placeholder':'Le numéro du registre de commerce ...'}),
            'numero_police': forms.TextInput(attrs={'placeholder':'Le numéro de police ...'}),
            'adresse_exacte': forms.TextInput(attrs={'placeholder':'Autre adrese ...'}),
            'type_caractere': forms.Select(attrs={"onChange":'OnTypeCaractereChanged()'}),
        }

        labels = {
            "matricule": "Martricule",
            "nom": "Dénomination",
            "nif_numero": "N° NIF",
            "rc_numero": "N° RC",
            "type_caractere": "Caractère",
            "code_postal":"CP",
            "tel": "N° Tél",
            "email": "Email",
            "adresse": "Adresse du siège",
            "numero_rueavenue": "N° Rue",
            "numero_police": "N° Police",
            "adresse_exacte": "Autre adresse du siège",
            'nif_numero': 'N° NIF',
        }

        help_texts = {
            "matricule": "Identifiant du contribuable",
            "nom": "Nom de raison sociale",
            "nif_numero": "Numéro de statut (NIF)",
            "rc_numero": "Registre de commerce",
            "type_caractere": "Type de caractère",
            "code_postal":"Format : entier",
            "tel":"Format internatonal valide",
            "email":"Adresse email valide",
            "adresse":"Commune - Zone - Quartier",
            "numero_rueavenue":"Avenue - Rue -Boulevar",
            "numero_police":"Le numéro du logement",
            "adresse_exacte": "En face de X, à côté de X, Derrière l'immeuble X ...",
            'nif_numero': "Numéro d'identité fiscale",
        }

        error_messages = {
            'matricule': {
                'required': ('Le matricule est obligatoire'),
            }
        }
    
    def __init__(self, *args, **kwargs):
        super(MoraleForm, self).__init__(*args, **kwargs)

        # New numero contribuable : Initialiser le champs matricule avec le nouveau nom chrono
        # 18 : Province, 1 : Personne Morale
        # self.fields['matricule'].initial = ChronoHelpers.get_new_num('181')
        self.fields['matricule'].initial = 'Auto - Chorno'

        # Initialiser le tél à '+257'
        self.fields['tel'].initial = '+257'
        
        # Identifiant du contribuable encours
        self._id = int(self.instance.id or 0)

        # Gestion de contrôles : Désactiver tous le champs de saisie si l'objet est validé
        if self._id>0:
            if self.instance.date_validate:
                self.fields['nom'].widget.attrs['disabled'] = True
                self.fields['numero_rueavenue'].widget.attrs['disabled'] = True
                self.fields['numero_police'].widget.attrs['disabled'] = True
                self.fields['code_postal'].widget.attrs['disabled'] = True
                self.fields['tel'].widget.attrs['disabled'] = True
                self.fields['email'].widget.attrs['disabled'] = True
                self.fields['nif_numero'].widget.attrs['disabled'] = True
                self.fields['rc_numero'].widget.attrs['disabled'] = True
                self.fields['type_caractere'].widget.attrs['disabled'] = True
                self.fields['adresse_exacte'].widget.attrs['disabled'] = True

    def clean_matricule(self):
        """
        Generer le numero matricule avant save
        """
        matricule = self.cleaned_data['matricule']
        
        # Mode création uniquement
        if self._id == 0:
            matricule = ChronoHelpers.get_new_num(CHRONO_PERSONNE_MORALE)

        return matricule

    def __si_nom_existe(self, nom):
        """
        Tester si le nom du contribuable (personne morale) existe
        """
        res = False
        
        # Filtrer uniquement le contribuable morale                    
        q = Q(matricule__startswith=str(CHRONO_PERSONNE_MORALE)) & Q(nom__icontains=nom) 
        obj = PersonneMorale.objects.filter(q)
        if obj:
            if self.instance.id is None:
                # Nouvelle personne morale (en mode création)
                res = True
            else:
                # Personne morale existante (en mode update)
                obj = obj.filter(id = self.instance.id) #Lui même
                if not obj :
                    res = True
        
        return res

    def clean(self):
        """
        Validations des champs spécifique
        """
        # Validation du nom, obligatoire
        nom = str(self.cleaned_data.get('nom')).strip()
        if len(nom)<5:
            raise forms.ValidationError(_("Nom trop court. Au moins 5 caractères."))

        # Morale : Le nom est unique
        if self.__si_nom_existe(nom):
            raise forms.ValidationError(_("Le nom de la personne modale existe déjà."))

        # Validation du numero de rc, obligatoire pour COMMERCIAL, facultatif pour LUCRATIF
        rc_numero = self.cleaned_data.get('rc_numero')
        type_caractere = self.cleaned_data.get('type_caractere')
        if type_caractere == COMMERCIAL:
            if len(rc_numero.strip()) == 0:
                raise forms.ValidationError(_("Le registre de commerce est recquis pour les sociétés commerciales."))
            else:
                if self._id>0:
                    # Mode update
                    obj = PersonneMorale.objects.filter(rc_numero = rc_numero).exclude(id = self._id)
                else:
                    # Mode creation
                    obj = PersonneMorale.objects.filter(rc_numero = rc_numero)
                if obj:
                    raise forms.ValidationError(_("Le registre de commerce existe déjà"))

        # Validation du NIF
        nif_numero = self.cleaned_data.get('nif_numero')
        if type_caractere!=ASSOCIATION:
            if not nif_numero:
                raise forms.ValidationError(_(str("Le NIF est recquis")))       
            else:
                if self._id>0:
                    # Mode update
                    obj = PersonneMorale.objects.filter(nif_numero = nif_numero).exclude(id = self._id)
                else:
                    # Mode creation
                    obj = PersonneMorale.objects.filter(nif_numero = nif_numero)
                if obj:
                    raise forms.ValidationError(_("Le numéro du NIF existe déjà"))

        # Validation deu code postal (en chiffre uniquement), facultatif
        code_postal = self.cleaned_data.get('code_postal')
        if code_postal:
            if not is_number_only(str(code_postal).strip()):
                raise forms.ValidationError(_("Le code postal doit être en chiffre uniquement."))            

        # Validation de d'adresse email, facultatif
        email = self.cleaned_data.get('email')
        if email:
            if not is_email_valid(email):  
                raise forms.ValidationError(_("Addresse email invalide."))     

        # Validation du numéro de tél (obligatoire)
        tel = str(self.cleaned_data.get('tel').strip())
        if not is_phone_valid(tel):
            raise forms.ValidationError(_("Numéro de téléphone invalide."))
            
        # Validation des adresses
        adresse = self.cleaned_data.get('adresse')
        numero_rueavenue = self.cleaned_data.get('numero_rueavenue')
        
        # Adressse obligatoire
        if adresse is None:
            raise forms.ValidationError(_("Veuillez indiquer l'adresse du siège."))

        # RueAvenue Obligatoire
        if numero_rueavenue is None:
            raise forms.ValidationError(_("Veuillez indiquer le numéro de rue/avenue/boulevard"))

        # Vérifier la liaison
        if adresse and numero_rueavenue:
            if not is_rue_avenue_exists(adresse, numero_rueavenue):
                raise forms.ValidationError(_("Cette rue-avenue n'existe pas pour l'adresse seléctionnée"))

        return self.cleaned_data

#------------------------------------------------------------------------------
class ImageUploadPhysiqueForm(forms.Form):
    """
    Image/File upload form.
    """
    identite_file = forms.FileField(required=False)
    photo_file = forms.FileField(required=False)
    nif_file = forms.FileField(required=False)

#------------------------------------------------------------------------------
class ImageUploadMoraleForm(forms.Form):
    """
    File upload form.
    """
    nif_file = forms.FileField(required=False)
    rc_file = forms.FileField(required=False)