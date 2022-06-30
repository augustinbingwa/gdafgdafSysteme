from django.utils.translation import gettext as _
from django import forms
from mod_foncier.models import FoncierCaracteristique, FoncierExpertise, FoncierImpot

class FoncierCaracteristiqueForm(forms.ModelForm):
    """
    Form Caractérstique technique d'une construction
    """
    class Meta:
        model = FoncierCaracteristique

        fields = ('impot_batie', 'superficie_batie') # , 'annee_mise_valeur'

        exclude = ('expertise',)
        
        labels = {
            "impot_batie": "Caractéristiques de la construction",
            "superficie_batie": "Superficie bâtie (m²)",
            #"annee_mise_valeur": "Année mise en valeur",
        }

    def __init__(self, *args, **kwargs):
        
        self._expertise = kwargs.pop('expertise', None)

        super(FoncierCaracteristiqueForm, self).__init__(*args, **kwargs)

        if self._expertise:
            self.fields['impot_batie'].queryset = FoncierImpot.objects.filter(accessibilite = self._expertise.parcelle.accessibilite)