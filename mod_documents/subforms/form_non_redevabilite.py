from django.utils.translation import ugettext_lazy as _
from django import forms

from mod_activite.models import Standard
from mod_documents.submodels.model_non_redevabilite import NonRedevabilite
from mod_finance.models import Taxe

from mod_parametrage.enums import *
from mod_parametrage.models import RueOuAvenue

from mod_helpers.hlp_validators import *
from mod_helpers.hlp_chrono import ChronoHelpers


class NonRedevabiliteForm(forms.ModelForm):
    """
    Form Activté Standard
    """

    class Meta:
        model = NonRedevabilite

        fields = ('reference', 'contribuable', 'libelle',)

        exclude = ('user_create',)

        widgets = {
            'reference': forms.TextInput(attrs={'readonly': 'readonly'}),
            'contribuable': forms.Select(attrs={"onChange": 'OnTypeEspaceChanged()'}),
        }

        labels = {
            "reference": "N° de référence",
            "contribuable": "Contribuable",
            "libelle": "Motif",
        }

        help_texts = {
            "reference": "Numéro de référence",
            "contribuable": "Numéro d’identification du contribuable",
            "libelle": "Motif",
        }

    def __init__(self, *args, **kwargs):
        super(NonRedevabiliteForm, self).__init__(*args, **kwargs)
        # Numero activité : Initialiser le champs numéro d'activité avec le nouveau nom chrono
        self.fields['reference'].initial = 'Auto - Chorno'
        self._id = int(self.instance.id or 0)

    def clean_reference(self):
        """
        Generer le numero matricule avant save
        """
        reference = self.cleaned_data['reference']
        # Mode création uniquement
        if self._id == 0:
            reference = ChronoHelpers.get_new_num(CHRONO_ATTESTATION_NON_REDEVABILITE)

        return reference
